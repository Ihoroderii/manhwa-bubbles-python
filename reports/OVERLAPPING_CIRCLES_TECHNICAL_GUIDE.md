# Overlapping Circles Algorithm - Technical Documentation

**File**: `examples/experiments/overlapping_circles_squares.py`  
**Purpose**: Professional manga-style speech bubble generation using overlapping ovals  
**Algorithm Complexity**: Advanced geometric constraint solving with pixel-precise rendering  
**Last Updated**: 2026-01-25

---

## Table of Contents

1. [Overview](#overview)
2. [Core Concept](#core-concept)
3. [Algorithm Architecture](#algorithm-architecture)
4. [Mathematical Foundations](#mathematical-foundations)
5. [Key Functions Deep Dive](#key-functions-deep-dive)
6. [Configuration Modes](#configuration-modes)
7. [Geometric Constraints](#geometric-constraints)
8. [Advanced Features](#advanced-features)
9. [Usage Examples](#usage-examples)
10. [Performance Considerations](#performance-considerations)

---

## Overview

The `overlapping_circles_squares.py` file implements a sophisticated algorithm for creating **professional manga-style speech bubbles** using a rectangle with strategically placed overlapping ovals on all four sides.

### What It Creates

```
Visual Representation:

         ╭─○──○─╮     ← Top ovals (2)
        ○│      │○    ← Side ovals (left/right)
        ○│ TEXT │○    ← Overlapping strategically
         ╰─○──○─╯     ← Bottom ovals (2)
           ↑
      Clear interior space for text
```

### Key Features

- ✅ **Organic, hand-drawn appearance** (not perfect geometric shapes)
- ✅ **Strategic overlaps** create visual depth and professional manga look
- ✅ **Clear interior space** for text placement
- ✅ **Automatic sizing** based on rectangle dimensions
- ✅ **Guaranteed corner intersections** through constraint enforcement
- ✅ **Multiple style presets** (varied, organic, laugh)
- ✅ **Pixel-precise rendering** for minimal manga style

---

## Core Concept

### The Problem

Traditional speech bubbles are either:
1. **Too geometric** (perfect circles/rectangles) → looks computer-generated
2. **Too random** (hand-drawn simulation) → inconsistent, hard to control

### The Solution

Use **constrained randomness**:
- Place ovals at mathematically determined positions
- Enforce strict geometric constraints (overlaps, penetration depth)
- Add subtle random variation for organic appearance
- Guarantee structural integrity (no gaps, proper connections)

### Design Philosophy

```
Mathematical Precision + Controlled Randomness = Professional Manga Look
     ↓                        ↓                           ↓
  Guaranteed overlaps    Size variation            Natural appearance
  Corner connections     Position jitter           Hand-drawn feel
  No opposite-side       Irregular spacing         Organic curves
  intersection
```

---

## Algorithm Architecture

### Main Function

```python
def create_overlapping_circles_square(ctx, cx, cy, base_width, base_height,
                                      text="OVERLAP!", 
                                      circle_style="varied", 
                                      show_full_ovals=True,
                                      return_circles=False, 
                                      background_color=None)
```

**Parameters**:
- `ctx` - Cairo drawing context
- `cx, cy` - Center coordinates of bubble
- `base_width, base_height` - Rectangle dimensions
- `text` - Text to display (if DRAW_TEXT enabled)
- `circle_style` - "varied", "organic", or "laugh"
- `show_full_ovals` - True: full ovals, False: minimal manga style
- `return_circles` - Return circle data instead of rendering
- `background_color` - For adaptive energy line coloring

### Algorithm Flow (5 Main Steps)

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: Generate Side Ovals                                 │
│   • Calculate number of ovals per side (1 or 2)            │
│   • Position ovals at strategic locations                   │
│   • Size ovals to avoid center intersection                 │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 2: Enforce Corner Overlaps                             │
│   • Check all 4 corners for adjacent-side overlaps          │
│   • Enlarge radii if overlaps missing                       │
│   • Guarantee continuous perimeter                          │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 3: Draw Base & Optional Full Ovals                     │
│   • Draw rectangle (may be hidden in minimal mode)          │
│   • Draw connection lines to exterior intersections         │
│   • Optionally draw full ovals with gradients               │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 4: Fill Interior Gaps (Optional)                       │
│   • Identify gaps between ovals                             │
│   • Fill ONLY the gaps (not entire rectangle)               │
│   • Creates negative space effect                           │
└─────────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│ Step 5: Emphasize Crossing Arcs (Minimal Mode)              │
│   • Find pixels where ovals cross rectangle border          │
│   • Group consecutive crossing pixels                       │
│   • Draw thick lines ONLY at crossings                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Mathematical Foundations

### Oval Placement Strategy

#### Rule 1: Side-Based Oval Count

```python
if side_length > threshold:
    num_ovals = 2  # Long sides get 2 ovals
else:
    num_ovals = 1  # Short sides get 1 oval
```

**Rationale**: 
- Long sides need more ovals to maintain organic curvature
- Short sides with 1 centered oval look natural

#### Rule 2: Penetration Depth

```python
PENETRATION_RATIO_SINGLE = 0.22  # 22% of smaller dimension
PENETRATION_RATIO_DOUBLE = 0.18  # 18% for each of 2 ovals
```

**Visual**:
```
Rectangle edge
      │
      │  ←22%→
      ├────○────  Oval penetrates inward
      │          but NOT to center
      │
    Center
```

**Why**: Too deep → ovals meet in center (no text space)  
**Why**: Too shallow → disconnected from rectangle

#### Rule 3: Same-Side Overlap Requirement

```python
SAME_SIDE_REQUIRED_OVERLAP = 0.28  # 28% of side length

# For two ovals on same side:
overlap_length = 2 * radius - center_separation
if overlap_length < required_minimum:
    enlarge_radius()
```

**Visual**:
```
Side of rectangle
───────────────────
   ○     ○         ← No overlap (BAD)
───────────────────

   ○○   ○○         ← Overlap! (GOOD)
───────────────────
```

#### Rule 4: Opposite-Side Avoidance

```python
# Horizontal sides: wide along edge, shallow into rectangle
if is_horizontal:
    rx = half_width * 0.74    # Wide
    ry = half_height * 0.28   # Shallow

# Vertical sides: tall along edge, narrow into rectangle  
else:
    rx = half_width * 0.28    # Narrow
    ry = half_height * 0.74   # Tall
```

**Visual**:
```
         Top oval (wide, shallow)
           ╭───○───╮
          │         │
Left oval │  TEXT   │ Right oval
(tall,    │  SPACE  │ (tall,
narrow)   │         │ narrow)
          │         │
           ╰───○───╯
         Bottom oval (wide, shallow)
```

**Why**: Prevents top/bottom ovals from touching center  
**Why**: Prevents left/right ovals from touching center  
**Result**: Clear rectangular text area preserved

### Corner Overlap Enforcement

#### Problem

Auto-generated ovals might not overlap at corners:

```
Corner gap example:

    │        ← Right side oval
    │○
────────    ← Bottom edge
  ○         ← Bottom oval
    ↑
   GAP! (disconnected border)
```

#### Solution

```python
def enforce_corner_overlaps(all_circles, cx, cy, half_width, half_height):
    # For each of 4 corners:
    for corner in ["top-left", "top-right", "bottom-right", "bottom-left"]:
        # Find closest oval from each adjacent side
        oval_a = find_closest_oval_to_corner(side_1, corner)
        oval_b = find_closest_oval_to_corner(side_2, corner)
        
        # Check axis-aligned overlap
        dx = abs(oval_a.x - oval_b.x)
        dy = abs(oval_a.y - oval_b.y)
        
        # Horizontal overlap check
        if dx > (oval_a.rx + oval_b.rx - MARGIN):
            needed = dx + MARGIN - (oval_a.rx + oval_b.rx)
            enlarge_smaller_rx(needed)
        
        # Vertical overlap check
        if dy > (oval_a.ry + oval_b.ry - MARGIN):
            needed = dy + MARGIN - (oval_a.ry + oval_b.ry)
            enlarge_smaller_ry(needed)
```

**Result**:
```
After enforcement:

    │
    │○╮      ← Ovals now overlap!
────────●─
    ○╯

(Continuous border at corner)
```

---

## Key Functions Deep Dive

### 1. `generate_side_circles()` (Lines 94-132)

**Purpose**: Generate ovals for all 4 sides of rectangle

**Algorithm**:
```python
def generate_side_circles(cx, cy, half_width, half_height, style):
    all_circles = []
    
    # Define 4 sides with start/end coordinates
    sides = [
        ("top", x1, y1, x2, y2),
        ("right", x1, y1, x2, y2),
        ("bottom", x1, y1, x2, y2),
        ("left", x1, y1, x2, y2)
    ]
    
    for side_name, start_x, start_y, end_x, end_y in sides:
        # Calculate side length
        side_length = distance(start, end)
        
        # Determine oval count (1 or 2)
        if is_long_side:
            num_circles = 2
        else:
            num_circles = 1
        
        # Generate ovals for this side
        side_circles = generate_circles_for_side(
            start_x, start_y, end_x, end_y, 
            side_name, style, num_circles, ...
        )
        
        all_circles.extend(side_circles)
    
    return all_circles
```

**Output**: List of circle dictionaries:
```python
[
    {
        'x': 250.3,      # Center X
        'y': 180.7,      # Center Y
        'rx': 85.2,      # Radius X
        'ry': 33.5,      # Radius Y
        'side': 'top',   # Which side
        'id': 0          # Unique ID
    },
    ...
]
```

### 2. `generate_circles_for_side()` (Lines 216-370)

**Purpose**: Generate ovals for ONE side with precise constraints

**Key Logic**:

#### A. Position Calculation

```python
# For single oval: center with jitter
if num_circles == 1:
    t = 0.5 + random.uniform(-0.08, 0.08)

# For two ovals: near corners
else:
    if i == 0:
        t = 0.18 + random.uniform(-0.05, 0.05)  # Near start
    else:
        t = 0.82 + random.uniform(-0.05, 0.05)  # Near end

# Calculate position along side
side_x = start_x + t * (end_x - start_x)
side_y = start_y + t * (end_y - start_y)
```

**Why random jitter**: Creates organic variation while staying within bounds

#### B. Outward Normal Calculation

```python
# Calculate direction pointing OUT from rectangle
if side_name == "top":
    normal_x, normal_y = 0, -1   # Point upward
elif side_name == "bottom":
    normal_x, normal_y = 0, 1    # Point downward
elif side_name == "left":
    normal_x, normal_y = -1, 0   # Point left
else:  # right
    normal_x, normal_y = 1, 0    # Point right
```

**Used for**: Positioning oval center outside rectangle edge

#### C. Radii Calculation

```python
# Horizontal sides (top/bottom)
if is_horizontal:
    base_span = 0.74 if single else 0.46 + random()
    
    rx = (half_width * base_span) * random(0.94, 1.05)
    ry = (half_height * 0.28) * random(0.92, 1.08)
    
    # rx: Wide along edge for corner reach
    # ry: Shallow to avoid center collision

# Vertical sides (left/right)
else:
    base_span = 0.74 if single else 0.46 + random()
    
    rx = (half_width * 0.28) * random(0.92, 1.08)
    ry = (half_height * base_span) * random(0.94, 1.05)
    
    # rx: Narrow to avoid center collision
    # ry: Tall along edge for corner reach
```

**Corner bias adjustment**:
```python
corner_bias = (num_circles >= 2 and (t < 0.3 or t > 0.7))
if corner_bias:
    base_span *= 0.9  # Shrink corner ovals → sharper gaps
```

#### D. Style Variations

**Laugh Style** (more chaotic):
```python
if style == "laugh":
    # More ovals on long sides
    if side_length > 140:
        num_circles = 3  # Instead of 2
    
    # Smaller, punchier bumps
    rx *= 0.78 * random(0.95, 1.08)
    ry *= 0.78 * random(0.95, 1.08)
    
    # Random exaggeration for energy
    if random() < 0.4:
        if is_horizontal:
            ry *= random(1.05, 1.18)  # Taller bulge
```

#### E. Same-Side Overlap Guarantee

```python
if num_circles >= 2:
    # Calculate current overlap
    center_separation = 0.6 * side_length  # Distance between centers
    current_overlap = 2 * along_radius - center_separation
    
    # Check minimum requirement
    min_required = SAME_SIDE_REQUIRED_OVERLAP * side_length
    
    if current_overlap < min_required:
        # Enlarge radius to meet requirement
        required_radius = (center_separation + min_required) / 2.0
        scale_factor = required_radius / along_radius
        
        if is_horizontal:
            rx *= scale_factor
        else:
            ry *= scale_factor
```

#### F. Penetration Depth

```python
if is_horizontal:
    # Horizontal penetration
    penetration = half_height * PENETRATION_RATIO
else:
    # Vertical penetration
    penetration = half_width * PENETRATION_RATIO

# Offset center inward by penetration amount
circle_x = side_x + normal_x * penetration
circle_y = side_y + normal_y * penetration
```

**Result**: Oval center is positioned just inside rectangle edge

### 3. `emphasize_border_crossing_pixels()` (Lines 750-839)

**Purpose**: Find exact pixels where oval borders intersect rectangle edges

**Why Needed**: For minimal manga style - only show the curved intersection arcs

**Algorithm**:

#### Step 1: Sample Oval Perimeter

```python
def find_crossing_pixels(circle, square_bounds):
    crossing_pixels = []
    
    # Sample 360 points around oval (1 degree intervals)
    for angle_deg in range(360):
        angle_rad = math.radians(angle_deg)
        
        # Calculate point on oval perimeter
        px = circle['x'] + circle['rx'] * math.cos(angle_rad)
        py = circle['y'] + circle['ry'] * math.sin(angle_rad)
        
        # Check if point is near rectangle border
        # (within 1.5 pixels tolerance)
        
        # Left border check
        if abs(px - square_left) < 1.5 and \
           square_top <= py <= square_bottom:
            crossing_pixels.append({
                'x': px, 'y': py, 
                'border': 'left',
                'circle_id': circle['id']
            })
        
        # Repeat for right, top, bottom borders...
    
    return crossing_pixels
```

**Precision**: 1 degree = ~6.28 samples per oval → sub-pixel accuracy

#### Step 2: Group Consecutive Pixels

```python
def group_consecutive_pixels(crossing_pixels):
    # Sort by border and position
    crossing_pixels.sort(key=lambda p: (p['border'], p['x'] + p['y']))
    
    groups = []
    current_group = [crossing_pixels[0]]
    
    for i in range(1, len(crossing_pixels)):
        prev = crossing_pixels[i-1]
        curr = crossing_pixels[i]
        
        # Calculate distance
        dist = distance(prev, curr)
        
        # Same border and close together?
        if curr['border'] == prev['border'] and dist < 3.0:
            current_group.append(curr)  # Continue group
        else:
            groups.append(current_group)  # Start new group
            current_group = [curr]
    
    groups.append(current_group)
    return groups
```

**Why group**: Draws smooth arcs instead of disconnected dots

#### Step 3: Draw Emphasized Arcs

```python
def draw_crossing_pixel_emphasis(ctx, crossing_pixels):
    pixel_groups = group_consecutive_pixels(crossing_pixels)
    
    for group in pixel_groups:
        if len(group) < 2:
            # Single pixel → draw dot
            ctx.arc(group[0]['x'], group[0]['y'], 1.5, 0, 2*pi)
            ctx.fill()
        else:
            # Multiple pixels → draw thick line
            ctx.set_line_width(3.0)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            
            ctx.move_to(group[0]['x'], group[0]['y'])
            for pixel in group[1:]:
                ctx.line_to(pixel['x'], pixel['y'])
            ctx.stroke()
```

**Result**: Only the crossing arcs are visible (minimal manga style)

### 4. `draw_laugh_energy_lines()` (Lines 380-430)

**Purpose**: Add radial "energy lines" for laugh/excitement bubbles

**Algorithm**:

```python
def draw_laugh_energy_lines(ctx, cx, cy, half_width, half_height, 
                            all_circles, background_color=None):
    
    # 1. Detect background color and adapt
    if background_color:
        r, g, b = background_color
        luminance = 0.299*r + 0.587*g + 0.114*b
        
        if luminance < 0.5:  # Dark background
            ctx.set_source_rgba(1.0, 1.0, 0.7, 0.8)  # Light yellow
        else:  # Light background
            ctx.set_source_rgba(0, 0, 0, 0.65)  # Black
    else:
        ctx.set_source_rgba(0, 0, 0, 0.65)  # Default black
    
    # 2. Draw 18 radial lines
    ctx.set_line_width(2.0)
    num_rays = 18
    
    # Outer radius (just outside bubble)
    outer_rx = half_width + 24
    outer_ry = half_height + 24
    
    for i in range(num_rays):
        # Calculate angle with random jitter
        angle = (2*pi) * (i / num_rays) + random.uniform(-0.05, 0.05)
        
        # Skip some rays randomly (18% chance)
        if random.random() < 0.18:
            continue
        
        # Random length for irregularity
        length = random.uniform(10, 24)
        
        # Start point (outside bubble)
        start_x = cx + math.cos(angle) * (outer_rx + random.uniform(-4, 4))
        start_y = cy + math.sin(angle) * (outer_ry + random.uniform(-4, 4))
        
        # End point (further out)
        end_x = start_x + math.cos(angle) * length
        end_y = start_y + math.sin(angle) * length
        
        # Draw line
        ctx.move_to(start_x, start_y)
        ctx.line_to(end_x, end_y)
    
    ctx.stroke()
```

**Visual Effect**:
```
        │  ╱  ╲  │
       ╱  ○───○  ╲     ← Energy rays
      │  ○     ○  │      radiating outward
       ╲  ○───○  ╱
        │  ╲  ╱  │
```

**Adaptive coloring**: Light rays on dark backgrounds, dark rays on light

### 5. `fill_rectangle_gaps_only()` (Lines 600-700)

**Purpose**: Fill ONLY the narrow gaps between ovals (not entire rectangle)

**Why**: Creates "negative space" effect - border defined by absence

**Algorithm**:

```python
def fill_rectangle_gaps_only(ctx, all_circles, cx, cy, half_width, half_height):
    # 1. Create clipping path = rectangle MINUS all ovals
    
    # Start with rectangle
    ctx.rectangle(cx - half_width, cy - half_height, 
                  half_width * 2, half_height * 2)
    
    # Subtract each oval
    for circle in all_circles:
        ctx.save()
        ctx.translate(circle['x'], circle['y'])
        ctx.scale(circle['rx'], circle['ry'])
        ctx.arc(0, 0, 1, 0, 2 * pi)
        ctx.restore()
    
    # Set to even-odd fill rule (subtracts ovals)
    ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    
    # 2. Fill with white
    ctx.set_source_rgb(1, 1, 1)
    ctx.fill()
```

**Visual Result**:
```
Before:                After gap fill:
   ○     ○                ○ ▓▓▓ ○
  ○ empty ○     →        ○ ████ ○
   ○     ○                ○ ▓▓▓ ○

(▓ = filled gaps, █ = empty center)
```

---

## Configuration Modes

### Global Configuration Flags (Lines 8-16)

```python
# Canvas settings
TRANSPARENT_CANVAS = True          # No background paint

# Filling behavior
RECTANGLE_FILL_IN_MINIMAL = False  # Don't fill whole rectangle
FILL_GAPS_ONLY = True              # Fill only between ovals

# Rendering options
DRAW_TEXT = False                  # Suppress text
EMPHASIZE_INTERIOR_ARCS = False    # Show crossing arcs

# Style options
INK_COLOR = (0, 0, 0, 1)           # Black ink
```

### Mode 1: Full Ovals Display

```python
surface = create_overlapping_circles_square(
    ctx, 250, 200, 180, 120,
    text="Hello!",
    circle_style="organic",
    show_full_ovals=True  # ← Full mode
)
```

**Characteristics**:
- ✅ Complete ovals visible
- ✅ Colored gradients
- ✅ Rectangle border visible
- ✅ Shows structure clearly
- ❌ Not production-ready (too detailed)

**Use Case**: Understanding, debugging, demonstrations

### Mode 2: Minimal Manga Style

```python
surface = create_overlapping_circles_square(
    ctx, 250, 200, 180, 120,
    text="",
    circle_style="organic",
    show_full_ovals=False  # ← Minimal mode
)
```

**Characteristics**:
- ✅ Only crossing arcs visible
- ✅ Clean, professional look
- ✅ Transparent background
- ✅ Manga-ready
- ✅ Production quality

**Use Case**: Final manga lettering

### Style Presets

#### "varied" (Default)

```python
circle_style="varied"
```

**Features**:
- Random size variation (±5-8%)
- Natural position jitter
- Organic appearance
- Balanced randomness

**Best For**: General-purpose bubbles

#### "organic"

```python
circle_style="organic"
```

**Features**:
- Smooth, gentle curves
- Consistent sizing
- Professional appearance
- Minimal randomness

**Best For**: Clean, professional manga

#### "laugh"

```python
circle_style="laugh"
```

**Features**:
- More ovals per side (3 instead of 2 on long sides)
- Smaller, punchier bumps (0.78× scale)
- Random exaggeration (±18% on some ovals)
- Radial energy lines
- Frenetic, bouncy appearance

**Best For**: Excitement, laughter, shouting bubbles

**Code Differences**:
```python
if style == "laugh":
    # Increase oval count
    if side_length > 140:
        num_circles = max(num_circles, 3)
    
    # Scale down for punchier bumps
    rx *= 0.78 * random(0.95, 1.08)
    ry *= 0.78 * random(0.95, 1.08)
    
    # Add energy lines
    draw_laugh_energy_lines(ctx, cx, cy, ...)
```

---

## Geometric Constraints

### Summary Table

| Constraint | Value | Purpose |
|------------|-------|---------|
| `PENETRATION_RATIO_SINGLE` | 0.22 (22%) | Single oval depth into rectangle |
| `PENETRATION_RATIO_DOUBLE` | 0.18 (18%) | Each of 2 ovals' depth |
| `SAME_SIDE_REQUIRED_OVERLAP` | 0.28 (28%) | Minimum same-side overlap |
| `HORIZONTAL_MIN_OVERLAP_FRAC` | 0.14 (14%) | Top/bottom pair overlap |
| `VERTICAL_MIN_OVERLAP_FRAC` | 0.14 (14%) | Left/right pair overlap |
| `CORNER_GROWTH` | 1.08 (8%) | Extra growth for corner ovals |

### Why These Values?

#### Penetration Depth (0.18-0.22)

**Too shallow (< 0.15)**:
- Ovals barely touch rectangle
- Disconnected appearance
- No organic integration

**Too deep (> 0.30)**:
- Ovals meet in center
- No text space
- Overcrowded

**Sweet spot (0.18-0.22)**:
- Visible integration
- Clear center
- Natural appearance

#### Same-Side Overlap (0.28)

**No overlap (< 0.10)**:
- Disconnected chain
- Gaps in perimeter
- Broken border

**Too much overlap (> 0.40)**:
- Ovals almost identical positions
- Redundant
- Loses chain effect

**Sweet spot (0.28)**:
- Clear chain connection
- Visible individual ovals
- Organic linking

#### Corner Growth (1.08)

**No growth (1.00)**:
- Corner ovals might not reach perpendicular neighbors
- Gaps at corners
- Disconnected border

**Too much growth (> 1.15)**:
- Corner ovals too large
- Overwhelm corner area
- Loses sharp corner gap

**Sweet spot (1.08)**:
- Guaranteed corner connection
- Maintains corner gap visibility
- Natural integration

---

## Advanced Features

### 1. Pixel-Precise Intersection Detection

**Traditional Approach** (approximate):
```python
# Check if oval bounding box intersects border
if oval_x < border_x + tolerance:
    intersection_found = True
```

**Problem**: Inaccurate for ellipses, misses actual crossing points

**This Algorithm** (precise):
```python
# Sample 360 points around actual oval perimeter
for angle in range(360):
    point = calculate_point_on_ellipse(angle)
    if distance_to_border(point) < 1.5_pixels:
        exact_crossing_point = point
```

**Advantage**: Sub-pixel accuracy, works for any ellipse shape

### 2. Background-Aware Color Adaptation

**Challenge**: Energy lines must be visible on any background

**Solution**: Luminance-based color selection

```python
# Calculate perceived brightness
luminance = 0.299*R + 0.587*G + 0.114*B

if luminance < 0.5:
    # Dark background → use light lines
    color = (1.0, 1.0, 0.7, 0.8)  # Light yellow
else:
    # Light background → use dark lines
    color = (0, 0, 0, 0.65)  # Black
```

**Luminance formula**: ITU-R BT.601 standard (human eye sensitivity)
- Green contributes most (58.7%)
- Red contributes medium (29.9%)
- Blue contributes least (11.4%)

### 3. Even-Odd Fill Rule (Gap Filling)

**Cairo Fill Rules**:

**FILL_RULE_WINDING** (default):
- Fills all enclosed areas
- Subpaths add to fill

**FILL_RULE_EVEN_ODD** (used here):
- Toggles fill on each boundary crossing
- Creates "holes" in filled areas

**Application**:
```python
# Create compound path
ctx.rectangle(...)  # Add rectangle (fill = ON)
for circle in circles:
    ctx.arc(...)    # Add circle (fill toggles → OFF inside circles)

ctx.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
ctx.fill()  # Fills rectangle MINUS circles
```

**Visual**:
```
Rectangle ▓▓▓▓▓▓▓▓▓
         ▓○ empty ○▓  ← Circles create holes
         ▓▓▓▓▓▓▓▓▓
```

### 4. Automatic Overlap Guarantee

**Problem**: Random placement might create gaps

**Solution**: Post-process enforcement

```python
# 1. Generate ovals with constraints
circles = generate_with_constraints()

# 2. Check all corner overlaps
for corner in all_corners:
    adjacent_ovals = find_adjacent_ovals(corner)
    if not overlapping(adjacent_ovals):
        # 3. Enlarge until overlapping
        enlarge_radii_minimally(adjacent_ovals)
```

**Key**: Minimal enlargement preserves intended gaps

### 5. Constraint-Based Randomness

**Traditional random**:
```python
radius = random.uniform(50, 100)  # Any value
```

**Problem**: No guarantees about overlaps, spacing

**This algorithm**:
```python
# Calculate required value from constraints
base_radius = calculate_from_constraints()

# Add controlled variation
radius = base_radius * random.uniform(0.94, 1.05)  # ±5%
```

**Guarantees**: All constraints met even with randomness

---

## Usage Examples

### Example 1: Basic Organic Bubble

```python
import cairo
from overlapping_circles_squares import create_overlapping_circles_square

# Create surface
width, height = 500, 400
surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
ctx = cairo.Context(surface)

# White background (optional)
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

# Create bubble (minimal manga style)
create_overlapping_circles_square(
    ctx,
    cx=250,           # Center X
    cy=200,           # Center Y
    base_width=180,   # Rectangle width
    base_height=120,  # Rectangle height
    text="",          # No text
    circle_style="organic",
    show_full_ovals=False  # Minimal style
)

# Save
surface.write_to_png("organic_bubble.png")
```

### Example 2: Laugh Bubble with Energy

```python
# Same setup as above...

create_overlapping_circles_square(
    ctx,
    cx=250, cy=200,
    base_width=200, base_height=140,
    text="",
    circle_style="laugh",  # ← Laugh style
    show_full_ovals=False,
    background_color=(1, 1, 1)  # White bg for color detection
)

surface.write_to_png("laugh_bubble.png")
```

### Example 3: Return Circle Data

```python
# Get circle data without rendering
circles = create_overlapping_circles_square(
    ctx,
    cx=250, cy=200,
    base_width=180, base_height=120,
    circle_style="organic",
    return_circles=True  # ← Return data instead of rendering
)

# Use circle data for custom processing
for circle in circles:
    print(f"Circle at ({circle['x']}, {circle['y']})")
    print(f"  Radii: {circle['rx']} x {circle['ry']}")
    print(f"  Side: {circle['side']}")
```

### Example 4: Full Ovals Display (Debug)

```python
# Show full structure for understanding
create_overlapping_circles_square(
    ctx,
    cx=250, cy=200,
    base_width=180, base_height=120,
    text="DEBUG",
    circle_style="varied",
    show_full_ovals=True  # ← Full display mode
)

surface.write_to_png("debug_full_ovals.png")
```

### Example 5: Integration with Auto-Scale

```python
from manhwa_bubbles.auto_scale import auto_scale_bubble_adaptive

# This function internally uses overlapping_circles_squares
surface, metadata = auto_scale_bubble_adaptive(
    text="Your dialogue here",
    canvas_size=(500, 400),
    max_iterations=5
)

# Automatically sizes bubble to fit text
surface.write_to_png("auto_sized_bubble.png")
```

### Example 6: Batch Generation

```python
import random

# Generate 10 varied bubbles
for i in range(10):
    random.seed(i)  # Reproducible variation
    
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 420, 320)
    ctx = cairo.Context(surface)
    
    # Vary size slightly
    width = 170 + random.uniform(-15, 15)
    height = 115 + random.uniform(-12, 12)
    
    create_overlapping_circles_square(
        ctx, 210, 160, width, height,
        circle_style="organic",
        show_full_ovals=False
    )
    
    surface.write_to_png(f"bubble_{i:02d}.png")
```

---

## Performance Considerations

### Computational Complexity

#### Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Generate side circles | O(n) | n = number of sides (4) |
| Enforce corner overlaps | O(c²) | c = circles per side (1-3) |
| Find crossing pixels | O(c × 360) | 360 samples per circle |
| Group pixels | O(p log p) | p = crossing pixels, sort |
| Draw operations | O(c + p) | Linear in elements |

**Overall**: O(c × 360 + p log p) ≈ **O(1440)** for typical bubble

**Fast**: ~1-2ms per bubble on modern hardware

#### Space Complexity

- **Circle data**: ~10 circles × 100 bytes = 1 KB
- **Crossing pixels**: ~500 pixels × 50 bytes = 25 KB
- **Cairo surface**: width × height × 4 bytes = 800 KB (for 500×400)

**Overall**: O(w × h) for surface, O(1) for algorithm

### Optimization Opportunities

#### 1. Reduce Sampling Resolution

```python
# Current: 360 samples per circle
for angle in range(360):
    sample_point(angle)

# Optimized: 180 samples (every 2 degrees)
for angle in range(0, 360, 2):
    sample_point(angle)
```

**Trade-off**: 2× faster, slightly less precise crossings

#### 2. Skip Empty Regions

```python
# Only sample angles likely to cross borders
for circle in circles:
    # Calculate angle range that could intersect rectangle
    angle_range = calculate_potential_crossing_range(circle, rect)
    
    # Only sample that range
    for angle in angle_range:
        sample_point(angle)
```

**Speed-up**: 3-4× faster (most of circle doesn't cross)

#### 3. Cache Circle Paths

```python
# Cache Cairo paths for reuse
circle_paths = {}

for circle in circles:
    if circle not in circle_paths:
        path = create_circle_path(circle)
        circle_paths[circle] = path
    
    ctx.append_path(circle_paths[circle])
```

**Use case**: Rendering same bubble multiple times

### Memory Optimization

#### Current: Full pixel storage

```python
crossing_pixels = []
for angle in range(360):
    crossing_pixels.append({'x': px, 'y': py, ...})  # Full dict
```

**Memory**: ~50 bytes × 500 pixels = 25 KB

#### Optimized: Compact storage

```python
# Use numpy arrays
crossing_x = np.zeros(500)
crossing_y = np.zeros(500)

for i, angle in enumerate(range(360)):
    crossing_x[i] = px
    crossing_y[i] = py
```

**Memory**: 8 bytes × 500 × 2 = 8 KB (3× reduction)

### Rendering Optimization

#### Use Cairo Groups for Transparency

```python
# Instead of multiple transparent draws
ctx.push_group()
draw_all_elements()
ctx.pop_group_to_source()
ctx.paint_with_alpha(0.9)
```

**Benefit**: Single compositing operation

---

## Integration Points

### Used By

1. **`manhwa_bubbles/auto_scale.py`**
   - Imports `create_overlapping_circles_square`
   - Uses for adaptive bubble sizing
   - Wraps in auto-sizing logic

2. **`manhwa_bubbles/organic_overlap.py`**
   - Wrapper for easier library integration
   - Exposes simplified API

3. **Test/Demo Scripts**
   - `examples/demo.py`
   - `examples/extended_demo.py`
   - Various test files

### Extension Points

#### Custom Styles

```python
# Add new style to SUPPORTED_STYLES
SUPPORTED_STYLES = {"varied", "organic", "laugh", "custom"}

# Handle in generate_circles_for_side()
if style == "custom":
    # Your custom logic here
    num_circles = custom_logic()
    rx *= custom_scale()
    ...
```

#### Custom Rendering

```python
# Override draw functions
def custom_draw_single_circle(ctx, circle, ...):
    # Your custom rendering
    pass

# Use in main function
if custom_mode:
    custom_draw_single_circle(ctx, circle, ...)
else:
    draw_single_circle(ctx, circle, ...)
```

---

## Troubleshooting

### Common Issues

#### Issue 1: Gaps at Corners

**Symptom**: Ovals don't connect at rectangle corners

**Cause**: Corner overlap enforcement not running or insufficient

**Fix**:
```python
# Increase CORNER_GROWTH factor
CORNER_GROWTH = 1.12  # Was 1.08

# Or increase margin in enforce_corner_overlaps
MARGIN = 3.0  # Was 1.0
```

#### Issue 2: Ovals Meet in Center

**Symptom**: No text space, ovals cross entire rectangle

**Cause**: Penetration depth too large

**Fix**:
```python
# Reduce penetration ratios
PENETRATION_RATIO_SINGLE = 0.18  # Was 0.22
PENETRATION_RATIO_DOUBLE = 0.14  # Was 0.18
```

#### Issue 3: Disconnected Same-Side Ovals

**Symptom**: Two ovals on same side don't touch

**Cause**: Overlap requirement not met

**Fix**:
```python
# Increase overlap requirement
SAME_SIDE_REQUIRED_OVERLAP = 0.35  # Was 0.28

# Or check generation logic for scale reduction
```

#### Issue 4: Energy Lines Invisible

**Symptom**: Laugh style doesn't show lines

**Cause**: Color doesn't contrast with background

**Fix**:
```python
# Pass background_color parameter
create_overlapping_circles_square(
    ...,
    circle_style="laugh",
    background_color=(r, g, b)  # ← Add this
)
```

#### Issue 5: Too Much Randomness

**Symptom**: Inconsistent bubble appearance

**Cause**: Random seed not set

**Fix**:
```python
import random
random.seed(42)  # Reproducible results

create_overlapping_circles_square(...)
```

---

## Future Enhancements

### Potential Improvements

1. **Adaptive Oval Count**
   - Dynamic oval count based on aspect ratio
   - More ovals for very long rectangles

2. **Bezier Curve Transitions**
   - Smooth bezier curves between ovals
   - Even more organic appearance

3. **Interior Pattern Variations**
   - Different overlap patterns (spiral, radial)
   - Style-specific interior ovals

4. **Performance Optimization**
   - GPU-accelerated rendering (Skia, OpenGL)
   - Parallel processing for batch generation

5. **Machine Learning Integration**
   - Train on real manga bubbles
   - Learn optimal overlap patterns

6. **3D Extrusion**
   - Add depth/shadow for 3D effect
   - Layered bubble rendering

---

## Conclusion

The `overlapping_circles_squares.py` algorithm represents a sophisticated approach to procedural manga bubble generation that balances:

- **Mathematical precision** (guaranteed overlaps, no gaps)
- **Organic randomness** (natural variation, hand-drawn feel)
- **Performance** (sub-second rendering)
- **Flexibility** (multiple styles, modes, configurations)

The key innovation is the **constraint-based random generation** system that:
1. Establishes hard requirements (overlaps, spacing)
2. Calculates positions/sizes to meet requirements
3. Adds controlled variation within constraints
4. Post-processes to guarantee correctness

This results in bubbles that look hand-drawn while maintaining structural integrity.

---

## References

### Internal Files
- `examples/experiments/overlapping_circles_squares.py` - Main implementation
- `examples/experiments/overlapping_circles_circle.py` - Circular variant
- `manhwa_bubbles/auto_scale.py` - Integration wrapper
- `manhwa_bubbles/organic_overlap.py` - Library wrapper

### External Resources
- Cairo Graphics Library: https://www.cairographics.org/
- Manga Speech Bubble Analysis: Professional manga reference
- Computational Geometry: Ellipse intersection algorithms

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-25  
**Maintained By**: Manhwa Bubbles Project
