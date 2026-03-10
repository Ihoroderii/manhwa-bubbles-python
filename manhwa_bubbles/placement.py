"""Smart bubble placement engine.

Detects characters via YOLO (optional) or uses known character positions from
the scenario, computes placement zones with face avoidance, prevents
bubble-to-bubble overlap, and handles narration placement.
"""
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .bubble_selector import BubbleStyle
from .scenario_parser import CharacterPosition, DialogueEntry


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Rect:
    """Axis-aligned rectangle."""
    x: int
    y: int
    w: int
    h: int

    @property
    def x2(self) -> int:
        return self.x + self.w

    @property
    def y2(self) -> int:
        return self.y + self.h

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    def overlaps(self, other: "Rect") -> bool:
        return not (
            self.x2 < other.x or other.x2 < self.x or
            self.y2 < other.y or other.y2 < self.y
        )


@dataclass
class Detection:
    """A detected character in the panel image."""
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    head: Tuple[int, int]            # (hx, hy)
    confidence: float = 1.0

    @property
    def width(self) -> int:
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> int:
        return self.bbox[3] - self.bbox[1]

    @property
    def face_rect(self) -> Rect:
        """Small region around the eyes/nose that bubbles should not fully
        cover.  Uses a fixed pixel offset from the head point so that
        bubbles placed above the head are never rejected.
        """
        hx, hy = self.head
        x1, y1, x2, y2 = self.bbox
        bw = x2 - x1
        face_w = min(int(bw * 0.35), 100)
        face_h = 50
        eye_y = hy + 30
        return Rect(hx - face_w // 2, eye_y, face_w, face_h)


@dataclass
class BubblePlacement:
    """Fully resolved placement for one bubble."""
    dialogue: DialogueEntry
    style: BubbleStyle
    rect: Rect                       # where the bubble goes on the image
    tail_target: Optional[Tuple[int, int]] = None  # character head coords
    tail_angle: float = 0.0          # angle from bubble center to head


# ---------------------------------------------------------------------------
# YOLO detection wrapper (optional dependency)
# ---------------------------------------------------------------------------

def detect_characters(image_path: str,
                      confidence: float = 0.25,
                      model_name: str = "yolov8n.pt") -> List[Detection]:
    """Run YOLO person detection on *image_path*.

    Returns an empty list if YOLO / OpenCV are not installed.
    """
    try:
        from ultralytics import YOLO  # type: ignore
    except ImportError:
        return []

    model = YOLO(model_name)
    results = model(image_path, conf=confidence, verbose=False)

    detections: List[Detection] = []
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) != 0:
                continue
            x1, y1, x2, y2 = (int(v) for v in box.xyxy[0].cpu().numpy())
            cx = (x1 + x2) // 2
            head_y = int(y1 + (y2 - y1) * 0.15)
            detections.append(Detection(
                bbox=(x1, y1, x2, y2),
                head=(cx, head_y),
                confidence=float(box.conf[0]),
            ))

    detections.sort(key=lambda d: d.head[0])
    return detections


# ---------------------------------------------------------------------------
# Placement zone generation
# ---------------------------------------------------------------------------

def _compute_candidate_rects(
    detection: Detection,
    bubble_w: int,
    bubble_h: int,
    image_w: int,
    image_h: int,
) -> List[Rect]:
    """Return candidate bubble Rects around *detection*, clamped to image.

    Positions are computed relative to the head and use the bubble size
    as the offset unit (not the character bbox), so results scale well
    regardless of how large the character's bounding box is.
    """
    hx, hy = detection.head
    bw2, bh2 = bubble_w // 2, bubble_h // 2
    candidates = []

    offsets = [
        # (dx, dy) — dx/dy in multiples of bubble half-size
        ( 0, -2.0),   # directly above
        (-1.0, -1.8),  # above-left
        ( 1.0, -1.8),  # above-right
        (-1.5, -1.2),  # far left, above
        ( 1.5, -1.2),  # far right, above
        (-2.0, -0.5),  # far left, beside
        ( 2.0, -0.5),  # far right, beside
        ( 0, -1.2),    # slightly above
    ]

    for dx_mult, dy_mult in offsets:
        cx = int(hx + dx_mult * bw2) - bw2
        cy = int(hy + dy_mult * bh2) - bh2
        cx = max(0, min(cx, image_w - bubble_w))
        cy = max(0, min(cy, image_h - bubble_h))
        candidates.append(Rect(cx, cy, bubble_w, bubble_h))

    return candidates


def _rect_overlaps_face(rect: Rect, face: Rect, head_y: int = 0) -> bool:
    """Check if bubble covers the face.  If the bubble's center is above the
    character's head, it is considered a natural "floating above" position
    and is never rejected."""
    if rect.cy < head_y:
        return False
    return rect.overlaps(face)


def _rect_overlaps_any(rect: Rect, placed: List[Rect]) -> bool:
    return any(rect.overlaps(r) for r in placed)


# ---------------------------------------------------------------------------
# Bubble sizing heuristics
# ---------------------------------------------------------------------------

def estimate_bubble_size(
    text: str,
    image_w: int,
    image_h: int,
    max_fraction: float = 0.35,
    min_w: int = 180,
    min_h: int = 80,
    engine: str = "pil",
    num_speakers: int = 1,
) -> Tuple[int, int]:
    """Rough bubble size from text length and panel dimensions.

    Cairo adaptive bubbles need a larger canvas because the overlapping
    ovals extend beyond the text area and text must fit inside the
    organic shape.  Minimum sizes are enforced so text does not overflow.
    """
    chars = len(text)

    speaker_scale = 1.0
    if num_speakers >= 3:
        speaker_scale = 0.55
    elif num_speakers == 2:
        speaker_scale = 0.70

    if engine in ("cairo_circle", "cairo_square"):
        est_w = max(280, int(chars * 10 + 120))
        est_h = max(240, int(est_w * 0.85))
        max_w = max(280, int(image_w * 0.48 * speaker_scale))
        max_h = max(240, int(image_h * 0.36 * speaker_scale))
        return min(est_w, max_w), min(est_h, max_h)

    est_w = max(min_w, int(chars * 9 + 40))
    est_h = max(min_h, 60 + 20 * max(1, chars // 25))

    max_w = int(image_w * max_fraction * speaker_scale)
    max_h = int(image_h * max_fraction * 0.5 * speaker_scale)

    return min(est_w, max_w), min(est_h, max_h)


# ---------------------------------------------------------------------------
# Narration placement
# ---------------------------------------------------------------------------

def _place_narration(
    dialogue: DialogueEntry,
    style: BubbleStyle,
    image_w: int,
    image_h: int,
    placed: List[Rect],
    index: int,
) -> BubblePlacement:
    """Place a narration box at the top or bottom edge of the panel."""
    bw, bh = estimate_bubble_size(dialogue.text, image_w, image_h)
    bw = min(int(image_w * 0.6), max(bw, int(image_w * 0.3)))
    bh = min(80, bh)

    margin = 15
    cx = (image_w - bw) // 2

    # Alternate top/bottom for successive narration boxes
    if index % 2 == 0:
        cy = margin
    else:
        cy = image_h - bh - margin

    rect = Rect(cx, cy, bw, bh)

    # Shift down/up if overlapping existing bubbles
    for _ in range(5):
        if not _rect_overlaps_any(rect, placed):
            break
        rect.y += bh + margin if index % 2 == 0 else -(bh + margin)

    rect.x = max(0, min(rect.x, image_w - bw))
    rect.y = max(0, min(rect.y, image_h - bh))

    return BubblePlacement(
        dialogue=dialogue,
        style=style,
        rect=rect,
        tail_target=None,
    )


# ---------------------------------------------------------------------------
# Manual character positions → Detection conversion
# ---------------------------------------------------------------------------

def positions_to_detections(
    characters: List[CharacterPosition],
) -> List[Detection]:
    """Convert known character positions to Detection objects.

    The resulting list is sorted left-to-right by head x-coordinate, matching
    the order produced by :func:`detect_characters`.
    """
    detections = []
    for cp in characters:
        detections.append(Detection(
            bbox=cp.bbox,
            head=cp.head,
            confidence=1.0,
        ))
    detections.sort(key=lambda d: d.head[0])
    return detections


def merge_detections(
    yolo_detections: List[Detection],
    manual_detections: List[Detection],
    iou_threshold: float = 0.3,
) -> List[Detection]:
    """Merge YOLO detections with manual positions, avoiding duplicates.

    If a manual detection overlaps significantly with a YOLO detection
    (IoU > *iou_threshold*), the YOLO one is kept (it may have a tighter
    bounding box).  Non-overlapping manual detections are appended.
    """
    if not manual_detections:
        return yolo_detections
    if not yolo_detections:
        return manual_detections

    def _iou(a: Detection, b: Detection) -> float:
        ax1, ay1, ax2, ay2 = a.bbox
        bx1, by1, bx2, by2 = b.bbox
        ix1, iy1 = max(ax1, bx1), max(ay1, by1)
        ix2, iy2 = min(ax2, bx2), min(ay2, by2)
        if ix2 <= ix1 or iy2 <= iy1:
            return 0.0
        inter = (ix2 - ix1) * (iy2 - iy1)
        area_a = (ax2 - ax1) * (ay2 - ay1)
        area_b = (bx2 - bx1) * (by2 - by1)
        return inter / (area_a + area_b - inter)

    merged = list(yolo_detections)
    for md in manual_detections:
        if not any(_iou(md, yd) > iou_threshold for yd in yolo_detections):
            merged.append(md)

    merged.sort(key=lambda d: d.head[0])
    return merged


# ---------------------------------------------------------------------------
# Detection ↔ character name mapping
# ---------------------------------------------------------------------------

def build_name_to_detection_map(
    characters: List[CharacterPosition],
    detections: List[Detection],
) -> Dict[str, int]:
    """Map character names to detection indices.

    Each manual ``CharacterPosition`` is matched to the closest ``Detection``
    (by head distance).  Returns ``{character_name: detection_index}``.
    """
    if not characters or not detections:
        return {}

    name_map: Dict[str, int] = {}
    used: set = set()

    for cp in characters:
        best_idx = None
        best_dist = float("inf")
        for i, det in enumerate(detections):
            if i in used:
                continue
            dx = cp.head[0] - det.head[0]
            dy = cp.head[1] - det.head[1]
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < best_dist:
                best_dist = dist
                best_idx = i
        if best_idx is not None:
            name_map[cp.name.lower()] = best_idx
            used.add(best_idx)

    return name_map


# ---------------------------------------------------------------------------
# Hint-to-detection matching
# ---------------------------------------------------------------------------

def _match_hint_to_detection(
    hint: Optional[str],
    detections: List[Detection],
    assigned: set,
) -> Optional[int]:
    """Return the index in *detections* that best matches *hint*."""
    if not detections:
        return None

    available = [i for i in range(len(detections)) if i not in assigned]
    if not available:
        return None

    if hint == "left":
        return available[0]
    if hint == "right":
        return available[-1]
    if hint == "center":
        return available[len(available) // 2]

    # No hint or unknown → pick first available
    return available[0]


def _match_character_to_detection(
    character_name: str,
    hint: Optional[str],
    detections: List[Detection],
    name_map: Dict[str, int],
    assigned: set,
) -> Optional[int]:
    """Match a dialogue's character to a detection, preferring name match."""
    key = character_name.lower()
    if key in name_map:
        idx = name_map[key]
        if idx not in assigned:
            return idx

    return _match_hint_to_detection(hint, detections, assigned)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def compute_placements(
    dialogues: List[Tuple[DialogueEntry, BubbleStyle]],
    image_w: int,
    image_h: int,
    detections: Optional[List[Detection]] = None,
    characters: Optional[List[CharacterPosition]] = None,
    seed: Optional[int] = None,
) -> List[BubblePlacement]:
    """Compute placement for every dialogue entry.

    Args:
        dialogues: List of (DialogueEntry, BubbleStyle) pairs.
        image_w, image_h: Panel image dimensions.
        detections: Character detections from YOLO (or ``None``).
        characters: Known character positions from the scenario.
            When provided, manual positions are merged with YOLO detections
            and character names are used for direct matching.
        seed: Optional RNG seed for reproducibility.

    Returns:
        List of BubblePlacement in the same order as *dialogues*.
    """
    if seed is not None:
        random.seed(seed)

    if detections is None:
        detections = []
    if characters is None:
        characters = []

    manual_dets = positions_to_detections(characters)
    detections = merge_detections(detections, manual_dets)

    name_map = build_name_to_detection_map(characters, detections)

    placed_rects: List[Rect] = []
    placements: List[BubblePlacement] = []
    assigned_dets: set = set()

    num_speakers = sum(1 for e, _ in dialogues if not e.is_narration())
    narration_idx = 0

    for entry, style in dialogues:
        # ---- Narration goes to panel edges ----
        if entry.is_narration():
            p = _place_narration(
                entry, style, image_w, image_h, placed_rects, narration_idx,
            )
            placed_rects.append(p.rect)
            placements.append(p)
            narration_idx += 1
            continue

        # ---- Speech bubble ----
        bw, bh = estimate_bubble_size(entry.text, image_w, image_h,
                                       engine=style.engine,
                                       num_speakers=num_speakers)

        det_idx = _match_character_to_detection(
            entry.character, entry.position_hint,
            detections, name_map, assigned_dets,
        )

        if det_idx is not None:
            assigned_dets.add(det_idx)
            det = detections[det_idx]

            candidates = _compute_candidate_rects(
                det, bw, bh, image_w, image_h,
            )

            hx, hy = det.head
            def _score(r: Rect) -> float:
                dx = abs(r.cx - hx)
                dy = r.cy - hy
                horiz_penalty = dx * 1.5
                above = dy < 0
                vert_cost = abs(dy)
                return horiz_penalty + vert_cost + (0 if above else 200)

            candidates.sort(key=_score)

            head_y = det.head[1]
            best: Optional[Rect] = None
            for cand in candidates:
                if _rect_overlaps_face(cand, det.face_rect, head_y):
                    continue
                if _rect_overlaps_any(cand, placed_rects):
                    continue
                best = cand
                break

            if best is None:
                for cand in candidates:
                    if not _rect_overlaps_face(cand, det.face_rect, head_y):
                        best = cand
                        break

            if best is None:
                best = candidates[0]

            tail_target = det.head
            dx = det.head[0] - best.cx
            dy = det.head[1] - best.cy
            tail_angle = math.atan2(dy, dx)

        else:
            margin = 20
            bx = random.randint(margin, max(margin, image_w - bw - margin))
            by = random.randint(margin, max(margin, image_h // 2 - bh))
            best = Rect(bx, by, bw, bh)

            for _ in range(10):
                if not _rect_overlaps_any(best, placed_rects):
                    break
                best.x = random.randint(margin, max(margin, image_w - bw - margin))
                best.y = random.randint(margin, max(margin, image_h // 2 - bh))

            tail_target = None
            tail_angle = 0.0

        placed_rects.append(best)
        placements.append(BubblePlacement(
            dialogue=entry,
            style=style,
            rect=best,
            tail_target=tail_target,
            tail_angle=tail_angle,
        ))

    return placements
