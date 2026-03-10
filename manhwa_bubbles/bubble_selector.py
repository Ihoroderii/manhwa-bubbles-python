"""Emotion-to-bubble-style mapping engine.

Given an emotion string (from LLM scenario output), selects the appropriate
bubble style and rendering engine (PIL or Cairo adaptive bubbles).

When Cairo (pycairo) is available the engine prefers the adaptive_circle_bubble /
adaptive_square_bubble renderers from ``examples/experiments/adaptive_bubbles.py``
which produce professional organic overlapping-oval shapes with auto-text-fitting,
word-wrapping and tails.  PIL styles are kept as fallback and for specialty shapes.
"""
import random
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from . import speech_bubbles, narrators, extended_styles

try:
    import cairo as _cairo_mod  # type: ignore
    _HAS_CAIRO = True
except ImportError:
    _HAS_CAIRO = False


@dataclass
class BubbleStyle:
    """Resolved bubble style ready for rendering."""
    name: str
    engine: str          # "pil", "cairo_circle", "cairo_square"
    draw_func: object = None
    bubble_type: Optional[str] = None
    pil_kwargs: dict = field(default_factory=dict)
    cairo_kwargs: dict = field(default_factory=dict)


# ── Cairo adaptive bubble helpers ──────────────────────────────────
# variant: radial5 (calm) / radial6 (normal) / radial7 (energetic)
# shape:   "circle" → adaptive_circle_bubble
#          "square" → adaptive_square_bubble

def _cc(variant="radial5", **extra):
    """Short-hand: Cairo circle candidate."""
    cfg = {"variant": variant}
    cfg.update(extra)
    return ("cairo_circle_" + variant, "cairo_circle", cfg)

def _cs(**extra):
    """Short-hand: Cairo square candidate."""
    cfg = dict(extra)
    return ("cairo_square", "cairo_square", cfg)


# Each emotion maps to a list of candidate styles.
# Cairo candidates come first; PIL fallbacks follow.

_EMOTION_MAP = {
    # --- Normal / neutral ---
    "normal": [
        _cc("radial5"),
        _cc("radial6"),
        _cs(),
        ("oval", "pil", {"bubble_type": "oval"}),
    ],
    "neutral": "normal",

    # --- Shouting / angry ---
    "shouting": [
        _cc("radial7"),
        _cc("radial6"),
        ("jagged", "pil", {"bubble_type": "jagged"}),
        ("shout_burst", "pil", {"func": "bubble_shout_burst"}),
    ],
    "angry": "shouting",
    "yelling": "shouting",

    # --- Rage ---
    "rage": [
        _cc("radial7"),
        ("rage_flame", "pil", {"func": "bubble_rage_flame"}),
    ],

    # --- Whispering / quiet ---
    "whispering": [
        _cc("radial5"),
        ("whisper_dotted", "pil", {"func": "bubble_whisper_dotted"}),
        ("whisper_thought", "pil", {"func": "bubble_whisper_thought"}),
    ],
    "quiet": "whispering",

    # --- Thinking / internal ---
    "thinking": [
        _cc("radial5"),
        _cs(),
        ("cloud", "pil", {"bubble_type": "cloud"}),
        ("thought_cloud_chain", "pil", {"func": "bubble_thought_cloud_chain"}),
    ],
    "internal": "thinking",
    "thought": "thinking",

    # --- Laughing / happy ---
    "laughing": [
        _cc("radial7"),
        _cc("radial6"),
        ("laugh_bouncy", "pil", {"func": "bubble_laugh_bouncy"}),
    ],
    "happy": "laughing",
    "giggling": "laughing",

    # --- Crying / sad ---
    "crying": [
        _cc("radial5"),
        ("cry_drip", "pil", {"func": "bubble_cry_drip"}),
    ],
    "sad": "crying",

    # --- Scared / shocked ---
    "scared": [
        _cc("radial6"),
        ("shock_mini_spike", "pil", {"func": "bubble_shock_mini_spike"}),
        ("nervous_wobble", "pil", {"func": "bubble_nervous_wobble"}),
    ],
    "shocked": "scared",
    "nervous": "scared",

    # --- Narration (PIL narration boxes — no Cairo needed) ---
    "narration": [
        _cs(),
        ("narrator_plain", "pil", {"func": "narrator_plain", "module": "narrators"}),
        ("narrator_dark", "pil", {"func": "narrator_dark", "module": "narrators"}),
        ("narrator_borderless", "pil", {"func": "narrator_borderless", "module": "narrators"}),
    ],
    "narrator": "narration",
    "caption": "narration",

    # --- Supernatural / magic ---
    "magic": [
        _cc("radial7"),
        ("magic_glow_frame", "pil", {"func": "bubble_magic_glow_frame"}),
        ("arcane_glyph", "pil", {"func": "bubble_arcane_glyph"}),
    ],
    "supernatural": "magic",

    # --- Telepathy ---
    "telepathy": [
        _cc("radial5"),
        ("telepathy_wave", "pil", {"func": "bubble_telepathy_wave"}),
    ],

    # --- Ghost ---
    "ghost": [
        _cc("radial5"),
        ("ghost_translucent", "pil", {"func": "bubble_ghost_translucent"}),
    ],

    # --- Horror ---
    "horror": [
        _cc("radial7"),
        ("dripping_horror", "pil", {"func": "bubble_dripping_horror"}),
        ("scratchy", "pil", {"bubble_type": "scratchy"}),
    ],
    "creepy": "horror",

    # --- Digital / radio / tech ---
    "digital": [
        _cs(),
        ("digital_system", "pil", {"func": "bubble_digital_system"}),
        ("ai_card", "pil", {"func": "bubble_ai_card"}),
    ],
    "radio": [
        _cs(),
        ("radio_comms", "pil", {"func": "bubble_radio_comms"}),
    ],
    "robotic": [
        _cs(),
        ("robotic_panel", "pil", {"func": "bubble_robotic_panel"}),
    ],

    # --- SFX / impact ---
    "sfx": [
        _cc("radial7"),
        ("sfx_capsule", "pil", {"func": "bubble_sfx_capsule"}),
        ("impact_bang", "pil", {"func": "bubble_impact_bang"}),
    ],
    "impact": "sfx",
    "sound_effect": "sfx",

    # --- Sarcastic ---
    "sarcastic": [
        _cs(),
        ("sarcastic_geometric", "pil", {"func": "bubble_sarcastic_geometric"}),
    ],

    # --- Cold / frozen ---
    "cold": [
        _cc("radial5"),
        ("breath_cold", "pil", {"func": "bubble_breath_cold"}),
    ],
    "frozen": "cold",

    # --- Drunk / dizzy ---
    "drunk": [
        _cc("radial6"),
        ("drunk_slur", "pil", {"func": "bubble_drunk_slur"}),
    ],
    "dizzy": "drunk",

    # --- Sleepy ---
    "sleepy": [
        _cc("radial5"),
        ("sleepy_slump", "pil", {"func": "bubble_sleepy_slump"}),
    ],
    "tired": "sleepy",

    # --- Romantic ---
    "romantic": [
        _cc("radial5"),
        ("heart", "pil", {"bubble_type": "heart"}),
    ],
    "love": "romantic",

    # --- Dark / evil ---
    "dark": [
        _cc("radial7"),
        _cs(),
        ("black", "pil", {"bubble_type": "black"}),
        ("inverted_aura", "pil", {"func": "bubble_inverted_aura"}),
    ],
    "evil": "dark",

    # --- Hypnotic ---
    "hypnotic": [
        _cc("radial6"),
        ("hypnotic_spiral", "pil", {"func": "bubble_hypnotic_spiral"}),
    ],

    # --- Choral / chanting ---
    "choral": [
        _cc("radial7"),
        ("chant_choral", "pil", {"func": "bubble_chant_choral"}),
    ],
    "chanting": "choral",

    # --- Echo ---
    "echo": [
        _cc("radial6"),
        ("echo_layers", "pil", {"func": "bubble_echo_layers"}),
    ],
}


def _resolve_alias(emotion: str) -> List[tuple]:
    """Resolve emotion aliases and return candidate list."""
    emotion = emotion.lower().strip()
    value = _EMOTION_MAP.get(emotion)
    if value is None:
        return _EMOTION_MAP["normal"]
    if isinstance(value, str):
        return _resolve_alias(value)
    return value


def _get_draw_func(config: dict):
    """Return the callable drawing function from config."""
    module_name = config.get("module", "extended_styles")
    func_name = config.get("func")

    if func_name is None:
        return None

    if module_name == "narrators":
        return getattr(narrators, func_name, None)
    return getattr(extended_styles, func_name, None)


def select_bubble_style(emotion: str, seed: Optional[int] = None,
                        prefer_cairo: bool = True) -> BubbleStyle:
    """Pick a bubble style for the given emotion.

    Args:
        emotion: Emotion/context string (e.g. "shouting", "narration", "sad").
        seed: Optional random seed for reproducible selection.
        prefer_cairo: When True and Cairo is available, Cairo candidates are
            eligible; otherwise only PIL candidates are returned.

    Returns:
        BubbleStyle with all info needed to render.
    """
    if seed is not None:
        random.seed(seed)

    candidates = _resolve_alias(emotion)

    if not prefer_cairo or not _HAS_CAIRO:
        pil_only = [c for c in candidates if c[1] == "pil"]
        candidates = pil_only or candidates

    name, engine, config = random.choice(candidates)

    style = BubbleStyle(
        name=name,
        engine=engine,
        bubble_type=config.get("bubble_type"),
        draw_func=_get_draw_func(config),
        pil_kwargs={k: v for k, v in config.items()
                    if k not in ("func", "module", "bubble_type", "style", "variant")},
        cairo_kwargs={k: v for k, v in config.items()
                      if k in ("style", "variant")},
    )
    return style


def list_emotions() -> List[str]:
    """Return sorted list of all recognized emotion keywords (excluding aliases)."""
    return sorted(k for k, v in _EMOTION_MAP.items() if not isinstance(v, str))


def list_all_keywords() -> List[str]:
    """Return sorted list of all recognized keywords including aliases."""
    return sorted(_EMOTION_MAP.keys())


def get_candidates(emotion: str) -> List[str]:
    """Return the candidate style names for an emotion."""
    return [name for name, _, _ in _resolve_alias(emotion)]
