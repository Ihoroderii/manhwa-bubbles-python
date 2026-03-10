"""Extended bubble styles collection.

Implements or stubs a large catalog of stylistic speech / narration / effect bubbles.
All functions draw into a Pillow ImageDraw interface.

Conventions:
- Each function name: bubble_<descriptor>
- Return value: None (draws in-place) OR returns bounding info where useful.
- All accept (draw, xy, text, **opts) where xy = (x, y, w, h)

NOTE: Some advanced visual effects (glow, blur, transparency) are simplified
since Pillow's ImageDraw lacks native blur; user may post-process.

Existing base styles (already provided elsewhere) are NOT redefined here
(e.g., bubble_spiky, bubble_heart). New or variant implementations provided.

Styles covered (numbers follow catalog described previously):
1 standard_oval (already via speech_bubble)
2 wide_soft
3 tall_narrow
4 whisper_dotted
5 shout_burst
6 shock_mini_spike
7 rage_flame (variant over shout)
8 laugh_bouncy (Pillow version)
9 giggle_soft
10 cry_drip
11 nervous_wobble
12 sarcastic_geometric
13 thought_cloud_chain (alias of thought cloud pattern)
14 inner_monologue
15 narration_box (already via narrator)
16 whisper_thought (hybrid)
17 black (existing)
18 inverted_aura
19 scratchy (existing)
20 dripping_horror
21 magic_glow_frame
22 arcane_glyph
23 telepathy_wave
24 ghost_translucent
25 static_electric
26 digital_system
27 radio_comms
28 robotic_panel
29 ai_card
30 impact_bang
31 sfx_capsule
32 chain_overlap_sequence
33 trailing_sequence
34 echo_layers
35 fragmented_arc
36 breath_cold
37 sleepy_slump
38 drunk_slur
39 hypnotic_spiral
40 chant_choral
41 text_only
42 bracketed_text
43 bold_plate
44 organic_overlapping (provided by Cairo variant; here we just supply a stub wrapper)
"""
from PIL import ImageDraw, ImageFont
import math, random

DEFAULT_FONT = ImageFont.load_default()

# Utility helpers -------------------------------------------------

def _center_text(draw, x, y, w, h, text, font, fill):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((x + (w - tw)/2, y + (h - th)/2), text, font=font, fill=fill)

def _jitter_points(base_points, amp):
    return [(px + random.uniform(-amp, amp), py + random.uniform(-amp, amp)) for px, py in base_points]

# 2. Wide soft ----------------------------------------------------

def bubble_wide_soft(draw, xy, text, softness=14, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    # Horizontal stretching with bezier-ish approximation using many points
    steps = 40
    pts = []
    for i in range(steps+1):
        t = i/steps
        ang = math.pi * t
        # ellipse param with horizontal scaling
        px = x + w/2 + (w/2)*math.cos(ang)
        py = y + h/2 + (h/2 - softness)*math.sin(ang)
        pts.append((px, py))
    # mirror bottom
    for i in range(steps, -1, -1):
        t = i/steps
        ang = math.pi * t
        px = x + w/2 + (w/2)*math.cos(ang)
        py = y + h/2 + (h/2 + softness)*math.sin(-ang)
        pts.append((px, py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw, x,y,w,h,text,font,fill="black")

# 3. Tall narrow --------------------------------------------------

def bubble_tall_narrow(draw, xy, text, squeeze=0.6, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    rx = w/2 * squeeze
    ry = h/2
    pts = []
    steps = 60
    for i in range(steps+1):
        ang = 2*math.pi*i/steps
        px = x + w/2 + rx*math.cos(ang)
        py = y + h/2 + ry*math.sin(ang)
        pts.append((px,py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 4. Whisper dotted -----------------------------------------------

def bubble_whisper_dotted(draw, xy, text, dash=9, outline="black", fill=None, font=DEFAULT_FONT):
    x,y,w,h = xy
    rx, ry = w/2, h/2
    steps = 90
    dots = []
    for i in range(steps):
        ang = 2*math.pi*i/steps
        if i % dash != 0:
            continue
        px = x + w/2 + rx*math.cos(ang)
        py = y + h/2 + ry*math.sin(ang)
        # small circle = represented as a point -> draw line zero length
        draw.line((px,py,px+1,py+1), fill=outline, width=1)
    if fill:
        draw.ellipse((x,y,x+w,y+h), outline=None, width=0, fill=fill)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 5. Shout burst --------------------------------------------------

def bubble_shout_burst(draw, xy, text, spikes=24, r_extra=18, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx, cy = x+w/2, y+h/2
    base_r = max(w,h)/2 - 4
    pts = []
    for i in range(spikes):
        ang = 2*math.pi*i/spikes
        r = base_r + (r_extra if i%2==0 else 2)
        px = cx + r*math.cos(ang)
        py = cy + r*math.sin(ang)
        pts.append((px,py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 6. Shock mini spike ---------------------------------------------

def bubble_shock_mini_spike(draw, xy, text, spikes=12, amp=8, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx, cy = x+w/2, y+h/2
    r = max(w,h)/2 - 6
    pts=[]
    for i in range(spikes):
        ang = 2*math.pi*i/spikes
        rr = r + (amp if i%2==0 else 0)
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 7. Rage flame ---------------------------------------------------

def bubble_rage_flame(draw, xy, text, tongues=26, base_push=10, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx, cy = x+w/2, y+h/2
    r = max(w,h)/2 - 8
    pts=[]
    for i in range(tongues):
        ang = 2*math.pi*i/tongues
        mod = 1 + 0.4*math.sin(i*1.3) + random.uniform(-0.1,0.1)
        rr = r * mod + (base_push if i%3==0 else 0)
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 8. Laugh bouncy -------------------------------------------------

def bubble_laugh_bouncy(draw, xy, text, bumps=3, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx, cy = x+w/2, y+h/2
    base_r = max(w,h)/2 - 4
    steps = 120
    pts=[]
    for i in range(steps):
        ang = 2*math.pi*i/steps
        # small frequency ripple
        ripple = 1 + 0.08*math.sin(ang*bumps*2) + 0.04*math.sin(ang*bumps*3)
        rr = base_r * ripple
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    # energy ticks
    for _ in range(12):
        ang = random.uniform(0,2*math.pi)
        sr = base_r*1.05
        er = sr + random.uniform(8,20)
        sx = cx + sr*math.cos(ang)
        sy = cy + sr*math.sin(ang)
        ex = cx + er*math.cos(ang)
        ey = cy + er*math.sin(ang)
        draw.line((sx,sy,ex,ey), fill=outline, width=2)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 9. Giggle soft --------------------------------------------------

def bubble_giggle_soft(draw, xy, text, waviness=6, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx,cy = x+w/2,y+h/2
    r = max(w,h)/2 - 5
    steps=100
    pts=[]
    for i in range(steps):
        ang = 2*math.pi*i/steps
        rr = r + 3*math.sin(ang*waviness)
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 10. Cry drip ----------------------------------------------------

def bubble_cry_drip(draw, xy, text, drips=4, max_len=20, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    # drips bottom region
    for _ in range(drips):
        dx = x + w/2 + random.uniform(-w*0.35, w*0.35)
        dy1 = y + h
        dy2 = dy1 + random.uniform(max_len*0.3, max_len)
        draw.line((dx,dy1,dx,dy2), fill=outline, width=2)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 11. Nervous wobble ----------------------------------------------

def bubble_nervous_wobble(draw, xy, text, jitter=4, steps=70, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx,cy = x+w/2,y+h/2
    rx, ry = w/2 - 4, h/2 - 4
    pts=[]
    for i in range(steps):
        ang = 2*math.pi*i/steps
        px = cx + rx*math.cos(ang) + random.uniform(-jitter,jitter)
        py = cy + ry*math.sin(ang) + random.uniform(-jitter,jitter)
        pts.append((px,py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 12. Sarcastic geometric -----------------------------------------

def bubble_sarcastic_geometric(draw, xy, text, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    pad = 4
    draw.rectangle((x,y,x+w,y+h), outline=outline, fill=fill, width=2)
    _center_text(draw,x+pad,y+pad,w-2*pad,h-2*pad,text,font,fill="black")

# 13. Thought cloud chain -----------------------------------------

def bubble_thought_cloud_chain(draw, xy, text, puffs=10, puff_r=12, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    cx,cy = x+w/2,y+h/2
    # main ellipse
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    for i in range(puffs):
        ang = 2*math.pi*i/puffs
        pr = puff_r * (0.7 + 0.3*math.sin(i))
        px = cx + (w/2 - pr/2)*math.cos(ang)
        py = cy + (h/2 - pr/2)*math.sin(ang)
        draw.ellipse((px-pr,py-pr,px+pr,py+pr), fill=fill, outline=outline)
    # small chain tail
    for k in range(3):
        rr = puff_r*(0.6 - k*0.15)
        tx = x + w*0.75 + k*8
        ty = y + h + 10 + k*12
        draw.ellipse((tx-rr,ty-rr,tx+rr,ty+rr), fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 14. Inner monologue ---------------------------------------------

def bubble_inner_monologue(draw, xy, text, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    draw.rounded_rectangle((x,y,x+w,y+h), radius=12, outline=outline, fill=fill, width=2)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 16. Whisper thought hybrid --------------------------------------

def bubble_whisper_thought(draw, xy, text, outline="black", fill="white", font=DEFAULT_FONT):
    # dotted outer + cloud inside
    x,y,w,h = xy
    bubble_whisper_dotted(draw, xy, text="", dash=7, outline=outline, fill=None, font=font)
    draw.ellipse((x+6,y+6,x+w-6,y+h-6), fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 18. Inverted aura ------------------------------------------------

def bubble_inverted_aura(draw, xy, text, rings=3, outline="white", fill="black", font=DEFAULT_FONT):
    x,y,w,h = xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline, width=2)
    for r in range(1,rings+1):
        pad = r*6
        draw.ellipse((x-pad,y-pad,x+w+pad,y+h+pad), outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="white")

# 20. Dripping horror ---------------------------------------------

def bubble_dripping_horror(draw, xy, text, drips=8, max_len=26, outline="black", fill="black", font=DEFAULT_FONT):
    x,y,w,h = xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    for _ in range(drips):
        dx = x + random.uniform(0,w)
        dy1 = y + h
        dy2 = dy1 + random.uniform(max_len*0.4, max_len)
        draw.line((dx,dy1,dx,dy2), fill=outline, width=3)
    _center_text(draw,x,y,w,h,text,font,fill="white")

# 21. Magic glow frame --------------------------------------------

def bubble_magic_glow_frame(draw, xy, text, rings=4, outline="gold", fill="white", font=DEFAULT_FONT):
    x,y,w,h = xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline, width=3)
    for r in range(1,rings+1):
        pad = r*4
        draw.ellipse((x-pad,y-pad,x+w+pad,y+h+pad), outline="yellow")
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 22. Arcane glyph -------------------------------------------------

def bubble_arcane_glyph(draw, xy, text, segments=12, outline="purple", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline, width=2)
    cx,cy = x+w/2,y+h/2
    r = max(w,h)/2 + 10
    for i in range(segments):
        ang = 2*math.pi*i/segments
        px = cx + r*math.cos(ang)
        py = cy + r*math.sin(ang)
        draw.line((cx,cy,px,py), fill=outline, width=1)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 23. Telepathy wave ----------------------------------------------

def bubble_telepathy_wave(draw, xy, text, waves=3, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    cx,cy = x+w/2,y+h/2
    for wv in range(1,waves+1):
        pad = wv*10
        draw.ellipse((cx-pad, cy-pad, cx+pad, cy+pad), outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 24. Ghost translucent -------------------------------------------

def bubble_ghost_translucent(draw, xy, text, outline="black", fill="white", alpha=160, font=DEFAULT_FONT):
    # For real translucency user should composite RGBA; here we approximate by using lighter fill
    x,y,w,h=xy
    gray = (240,240,255)
    draw.ellipse((x,y,x+w,y+h), fill=gray, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 25. Static electric ---------------------------------------------

def bubble_static_electric(draw, xy, text, sparks=14, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    cx,cy = x+w/2,y+h/2
    for _ in range(sparks):
        ang = random.uniform(0,2*math.pi)
        inner = min(w,h)/2
        outer = inner + random.uniform(8,18)
        sx = cx + inner*math.cos(ang)
        sy = cy + inner*math.sin(ang)
        ex = cx + outer*math.cos(ang)
        ey = cy + outer*math.sin(ang)
        draw.line((sx,sy,ex,ey), fill=outline, width=1)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 26. Digital system ----------------------------------------------

def bubble_digital_system(draw, xy, text, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    # pixel-like corners
    draw.rectangle((x,y,x+w,y+h), fill=fill, outline=outline, width=2)
    # corner squares
    sq=6
    for cxp,cyp in [(x,y),(x+w-sq,y),(x,y+h-sq),(x+w-sq,y+h-sq)]:
        draw.rectangle((cxp,cyp,cxp+sq,cyp+sq), fill=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 27. Radio comms -------------------------------------------------

def bubble_radio_comms(draw, xy, text, bars=4, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.rounded_rectangle((x,y,x+w,y+h), radius=6, outline=outline, fill=fill, width=2)
    # signal bars right side
    bx = x+w-10
    for i in range(bars):
        top = y + h - 6 - i*6
        draw.line((bx, top, bx, y+h-6), fill=outline, width=2)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 28. Robotic panel -----------------------------------------------

def bubble_robotic_panel(draw, xy, text, outline="black", fill="white", bevel=6, font=DEFAULT_FONT):
    x,y,w,h=xy
    # octagon-like shape
    pts=[(x+bevel,y),(x+w-bevel,y),(x+w,y+bevel),(x+w,y+h-bevel),(x+w-bevel,y+h),(x+bevel,y+h),(x,y+h-bevel),(x,y+bevel)]
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 29. AI card ------------------------------------------------------

def bubble_ai_card(draw, xy, text, outline="#333", fill="#f5f5f5", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.rounded_rectangle((x,y,x+w,y+h), radius=10, outline=outline, fill=fill, width=2)
    # small header bar
    draw.rectangle((x,y,x+w,y+10), fill="#ddd")
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 30. Impact bang -------------------------------------------------

def bubble_impact_bang(draw, xy, text, spikes=14, amp=30, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    cx,cy = x+w/2,y+h/2
    base = max(w,h)/2 - 8
    pts=[]
    for i in range(spikes):
        ang = 2*math.pi*i/spikes
        rr = base + (amp if i%2==0 else 4)
        pts.append((cx+rr*math.cos(ang), cy+rr*math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 31. SFX capsule --------------------------------------------------

def bubble_sfx_capsule(draw, xy, text, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    r = h/2
    draw.rounded_rectangle((x,y,x+w,y+h), radius=int(r), outline=outline, fill=fill, width=2)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 32. Chain overlap sequence --------------------------------------

def bubble_chain_overlap_sequence(draw, bubbles, outline="black", fill="white", font=DEFAULT_FONT):
    """Draw a list of (xy, text) overlapping slightly to indicate rapid exchange.
    bubbles: list of ((x,y,w,h), text)
    """
    offset = 0
    for (xy,text) in bubbles:
        x,y,w,h = xy
        x_adj = x + offset
        draw.ellipse((x_adj,y,x_adj+w,y+h), fill=fill, outline=outline)
        _center_text(draw,x_adj,y,w,h,text,font,fill="black")
        offset += int(w*0.25)

# 33. Trailing sequence -------------------------------------------

def bubble_trailing_sequence(draw, bubbles, outline="black", fill="white", font=DEFAULT_FONT):
    """Draw bubbles decreasing in size for trailing thought/speech."""
    scale = 1.0
    for (xy,text) in bubbles:
        x,y,w,h = xy
        w2,h2 = w*scale, h*scale
        draw.ellipse((x,y,x+w2,y+h2), fill=fill, outline=outline)
        _center_text(draw,x,y,w2,h2,text,font,fill="black")
        scale *= 0.78

# 34. Echo layers --------------------------------------------------

def bubble_echo_layers(draw, xy, text, layers=3, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    for i in range(1,layers+1):
        pad = i*6
        draw.ellipse((x-pad,y-pad,x+w+pad,y+h+pad), outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 35. Fragmented arc -----------------------------------------------

def bubble_fragmented_arc(draw, xy, text, segments=90, keep_ratio=0.6, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    rx, ry = w/2, h/2
    cx, cy = x+rx, y+ry
    pts=[]
    for i in range(segments):
        if random.random() > keep_ratio:
            continue
        ang = 2*math.pi*i/segments
        px = cx + rx*math.cos(ang)
        py = cy + ry*math.sin(ang)
        pts.append((px,py))
    # draw small segments
    for (px,py) in pts:
        draw.line((px,py,px+1,py+1), fill=outline)
    if fill:
        draw.ellipse((x,y,x+w,y+h), fill=fill)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 36. Breath cold --------------------------------------------------

def bubble_breath_cold(draw, xy, text, puffs=3, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    # trailing vapor bottom-right
    for i in range(puffs):
        r = 8 - i*2
        draw.ellipse((x+w + i*10, y+h*0.6 + i*6, x+w + i*10 + r, y+h*0.6 + i*6 + r), outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 37. Sleepy slump -------------------------------------------------

def bubble_sleepy_slump(draw, xy, text, slump=8, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    # Lower the top center a bit to look droopy
    steps=80
    cx,cy = x+w/2,y+h/2
    rx,ry=w/2,h/2
    pts=[]
    for i in range(steps):
        ang = 2*math.pi*i/steps
        dy_extra = -slump if (0 < ang < math.pi) else 0
        px = cx + rx*math.cos(ang)
        py = cy + ry*math.sin(ang) + dy_extra
        pts.append((px,py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 38. Drunk slur ---------------------------------------------------

def bubble_drunk_slur(draw, xy, text, wobble=5, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    steps=70
    cx,cy=x+w/2,y+h/2
    rx,ry=w/2,h/2
    pts=[]
    for i in range(steps):
        ang=2*math.pi*i/steps
        rr = 1 + 0.08*math.sin(ang*3) + random.uniform(-0.05,0.05)
        px = cx + rx*rr*math.cos(ang)
        py = cy + ry*rr*math.sin(ang) + random.uniform(-wobble,wobble)
        pts.append((px,py))
    draw.polygon(pts, fill=fill, outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 39. Hypnotic spiral ----------------------------------------------

def bubble_hypnotic_spiral(draw, xy, text, turns=4, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    cx,cy = x+w/2,y+h/2
    # spiral path
    steps=200
    last=None
    for i in range(steps):
        t = i/steps
        ang = turns*2*math.pi*t
        r = (min(w,h)/2 - 6)*t
        px = cx + r*math.cos(ang)
        py = cy + r*math.sin(ang)
        if last:
            draw.line((last[0],last[1],px,py), fill=outline)
        last=(px,py)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 40. Chant choral -------------------------------------------------

def bubble_chant_choral(draw, xy, text, rings=5, outline="black", fill="white", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.ellipse((x,y,x+w,y+h), fill=fill, outline=outline)
    cx,cy=x+w/2,y+h/2
    for i in range(1,rings+1):
        pad = i*5
        draw.ellipse((cx-pad, cy-pad, cx+pad, cy+pad), outline=outline)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 41. Text only ----------------------------------------------------

def bubble_text_only(draw, xy, text, font=DEFAULT_FONT, fill="black"):
    x,y,w,h=xy
    _center_text(draw,x,y,w,h,text,font,fill)

# 42. Bracketed text ----------------------------------------------

def bubble_bracketed_text(draw, xy, text, font=DEFAULT_FONT, fill="black"):
    x,y,w,h=xy
    decorated = f"[{text}]"
    _center_text(draw,x,y,w,h,decorated,font,fill)

# 43. Bold plate ---------------------------------------------------

def bubble_bold_plate(draw, xy, text, outline="black", fill="#fffdd0", font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.rectangle((x,y,x+w,y+h), fill=fill, outline=outline, width=3)
    _center_text(draw,x,y,w,h,text,font,fill="black")

# 44. Organic overlapping stub ------------------------------------

def bubble_organic_overlapping_stub(draw, xy, text, note=True, font=DEFAULT_FONT):
    x,y,w,h=xy
    draw.rectangle((x,y,x+w,y+h), outline="black", fill="white")
    msg = text if not note else text+" [Use Cairo generate_overlapping_bubble()]"
    _center_text(draw,x,y,w,h,msg,font,fill="black")
