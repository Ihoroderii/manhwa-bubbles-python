"""
Speech bubble functions for manhwa-style comics.
"""

from PIL import Image, ImageDraw, ImageFont
import math

_cairo_available = False
try:
    import cairo as _cairo
    _cairo_available = True
except ImportError:
    pass


def bubble_heart(draw, xy, text):
    """
    Heart-shaped bubble (romantic).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    points = []
    for t in range(0, 360, 5):
        rad = math.radians(t)
        px = x + w//2 + int(16*math.sin(rad)**3 * (w/20))
        py = y + h//2 - int((13*math.cos(rad) - 5*math.cos(2*rad) - 2*math.cos(3*rad) - math.cos(4*rad)) * (h/20))
        points.append((px, py))
    draw.polygon(points, fill="white", outline="red", width=3)
    font = ImageFont.load_default()
    draw.text((x+w//3, y+h//3), text, font=font, fill="red")


def bubble_spiky(draw, xy, text):
    """
    Spiky flame-like bubble (rage).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    points = []
    num_points = 40
    for i in range(num_points):
        angle = 2*math.pi*i/num_points
        r = (w//2) + (20 if i % 2 == 0 else 5)
        px = x+w//2 + int(r*math.cos(angle))
        py = y+h//2 + int(r*math.sin(angle))
        points.append((px, py))
    draw.polygon(points, fill="white", outline="black")
    font = ImageFont.load_default()
    draw.text((x+w//3, y+h//3), text, font=font, fill="black")


def bubble_glow(draw, xy, text):
    """
    Bubble with glowing aura (magic/divine).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    for r in range(0, 20, 4):
        draw.ellipse((x-r, y-r, x+w+r, y+h+r), outline="yellow", width=2)
    draw.ellipse((x, y, x+w, y+h), fill="white", outline="gold", width=3)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


def bubble_scratchy(draw, xy, text):
    """
    Scratchy/rough border bubble (madness/creepy).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
    """
    x, y, w, h = xy
    for i in range(100):
        px1 = x + int(math.cos(i)*w/2) + w//2
        py1 = y + int(math.sin(i)*h/2) + h//2
        px2 = px1 + (math.sin(i*3)*10)
        py2 = py1 + (math.cos(i*5)*10)
        draw.line((px1, py1, px2, py2), fill="black", width=1)
    draw.rectangle((x, y, x+w, y+h), fill="white")
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


def _bezier_point(t, p0, p1, p2, p3):
    """Evaluate cubic Bezier at parameter t."""
    u = 1 - t
    return (
        u*u*u*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t*t*t*p3[0],
        u*u*u*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t*t*t*p3[1],
    )


def draw_tail(draw, x, y, direction="down", length=35, width=22):
    """
    Draws a smooth curved tail using Bezier approximation (PIL fallback).

    Args:
        draw: PIL ImageDraw object
        x, y: Attachment point on the bubble edge
        direction: Direction for the tail ("down", "up", "left", "right")
        length: How far the tail extends
        width: Width of tail at the base
    """
    hw = width / 2
    steps = 12  # number of segments for smooth curve

    if direction == "down":
        left  = (x - hw, y)
        right = (x + hw, y)
        tip   = (x, y + length)
        cp_l  = (x - hw * 0.4, y + length * 0.6)
        cp_r  = (x + hw * 0.4, y + length * 0.6)
    elif direction == "up":
        left  = (x - hw, y)
        right = (x + hw, y)
        tip   = (x, y - length)
        cp_l  = (x - hw * 0.4, y - length * 0.6)
        cp_r  = (x + hw * 0.4, y - length * 0.6)
    elif direction == "left":
        left  = (x, y - hw)
        right = (x, y + hw)
        tip   = (x - length, y)
        cp_l  = (x - length * 0.6, y - hw * 0.4)
        cp_r  = (x - length * 0.6, y + hw * 0.4)
    else:  # right
        left  = (x, y - hw)
        right = (x, y + hw)
        tip   = (x + length, y)
        cp_l  = (x + length * 0.6, y - hw * 0.4)
        cp_r  = (x + length * 0.6, y + hw * 0.4)

    # Build smooth polygon: left edge curve -> tip -> right edge curve back
    points = []
    for i in range(steps + 1):
        t = i / steps
        points.append(_bezier_point(t, left, cp_l, cp_l, tip))
    for i in range(steps, -1, -1):
        t = i / steps
        points.append(_bezier_point(t, right, cp_r, cp_r, tip))

    draw.polygon(points, fill="white", outline="black", width=2)


def draw_tail_cairo(image, x, y, direction="down", length=35, width=22):
    """Draw a smooth curved tail using PyCairo curve_to() and composite
    onto a PIL Image.  Returns the updated image.

    Args:
        image: PIL Image (RGBA)
        x, y: Attachment point on the bubble edge
        direction: "down", "up", "left", "right"
        length: How far the tail extends
        width: Width at the base
    """
    hw = width / 2

    if direction == "down":
        p1 = (x - hw, y)
        p2 = (x + hw, y)
        tip = (x, y + length)
        cp1 = (x - hw * 0.3, y + length * 0.55)
        cp2 = (x + hw * 0.3, y + length * 0.55)
    elif direction == "up":
        p1 = (x - hw, y)
        p2 = (x + hw, y)
        tip = (x, y - length)
        cp1 = (x - hw * 0.3, y - length * 0.55)
        cp2 = (x + hw * 0.3, y - length * 0.55)
    elif direction == "left":
        p1 = (x, y - hw)
        p2 = (x, y + hw)
        tip = (x - length, y)
        cp1 = (x - length * 0.55, y - hw * 0.3)
        cp2 = (x - length * 0.55, y + hw * 0.3)
    else:  # right
        p1 = (x, y - hw)
        p2 = (x, y + hw)
        tip = (x + length, y)
        cp1 = (x + length * 0.55, y - hw * 0.3)
        cp2 = (x + length * 0.55, y + hw * 0.3)

    img_w, img_h = image.size
    surface = _cairo.ImageSurface(_cairo.FORMAT_ARGB32, img_w, img_h)
    ctx = _cairo.Context(surface)

    ctx.move_to(*p1)
    ctx.curve_to(*cp1, *tip, *tip)
    ctx.curve_to(*tip, *cp2, *p2)
    ctx.close_path()

    ctx.set_source_rgba(1, 1, 1, 1)
    ctx.fill_preserve()
    ctx.set_source_rgba(0, 0, 0, 0.95)
    ctx.set_line_width(2.5)
    ctx.stroke()

    tail_pil = Image.frombuffer(
        "RGBA",
        (surface.get_width(), surface.get_height()),
        surface.get_data(),
        "raw", "BGRA", 0, 1,
    )
    image = image.convert("RGBA")
    return Image.alpha_composite(image, tail_pil)


def speech_bubble(draw, xy, text, bubble_type="oval", tail_dir="down",
                  image=None, no_tail=False):
    """
    Draws different manhwa bubble types.
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for bubble position and size
        text: Text to display in the bubble
        bubble_type: Type of bubble ("oval", "rect", "cloud", "jagged", "wavy", "black", "heart", "spiky", "glow", "scratchy")
        tail_dir: Direction for the speech tail ("down", "up", "left", "right")
        image: Optional PIL Image (RGBA) — when provided and Cairo is
               available, the tail will be rendered with PyCairo curve_to().
               Returns the updated image in that case.
        no_tail: If True, skip drawing the tail.
    """
    x, y, w, h = xy
    text_color = "black"  # default

    if bubble_type == "oval":  # normal speech
        draw.ellipse((x, y, x+w, y+h), fill="white", outline="black", width=3)

    elif bubble_type == "rect":  # narration
        draw.rectangle((x, y, x+w, y+h), fill="white", outline="black", width=3)

    elif bubble_type == "cloud":  # thought
        for i in range(12):
            angle = 2*math.pi*i/12
            cx = x+w//2 + int((w//2)*math.cos(angle))
            cy = y+h//2 + int((h//2)*math.sin(angle))
            draw.ellipse((cx-15, cy-15, cx+15, cy+15), fill="white", outline="black")
        draw.ellipse((x, y, x+w, y+h), fill="white", outline="black")

    elif bubble_type == "jagged":  # shouting
        points = []
        num_points = 20
        for i in range(num_points):
            angle = 2*math.pi*i/num_points
            r = (w//2) + (15 if i % 2 == 0 else 5)
            px = x+w//2 + int(r*math.cos(angle))
            py = y+h//2 + int(r*math.sin(angle))
            points.append((px, py))
        draw.polygon(points, fill="white", outline="black")

    elif bubble_type == "wavy":  # nervous/shaky
        steps = 20
        path = []
        for i in range(steps+1):
            px = x + (w*i)//steps
            py = y + (h//2) + int(10*math.sin(i*0.8))
            path.append((px, py))
        draw.line(path, fill="black", width=3)
        draw.rectangle((x, y, x+w, y+h), fill="white")  # simple white box inside

    elif bubble_type == "black":  # evil/dark intent
        draw.ellipse((x, y, x+w, y+h), fill="black", outline="white", width=3)
        text_color = "white"
        
    elif bubble_type == "heart":  # romantic
        bubble_heart(draw, xy, text)
        return  # heart bubble handles its own text
        
    elif bubble_type == "spiky":  # rage/flame
        bubble_spiky(draw, xy, text)
        return  # spiky bubble handles its own text
        
    elif bubble_type == "glow":  # magic/divine
        bubble_glow(draw, xy, text)
        return  # glow bubble handles its own text
        
    elif bubble_type == "scratchy":  # madness/creepy
        bubble_scratchy(draw, xy, text)
        return  # scratchy bubble handles its own text

    # Tail (skip for special bubbles that handle their own rendering)
    if not no_tail and bubble_type not in ["rect", "wavy", "heart", "spiky", "glow", "scratchy"]:
        if _cairo_available and image is not None:
            image = draw_tail_cairo(image, x + w // 2, y + h,
                                    direction=tail_dir)
        else:
            draw_tail(draw, x + w // 2, y + h, direction=tail_dir)

    # Add text (skip for special bubbles that handle their own text)
    if bubble_type not in ["heart", "spiky", "glow", "scratchy"]:
        font = ImageFont.load_default()
        # Simple word-wrap and center text inside the bubble
        max_text_w = w - 20
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test = (current_line + " " + word).strip()
            bbox = font.getbbox(test) if hasattr(font, 'getbbox') else (0, 0) + font.getsize(test)
            tw = bbox[2] - bbox[0]
            if tw > max_text_w and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test
        if current_line:
            lines.append(current_line)
        line_h = 12
        total_h = len(lines) * line_h
        start_y = y + (h - total_h) // 2
        for i, line in enumerate(lines):
            bbox = font.getbbox(line) if hasattr(font, 'getbbox') else (0, 0) + font.getsize(line)
            tw = bbox[2] - bbox[0]
            tx = x + (w - tw) // 2
            draw.text((tx, start_y + i * line_h), line, font=font, fill=text_color)

    return image