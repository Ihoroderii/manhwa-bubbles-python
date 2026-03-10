"""End-to-end manga bubble pipeline.

Takes an AI-generated panel image + LLM scenario JSON and produces the final
manga page with speech bubbles automatically placed and styled.

The pipeline prefers the Cairo-based adaptive bubble renderers
(``adaptive_circle_bubble`` / ``adaptive_square_bubble``) you developed in
``examples/experiments/adaptive_bubbles.py``.  These produce professional
organic overlapping-oval shapes with auto-text-fitting, word-wrapping, and
tails.  PIL renderers are used as fallback or for specialty shapes.

Usage::

    from manhwa_bubbles.pipeline import process_manga_page

    result = process_manga_page(
        image_path="panel_001.png",
        scenario={"panels": [{"panel_id": 1, "image": "panel_001.png",
                               "dialogues": [{"character": "Hero",
                                              "text": "Let's go!",
                                              "emotion": "shouting"}]}]},
        output_path="panel_001_final.png",
    )
"""
import math
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image, ImageDraw, ImageFont

from .bubble_selector import BubbleStyle, select_bubble_style
from .scenario_parser import (
    DialogueEntry,
    PanelData,
    Scenario,
    ScenarioParseError,
    parse_scenario,
)
from .placement import (
    BubblePlacement,
    Detection,
    Rect,
    compute_placements,
    detect_characters,
    merge_detections,
    positions_to_detections,
)
from . import speech_bubbles, narrators, extended_styles


# ---------------------------------------------------------------------------
# Lazy-load Cairo adaptive bubble functions
# ---------------------------------------------------------------------------

_adaptive_circle_bubble = None
_adaptive_square_bubble = None
_cairo_adaptive_loaded = False


def _load_adaptive_bubbles():
    global _adaptive_circle_bubble, _adaptive_square_bubble, _cairo_adaptive_loaded
    if _cairo_adaptive_loaded:
        return
    _cairo_adaptive_loaded = True

    try:
        import cairo  # noqa: F401
    except ImportError:
        return

    exp_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'experiments')
    exp_path = os.path.abspath(exp_path)
    if exp_path not in sys.path and os.path.isdir(exp_path):
        sys.path.insert(0, exp_path)

    try:
        from adaptive_bubbles import adaptive_circle_bubble, adaptive_square_bubble
        _adaptive_circle_bubble = adaptive_circle_bubble
        _adaptive_square_bubble = adaptive_square_bubble
    except ImportError:
        pass


# ---------------------------------------------------------------------------
# Result container
# ---------------------------------------------------------------------------

@dataclass
class PipelineResult:
    """Result of processing one panel."""
    panel_id: int
    image_path: str
    output_path: str
    placements: List[BubblePlacement] = field(default_factory=list)
    detections: List[Detection] = field(default_factory=list)


# ---------------------------------------------------------------------------
# PIL rendering helpers
# ---------------------------------------------------------------------------

def _draw_tail_pil(draw: ImageDraw.ImageDraw,
                   placement: BubblePlacement) -> None:
    """Draw a triangular tail from bubble center toward the character head."""
    if placement.tail_target is None:
        return

    r = placement.rect
    hx, hy = placement.tail_target
    bcx, bcy = r.cx, r.cy

    dx = hx - bcx
    dy = hy - bcy
    dist = math.sqrt(dx * dx + dy * dy) or 1.0
    ux, uy = dx / dist, dy / dist

    half_w, half_h = r.w / 2, r.h / 2
    attach_x = bcx + half_w * 0.8 * ux
    attach_y = bcy + half_h * 0.8 * uy

    tail_len = min(80, dist * 0.5)
    tip_x = attach_x + ux * tail_len
    tip_y = attach_y + uy * tail_len

    # Perpendicular direction for tail width
    px, py = -uy, ux
    tw = 18
    base_left  = (attach_x + px * tw, attach_y + py * tw)
    base_right = (attach_x - px * tw, attach_y - py * tw)
    tip = (tip_x, tip_y)

    # Bezier control points for smooth curved edges — slight outward bow
    cp_l = (attach_x + px * tw * 0.5 + ux * tail_len * 0.5,
            attach_y + py * tw * 0.5 + uy * tail_len * 0.5)
    cp_r = (attach_x - px * tw * 0.5 + ux * tail_len * 0.5,
            attach_y - py * tw * 0.5 + uy * tail_len * 0.5)

    # Build smooth polygon via cubic Bezier sampling
    steps = 12
    points = []
    for i in range(steps + 1):
        t = i / steps
        u = 1 - t
        bx = u**3*base_left[0] + 3*u**2*t*cp_l[0] + 3*u*t**2*cp_l[0] + t**3*tip[0]
        by = u**3*base_left[1] + 3*u**2*t*cp_l[1] + 3*u*t**2*cp_l[1] + t**3*tip[1]
        points.append((bx, by))
    for i in range(steps, -1, -1):
        t = i / steps
        u = 1 - t
        bx = u**3*base_right[0] + 3*u**2*t*cp_r[0] + 3*u*t**2*cp_r[0] + t**3*tip[0]
        by = u**3*base_right[1] + 3*u**2*t*cp_r[1] + 3*u*t**2*cp_r[1] + t**3*tip[1]
        points.append((bx, by))

    draw.polygon(points, fill="white", outline="black", width=2)


def _render_pil_bubble(draw: ImageDraw.ImageDraw,
                       placement: BubblePlacement) -> None:
    """Render a PIL-engine bubble onto *draw*."""
    r = placement.rect
    xy = (r.x, r.y, r.w, r.h)
    text = placement.dialogue.text
    style = placement.style

    if style.bubble_type:
        speech_bubbles.speech_bubble(draw, xy, text,
                                     bubble_type=style.bubble_type,
                                     tail_dir="down")
    elif style.draw_func is not None:
        try:
            style.draw_func(draw, xy, text, **style.pil_kwargs)
        except TypeError:
            style.draw_func(draw, xy, text)
    else:
        draw.ellipse((r.x, r.y, r.x2, r.y2),
                     fill="white", outline="black", width=2)
        font = ImageFont.load_default()
        draw.text((r.x + 10, r.y + 10), text, font=font, fill="black")

    _draw_tail_pil(draw, placement)


# ---------------------------------------------------------------------------
# Cairo adaptive bubble rendering
# ---------------------------------------------------------------------------

def _render_cairo_adaptive(image: Image.Image,
                           placement: BubblePlacement) -> Image.Image:
    """Render using adaptive_circle_bubble / adaptive_square_bubble.

    These are the organic overlapping-oval bubbles with auto-text-fitting,
    word-wrapping, and Cairo-drawn tails that were built in experiments/.
    Falls back to PIL if the adaptive module is unavailable.
    """
    _load_adaptive_bubbles()

    engine = placement.style.engine
    r = placement.rect
    text = placement.dialogue.text
    seed = hash(text) & 0x7FFFFFFF

    # Compute tail target relative to the bubble canvas
    tail_target = None
    if placement.tail_target is not None:
        hx, hy = placement.tail_target
        tail_target = (hx - r.x, hy - r.y)

    canvas_size = (r.w, r.h)
    variant = placement.style.cairo_kwargs.get("variant", "radial5")

    surface = None
    if engine == "cairo_circle" and _adaptive_circle_bubble is not None:
        surface, _meta = _adaptive_circle_bubble(
            text,
            variant=variant,
            canvas_size=canvas_size,
            seed=seed,
            wrap=True,
            max_lines=4,
            max_iterations=8,
            tail_target=tail_target,
            max_panel_fraction=0.82,
            target_inner_padding=12,
            min_font_size=14,
            ensure_inside=True,
            verify_attempts=10,
        )
    elif engine == "cairo_square" and _adaptive_square_bubble is not None:
        surface, _meta = _adaptive_square_bubble(
            text,
            canvas_size=canvas_size,
            seed=seed,
            wrap=True,
            max_lines=4,
            max_iterations=8,
            tail_target=tail_target,
            max_panel_fraction=0.82,
            target_inner_padding=12,
            min_font_size=14,
            ensure_inside=True,
            verify_attempts=10,
        )

    if surface is None:
        draw = ImageDraw.Draw(image)
        _render_pil_bubble(draw, placement)
        return image

    bubble_pil = Image.frombuffer(
        "RGBA",
        (surface.get_width(), surface.get_height()),
        surface.get_data(),
        "raw", "BGRA", 0, 1,
    )

    image = image.convert("RGBA")
    temp = Image.new("RGBA", image.size, (0, 0, 0, 0))
    paste_x = max(0, min(r.x, image.width - bubble_pil.width))
    paste_y = max(0, min(r.y, image.height - bubble_pil.height))
    temp.paste(bubble_pil, (paste_x, paste_y), bubble_pil)
    image = Image.alpha_composite(image, temp)

    return image


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def process_panel(
    image_path: str,
    panel: PanelData,
    output_path: Optional[str] = None,
    yolo_confidence: float = 0.25,
    yolo_model: str = "yolov8n.pt",
    use_yolo: bool = True,
    prefer_cairo: bool = True,
    seed: Optional[int] = None,
) -> PipelineResult:
    """Process a single panel: detect -> select styles -> place -> render.

    Args:
        image_path: Path to the panel image file.
        panel: Parsed PanelData with dialogue entries.
        output_path: Where to save the result. Defaults to ``<name>_bubbles.png``.
        yolo_confidence: YOLO confidence threshold.
        yolo_model: YOLO model file name.
        use_yolo: Whether to attempt YOLO detection.
        prefer_cairo: Prefer Cairo renderer when available.
        seed: Random seed for reproducible results.

    Returns:
        PipelineResult with metadata about what was done.
    """
    if output_path is None:
        base = image_path.rsplit(".", 1)[0]
        output_path = f"{base}_bubbles.png"

    image = Image.open(image_path).convert("RGBA")
    img_w, img_h = image.size

    # 1. Detect characters (YOLO + manual positions from scenario)
    yolo_dets: List[Detection] = []
    if use_yolo:
        yolo_dets = detect_characters(image_path, yolo_confidence, yolo_model)
    manual_dets = positions_to_detections(panel.characters)
    detections = merge_detections(yolo_dets, manual_dets)

    # 2. Select bubble styles for each dialogue
    styled_dialogues = []
    for i, entry in enumerate(panel.dialogues):
        style = select_bubble_style(
            entry.emotion,
            seed=(seed + i) if seed is not None else None,
            prefer_cairo=prefer_cairo,
        )
        styled_dialogues.append((entry, style))

    # 3. Compute placements (with name-based matching when characters are known)
    placements = compute_placements(
        styled_dialogues, img_w, img_h,
        detections=detections,
        characters=panel.characters,
        seed=seed,
    )

    # 4. Render each bubble
    draw = ImageDraw.Draw(image)
    for p in placements:
        if p.style.engine in ("cairo_circle", "cairo_square"):
            image = _render_cairo_adaptive(image, p)
            draw = ImageDraw.Draw(image)
        else:
            _render_pil_bubble(draw, p)

    # 5. Save
    image.save(output_path)

    return PipelineResult(
        panel_id=panel.panel_id,
        image_path=image_path,
        output_path=output_path,
        placements=placements,
        detections=detections,
    )


def process_manga_page(
    image_path: str,
    scenario: Union[str, dict],
    output_path: Optional[str] = None,
    panel_index: int = 0,
    **kwargs,
) -> PipelineResult:
    """High-level entry point: parse scenario + process one panel.

    This is the simplest way to add bubbles to a manga page::

        result = process_manga_page(
            "panel.png",
            {"panels": [{"panel_id": 1, "image": "panel.png",
                          "dialogues": [{"character": "A",
                                         "text": "Hi!",
                                         "emotion": "normal"}]}]},
        )

    Args:
        image_path: Path to the panel image.
        scenario: JSON string or dict with the full scenario.
        output_path: Where to save. Defaults to ``<name>_bubbles.png``.
        panel_index: Which panel in the scenario to process (default 0).
        **kwargs: Forwarded to :func:`process_panel`.

    Returns:
        PipelineResult.
    """
    parsed = parse_scenario(scenario)
    if panel_index >= len(parsed.panels):
        raise ScenarioParseError(
            f"panel_index {panel_index} out of range "
            f"(scenario has {len(parsed.panels)} panels)"
        )
    panel = parsed.panels[panel_index]
    return process_panel(image_path, panel, output_path, **kwargs)


def process_all_panels(
    scenario: Union[str, dict],
    image_dir: str = ".",
    output_dir: Optional[str] = None,
    **kwargs,
) -> List[PipelineResult]:
    """Process every panel in a scenario.

    Args:
        scenario: Full scenario JSON/dict.
        image_dir: Directory where panel images are located.
        output_dir: Directory for output files (defaults to *image_dir*).
        **kwargs: Forwarded to :func:`process_panel`.

    Returns:
        List of PipelineResult, one per panel.
    """
    import os
    parsed = parse_scenario(scenario)
    if output_dir is None:
        output_dir = image_dir

    results = []
    for panel in parsed.panels:
        img_path = os.path.join(image_dir, panel.image)
        out_name = f"{os.path.splitext(panel.image)[0]}_bubbles.png"
        out_path = os.path.join(output_dir, out_name)
        r = process_panel(img_path, panel, out_path, **kwargs)
        results.append(r)

    return results
