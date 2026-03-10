"""Parse LLM-generated scenario JSON into structured panel/dialogue data.

Expected input format (JSON)::

    {
      "panels": [
        {
          "panel_id": 1,
          "image": "panel_001.png",
          "characters": [
            {
              "name": "Hero",
              "bbox": [175, 560, 265, 900],
              "head": [220, 600]
            },
            {
              "name": "Villain",
              "bbox": [465, 610, 535, 860]
            }
          ],
          "dialogues": [
            {
              "character": "Hero",
              "text": "We need to go now!",
              "emotion": "shouting",
              "position_hint": "left"
            },
            {
              "character": "Narrator",
              "text": "The battle was about to begin...",
              "emotion": "narration"
            }
          ]
        }
      ]
    }

The ``characters`` array is optional.  When present, bubble placement uses
these known positions to anchor speech bubbles near the correct character
instead of relying solely on YOLO detection.  ``head`` is optional and will
be estimated from the upper-center of ``bbox`` when omitted.
"""
import json
from dataclasses import dataclass, field
from typing import List, Optional, Union

from .bubble_selector import list_all_keywords


@dataclass
class CharacterPosition:
    """Known position of a character in the panel image.

    Provided by the image-generation step so that bubble placement can anchor
    speech bubbles near the correct speaker without relying on YOLO.
    """
    name: str
    bbox: tuple  # (x1, y1, x2, y2) pixel coordinates
    head: Optional[tuple] = None  # (hx, hy) — estimated from bbox if absent

    def __post_init__(self):
        if self.head is None:
            x1, y1, x2, y2 = self.bbox
            self.head = ((x1 + x2) // 2, int(y1 + (y2 - y1) * 0.15))


@dataclass
class DialogueEntry:
    """Single dialogue line within a panel."""
    character: str
    text: str
    emotion: str = "normal"
    position_hint: Optional[str] = None  # "left", "right", "center", "top", "bottom"

    def is_narration(self) -> bool:
        return self.emotion in ("narration", "narrator", "caption")


@dataclass
class PanelData:
    """Parsed data for one manga panel."""
    panel_id: int
    image: str
    dialogues: List[DialogueEntry] = field(default_factory=list)
    characters: List[CharacterPosition] = field(default_factory=list)

    @property
    def speech_dialogues(self) -> List[DialogueEntry]:
        """Dialogues that are character speech (not narration)."""
        return [d for d in self.dialogues if not d.is_narration()]

    @property
    def narration_dialogues(self) -> List[DialogueEntry]:
        """Dialogues that are narration/caption."""
        return [d for d in self.dialogues if d.is_narration()]


@dataclass
class Scenario:
    """Full scenario containing multiple panels."""
    panels: List[PanelData] = field(default_factory=list)


class ScenarioParseError(Exception):
    """Raised when scenario JSON is invalid or malformed."""


_VALID_POSITION_HINTS = {"left", "right", "center", "top", "bottom", None}


def _normalize_emotion(emotion: str) -> str:
    """Normalize emotion string to a known keyword, or fall back to 'normal'."""
    normalized = emotion.lower().strip()
    known = set(list_all_keywords())
    if normalized in known:
        return normalized
    # fuzzy: strip trailing 's', 'ing', 'ly'
    for suffix in ("ing", "ly", "s"):
        if normalized.endswith(suffix):
            base = normalized[:-len(suffix)]
            if base in known:
                return base
    return "normal"


def _parse_dialogue(raw: dict, panel_id: int, idx: int) -> DialogueEntry:
    """Parse and validate a single dialogue entry."""
    if not isinstance(raw, dict):
        raise ScenarioParseError(
            f"Panel {panel_id}, dialogue {idx}: expected dict, got {type(raw).__name__}"
        )

    text = raw.get("text", "").strip()
    if not text:
        raise ScenarioParseError(
            f"Panel {panel_id}, dialogue {idx}: 'text' is required and cannot be empty"
        )

    character = raw.get("character", "Unknown").strip()
    emotion = _normalize_emotion(raw.get("emotion", "normal"))

    position_hint = raw.get("position_hint")
    if position_hint is not None:
        position_hint = position_hint.lower().strip()
        if position_hint not in _VALID_POSITION_HINTS:
            position_hint = None

    return DialogueEntry(
        character=character,
        text=text,
        emotion=emotion,
        position_hint=position_hint,
    )


def _parse_character(raw: dict, panel_id: int, idx: int) -> CharacterPosition:
    """Parse and validate a single character position entry."""
    if not isinstance(raw, dict):
        raise ScenarioParseError(
            f"Panel {panel_id}, character {idx}: expected dict, got {type(raw).__name__}"
        )

    name = raw.get("name", "").strip()
    if not name:
        raise ScenarioParseError(
            f"Panel {panel_id}, character {idx}: 'name' is required"
        )

    bbox = raw.get("bbox")
    if bbox is None or not isinstance(bbox, (list, tuple)) or len(bbox) != 4:
        raise ScenarioParseError(
            f"Panel {panel_id}, character {idx}: 'bbox' must be [x1, y1, x2, y2]"
        )
    bbox = tuple(int(v) for v in bbox)

    head_raw = raw.get("head")
    head = None
    if head_raw is not None:
        if isinstance(head_raw, (list, tuple)) and len(head_raw) == 2:
            head = (int(head_raw[0]), int(head_raw[1]))

    return CharacterPosition(name=name, bbox=bbox, head=head)


def _parse_panel(raw: dict, idx: int) -> PanelData:
    """Parse and validate a single panel."""
    if not isinstance(raw, dict):
        raise ScenarioParseError(
            f"Panel index {idx}: expected dict, got {type(raw).__name__}"
        )

    panel_id = raw.get("panel_id", idx + 1)
    image = raw.get("image", "")
    if not image:
        raise ScenarioParseError(
            f"Panel {panel_id}: 'image' path is required"
        )

    raw_characters = raw.get("characters", [])
    if not isinstance(raw_characters, list):
        raise ScenarioParseError(
            f"Panel {panel_id}: 'characters' must be a list"
        )
    characters = [
        _parse_character(c, panel_id, i)
        for i, c in enumerate(raw_characters)
    ]

    raw_dialogues = raw.get("dialogues", [])
    if not isinstance(raw_dialogues, list):
        raise ScenarioParseError(
            f"Panel {panel_id}: 'dialogues' must be a list"
        )
    dialogues = [
        _parse_dialogue(d, panel_id, i)
        for i, d in enumerate(raw_dialogues)
    ]

    return PanelData(
        panel_id=panel_id, image=image,
        dialogues=dialogues, characters=characters,
    )


def parse_scenario(data: Union[str, dict]) -> Scenario:
    """Parse scenario JSON string or dict into a Scenario object.

    Args:
        data: JSON string or already-parsed dict with the scenario.

    Returns:
        Scenario with validated PanelData entries.

    Raises:
        ScenarioParseError: If the input is malformed.
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ScenarioParseError(f"Invalid JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise ScenarioParseError(
            f"Scenario root must be a dict, got {type(data).__name__}"
        )

    raw_panels = data.get("panels")
    if raw_panels is None:
        raise ScenarioParseError("Missing 'panels' key in scenario")
    if not isinstance(raw_panels, list):
        raise ScenarioParseError("'panels' must be a list")
    if len(raw_panels) == 0:
        raise ScenarioParseError("'panels' list is empty")

    panels = [_parse_panel(p, i) for i, p in enumerate(raw_panels)]
    return Scenario(panels=panels)


def parse_scenario_file(path: str) -> Scenario:
    """Load and parse a scenario from a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return parse_scenario(f.read())
