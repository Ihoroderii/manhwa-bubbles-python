"""
Auto-scaling wrapper for manga panel bubbles.
Automatically adjusts bubble size based on panel dimensions.
"""

import importlib
import math
import random
from typing import Tuple, Optional, Dict

try:
    import cairo  # type: ignore
except ImportError:
    cairo = None
    _CAIRO_IMPORT_ERROR = "pycairo is required for auto-scaling"

create_overlapping_circles_square = None


def _load_overlapping_circles():
    """Lazy-load create_overlapping_circles_square from experiments."""
    global create_overlapping_circles_square
    if create_overlapping_circles_square is not None:
        return

    import os, sys
    experiments_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'experiments')
    if os.path.exists(experiments_path) and experiments_path not in sys.path:
        sys.path.insert(0, experiments_path)

    for module_path in (
        'overlapping_circles_squares',
        'examples.experiments.overlapping_circles_squares',
    ):
        try:
            mod = importlib.import_module(module_path)
            create_overlapping_circles_square = mod.create_overlapping_circles_square
            return
        except (ImportError, AttributeError):
            continue


def _ensure_cairo():
    """Ensure Cairo is available."""
    if cairo is None:
        raise RuntimeError(
            f"pycairo is required for auto-scaling but is not installed: "
            f"{_CAIRO_IMPORT_ERROR if '_CAIRO_IMPORT_ERROR' in globals() else 'Unknown error'}"
        )


def find_free_bbox_rect(cx: float, cy: float, half_w: float, half_h: float, 
                        circles: list, samples: int = 140) -> Tuple[float, float, float, float]:
    """
    Find free bounding box inside rectangle bubble.
    Returns (center_x, center_y, width, height) of free space.
    
    Args:
        cx, cy: Center of rectangle
        half_w, half_h: Half width and height of rectangle
        circles: List of circle dictionaries with 'x', 'y', 'rx', 'ry'
        samples: Number of sample points to check
    
    Returns:
        Tuple of (center_x, center_y, width, height) of free space
    """
    if not circles:
        return (cx, cy, half_w * 2, half_h * 2)
    
    # Sample points inside rectangle
    min_x, max_x = cx - half_w, cx + half_w
    min_y, max_y = cy - half_h, cy + half_h
    
    free_points = []
    for _ in range(samples):
        px = random.uniform(min_x, max_x)
        py = random.uniform(min_y, max_y)
        
        # Check if point is NOT inside any circle
        is_free = True
        for circle in circles:
            dx = (px - circle['x']) / circle['rx']
            dy = (py - circle['y']) / circle['ry']
            if dx*dx + dy*dy <= 1.0:
                is_free = False
                break
        
        if is_free:
            free_points.append((px, py))
    
    if not free_points:
        return (cx, cy, 0, 0)
    
    # Calculate bounding box of free points
    xs = [p[0] for p in free_points]
    ys = [p[1] for p in free_points]
    
    return (
        (min(xs) + max(xs)) / 2,  # center_x
        (min(ys) + max(ys)) / 2,  # center_y
        max(xs) - min(xs),         # width
        max(ys) - min(ys)          # height
    )


def auto_scale_bubble_for_panel(
    panel_width: int,
    panel_height: int,
    text: str = "",
    style: str = "organic",
    position: Optional[Tuple[float, float]] = None,  # (x_ratio, y_ratio) 0.0-1.0
    max_panel_fraction: float = 0.4,  # Max 40% of panel size
    min_panel_fraction: float = 0.15,  # Min 15% of panel size
    text_padding: float = 0.1,  # 10% padding for text
    aspect_ratio: Optional[float] = None,  # None = auto-calculate
    show_full_ovals: bool = False,
    seed: Optional[int] = None,
    background_color: Optional[Tuple[float, float, float]] = None  # (r, g, b) for background-aware colors
) -> Tuple:
    """
    Automatically scale bubble to fit manga panel.
    
    Args:
        panel_width: Width of manga panel in pixels
        panel_height: Height of manga panel in pixels
        text: Text content (affects size if provided)
        style: Bubble style ("organic", "laugh", "varied")
        position: Optional (x_ratio, y_ratio) position (0.0-1.0), None = center
        max_panel_fraction: Maximum fraction of panel size (0.0-1.0)
        min_panel_fraction: Minimum fraction of panel size (0.0-1.0)
        text_padding: Padding around text as fraction
        aspect_ratio: Optional fixed aspect ratio, None = auto
        show_full_ovals: Show full ovals or minimal mode
        seed: Random seed for reproducibility
    
    Returns:
        (surface, ctx, metadata_dict)
    """
    _ensure_cairo()
    _load_overlapping_circles()

    if create_overlapping_circles_square is None:
        raise RuntimeError(
            "create_overlapping_circles_square not found. "
            "Ensure examples/experiments/overlapping_circles_squares.py exists."
        )

    if seed is not None:
        random.seed(seed)
    
    # Calculate base size based on panel dimensions
    panel_min_dim = min(panel_width, panel_height)
    panel_max_dim = max(panel_width, panel_height)
    
    # Auto-calculate bubble size
    if text:
        # Estimate text size (rough approximation)
        estimated_text_width = len(text) * 8  # ~8 pixels per character
        estimated_text_height = 20  # Base line height
        
        # Calculate required bubble size with padding
        required_width = estimated_text_width * (1 + 2 * text_padding)
        required_height = estimated_text_height * (1 + 2 * text_padding)
        
        # Scale to fit panel constraints
        max_width = panel_width * max_panel_fraction
        max_height = panel_height * max_panel_fraction
        min_width = panel_width * min_panel_fraction
        min_height = panel_height * min_panel_fraction
        
        # Clamp to constraints
        bubble_width = max(min_width, min(required_width, max_width))
        bubble_height = max(min_height, min(required_height, max_height))
    else:
        # No text: use proportional sizing
        bubble_width = panel_min_dim * max_panel_fraction
        bubble_height = panel_min_dim * max_panel_fraction * 0.7  # Slightly taller
        
        # Respect aspect ratio if provided
        if aspect_ratio:
            if bubble_width / bubble_height > aspect_ratio:
                bubble_width = bubble_height * aspect_ratio
            else:
                bubble_height = bubble_width / aspect_ratio
    
    # Calculate position
    if position is None:
        cx = panel_width / 2
        cy = panel_height / 2
    else:
        cx = panel_width * position[0]
        cy = panel_height * position[1]
    
    # Create surface matching panel size
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_width, panel_height)
    ctx = cairo.Context(surface)
    
    # Set background color if provided
    if background_color is not None:
        if len(background_color) >= 3:
            if len(background_color) == 4:
                ctx.set_source_rgba(*background_color)
            else:
                ctx.set_source_rgb(*background_color)
            ctx.paint()
        else:
            # Transparent background
            ctx.set_source_rgba(0, 0, 0, 0)
            ctx.paint()
    else:
        # Transparent background
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.paint()
    
    # Draw bubble at calculated size and position
    create_overlapping_circles_square(
        ctx, cx, cy, bubble_width, bubble_height,
        text=text, circle_style=style,
        show_full_ovals=show_full_ovals,
        background_color=background_color
    )
    
    # Return metadata
    metadata = {
        'bubble_size': (bubble_width, bubble_height),
        'position': (cx, cy),
        'panel_size': (panel_width, panel_height),
        'scale_factor': bubble_width / 180.0,  # Relative to default 180
        'panel_fraction': (bubble_width / panel_width, bubble_height / panel_height)
    }
    
    return surface, ctx, metadata


def auto_scale_bubble_adaptive(
    panel_width: int,
    panel_height: int,
    text: str = "",
    style: str = "organic",
    target_text_padding: int = 20,
    max_panel_fraction: float = 0.35,
    min_font_size: int = 12,
    max_iterations: int = 6,
    show_full_ovals: bool = False,
    seed: Optional[int] = None,
    background_color: Optional[Tuple[float, float, float]] = None  # (r, g, b) for background-aware colors
) -> Tuple:
    """
    Adaptive auto-scaling: iteratively adjusts size to fit text perfectly.
    
    Args:
        panel_width, panel_height: Panel dimensions
        text: Text to fit inside bubble
        style: Bubble style
        target_text_padding: Desired padding around text in pixels
        max_panel_fraction: Maximum fraction of panel
        min_font_size: Minimum font size
        max_iterations: Max iterations for adaptive sizing
        show_full_ovals: Show full ovals
        seed: Random seed
    
    Returns:
        (surface, ctx, metadata)
    """
    _ensure_cairo()
    _load_overlapping_circles()

    if create_overlapping_circles_square is None:
        raise RuntimeError(
            "create_overlapping_circles_square not found. "
            "Ensure examples/experiments/overlapping_circles_squares.py exists."
        )

    if seed is not None:
        random.seed(seed)
    
    # Measure text (simplified - you might want to use actual font metrics)
    if text:
        # Estimate text dimensions
        chars_per_line = int((panel_width * max_panel_fraction) / 8)
        num_lines = max(1, (len(text) + chars_per_line - 1) // chars_per_line)
        text_width = min(len(text) * 8, panel_width * max_panel_fraction * 0.8)
        text_height = num_lines * (min_font_size + 4)
        
        required_width = text_width + 2 * target_text_padding
        required_height = text_height + 2 * target_text_padding
    else:
        # Default size
        required_width = panel_width * max_panel_fraction * 0.6
        required_height = panel_height * max_panel_fraction * 0.5
    
    # Initial bubble size estimate
    half_w = required_width / 2
    half_h = required_height / 2
    cx = panel_width / 2
    cy = panel_height / 2
    
    # Adaptive iteration
    final_iteration = 0
    for iteration in range(max_iterations):
        final_iteration = iteration
        # Create temporary surface to measure free space
        temp_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_width, panel_height)
        temp_ctx = cairo.Context(temp_surface)
        
        circles = create_overlapping_circles_square(
            temp_ctx, cx, cy, half_w * 2, half_h * 2,
            text="", circle_style=style,
            show_full_ovals=False, return_circles=True
        )
        
        # Find free bounding box inside bubble
        free_bbox = find_free_bbox_rect(cx, cy, half_w, half_h, circles)
        free_w, free_h = free_bbox[2], free_bbox[3]
        
        if free_w == 0 or free_h == 0:
            # Too small, grow
            half_w *= 1.2
            half_h *= 1.2
            continue
        
        # Check if free space fits text
        scale_w = required_width / free_w if free_w > 0 else 1.0
        scale_h = required_height / free_h if free_h > 0 else 1.0
        needed_scale = max(scale_w, scale_h)
        
        # Check panel limits
        max_w = panel_width * max_panel_fraction
        max_h = panel_height * max_panel_fraction
        
        projected_w = half_w * 2 * needed_scale
        projected_h = half_h * 2 * needed_scale
        
        if projected_w > max_w or projected_h > max_h:
            # Clamp to panel limits
            scale_limit = min(max_w / (half_w * 2), max_h / (half_h * 2))
            half_w *= scale_limit
            half_h *= scale_limit
            break
        
        # Check convergence
        if 0.92 < needed_scale < 1.08:
            break
        
        # Adjust size
        half_w *= needed_scale
        half_h *= needed_scale
    
    # Create final surface
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, panel_width, panel_height)
    ctx = cairo.Context(surface)
    
    # Set background color if provided
    if background_color is not None:
        if len(background_color) >= 3:
            if len(background_color) == 4:
                ctx.set_source_rgba(*background_color)
            else:
                ctx.set_source_rgb(*background_color)
            ctx.paint()
        else:
            ctx.set_source_rgba(0, 0, 0, 0)
            ctx.paint()
    else:
        ctx.set_source_rgba(0, 0, 0, 0)
        ctx.paint()
    
    # Draw final bubble
    create_overlapping_circles_square(
        ctx, cx, cy, half_w * 2, half_h * 2,
        text=text, circle_style=style,
        show_full_ovals=show_full_ovals,
        background_color=background_color
    )
    
    metadata = {
        'bubble_size': (half_w * 2, half_h * 2),
        'position': (cx, cy),
        'panel_size': (panel_width, panel_height),
        'iterations': final_iteration + 1,
        'panel_fraction': ((half_w * 2) / panel_width, (half_h * 2) / panel_height)
    }
    
    return surface, ctx, metadata


def quick_auto_bubble(panel_size: Tuple[int, int], text: str = "", 
                      style: str = "organic"):
    """
    Quick helper: auto-scale bubble for panel.
    
    Usage:
        surf = quick_auto_bubble((800, 1200), "Hello!", "laugh")
        surf.write_to_png("output.png")
    
    Args:
        panel_size: Tuple of (width, height)
        text: Text content
        style: Bubble style
    
    Returns:
        Cairo ImageSurface
    """
    surface, _, _ = auto_scale_bubble_for_panel(
        panel_size[0], panel_size[1], text, style
    )
    return surface

