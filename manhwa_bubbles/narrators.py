"""
Narrator box functions for manhwa-style comics.
"""

from PIL import ImageDraw, ImageFont


def narrator_plain(draw, xy, text):
    """
    Plain rectangular narration box.
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for box position and size
        text: Text to display in the narration box
    """
    x, y, w, h = xy
    draw.rectangle((x, y, x+w, y+h), fill="white", outline="black", width=2)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


def narrator_borderless(draw, xy, text):
    """
    Borderless floating narration (just text).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for text position and size
        text: Text to display
    """
    x, y, w, h = xy
    font = ImageFont.load_default()
    draw.text((x, y), text, font=font, fill="black")


def narrator_dashed(draw, xy, text):
    """
    Dashed border narration box.
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for box position and size
        text: Text to display in the narration box
    """
    x, y, w, h = xy
    draw.rectangle((x, y, x+w, y+h), fill="white")
    step = 10
    for i in range(x, x+w, step):
        draw.line((i, y, min(i+5, x+w), y), fill="black", width=2)
        draw.line((i, y+h, min(i+5, x+w), y+h), fill="black", width=2)
    for j in range(y, y+h, step):
        draw.line((x, j, x, min(j+5, y+h)), fill="black", width=2)
        draw.line((x+w, j, x+w, min(j+5, y+h)), fill="black", width=2)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")


def narrator_dark(draw, xy, text):
    """
    Dark/ominous narration box.
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for box position and size
        text: Text to display in the narration box
    """
    x, y, w, h = xy
    draw.rectangle((x, y, x+w, y+h), fill="black", outline="white", width=2)
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="white")


def narrator_wavy(draw, xy, text):
    """
    Wavy border narration box (dreamy/unstable).
    
    Args:
        draw: PIL ImageDraw object
        xy: Tuple of (x, y, width, height) for box position and size
        text: Text to display in the narration box
    """
    x, y, w, h = xy
    step = 10
    offset = 0
    path_top, path_bottom = [], []
    for i in range(x, x+w+1, step):
        offset = 5 if (i//step) % 2 == 0 else -5
        path_top.append((i, y+offset))
        path_bottom.append((i, y+h+offset))
    draw.line(path_top, fill="black", width=2)
    draw.line(path_bottom, fill="black", width=2)
    # left and right wavy lines
    path_left, path_right = [], []
    for j in range(y, y+h+1, step):
        offset = 5 if (j//step) % 2 == 0 else -5
        path_left.append((x+offset, j))
        path_right.append((x+w+offset, j))
    draw.line(path_left, fill="black", width=2)
    draw.line(path_right, fill="black", width=2)
    # fill background
    draw.rectangle((x, y, x+w, y+h), fill="white")
    font = ImageFont.load_default()
    draw.text((x+10, y+10), text, font=font, fill="black")