#!/usr/bin/env python3
"""
Simple YOLO test to diagnose detection issues.
"""

import sys
import math
import random

print("="*70)
print("YOLO DETECTION DIAGNOSTIC")
print("="*70)
print()

# Check dependencies
print("Checking dependencies...")
missing = []

try:
    import cv2
    print("✅ opencv-python installed")
except ImportError:
    print("❌ opencv-python NOT installed")
    missing.append("opencv-python")

try:
    from ultralytics import YOLO
    print("✅ ultralytics (YOLO) installed")
except ImportError:
    print("❌ ultralytics NOT installed")
    missing.append("ultralytics")

try:
    from PIL import Image
    print("✅ pillow installed")
except ImportError:
    print("❌ pillow NOT installed")
    missing.append("pillow")

print()

if missing:
    print("❌ MISSING DEPENDENCIES!")
    print()
    print("Install them with:")
    print(f"  pip3 install {' '.join(missing)}")
    print()
    print("Or install all at once:")
    print("  pip3 install ultralytics opencv-python pillow")
    sys.exit(1)

print("✅ All dependencies installed!")
print()

# Test YOLO detection
print("Testing YOLO detection...")
try:
    model = YOLO('yolov8n.pt')
    print("✅ YOLO model loaded")
    
    # Test with your manga
    if len(sys.argv) > 1:
        manga_file = sys.argv[1]
        print(f"\nTesting detection on: {manga_file}")
        
        # Try different confidence levels
        best_results = None
        best_conf = None
        for conf in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]:
            results = model(manga_file, conf=conf, verbose=False)
            
            person_count = 0
            for result in results:
                for box in result.boxes:
                    if int(box.cls[0]) == 0:  # person class
                        person_count += 1
            
            print(f"  confidence={conf:.2f} → {person_count} people detected")
            
            if person_count > 0 and best_results is None:
                best_results = results
                best_conf = conf
                print()
                print(f"✅ Best confidence level: {conf}")
                print(f"   Found {person_count} people")
                break
        
        # Show detailed detection info
        if best_results:
            print()
            print("="*70)
            print("DETECTED PEOPLE DETAILS:")
            print("="*70)
            
            import cv2
            img = cv2.imread(manga_file)
            
            # Different colors for each person
            colors = [
                (0, 255, 0),      # Green for Person 1
                (255, 0, 0),      # Blue for Person 2
                (0, 0, 255),      # Red for Person 3
                (255, 255, 0),    # Cyan for Person 4
                (255, 0, 255),    # Magenta for Person 5
                (0, 255, 255),    # Yellow for Person 6
            ]
            
            person_num = 0
            all_detections = []
            
            for result in best_results:
                for box in result.boxes:
                    if int(box.cls[0]) == 0:  # person class
                        person_num += 1
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        conf_val = float(box.conf[0])
                        
                        # Get color for this person
                        color = colors[(person_num - 1) % len(colors)]
                        
                        # Calculate center and head position
                        cx = int((x1 + x2) / 2)
                        cy = int((y1 + y2) / 2)
                        head_y = int(y1 + (y2 - y1) * 0.15)
                        
                        print(f"\nPerson {person_num}:")
                        print(f"  Bounding box: ({int(x1)}, {int(y1)}) to ({int(x2)}, {int(y2)})")
                        print(f"  Center: ({cx}, {cy})")
                        print(f"  Head position: ({cx}, {head_y})")
                        print(f"  Confidence: {conf_val:.2%}")
                        print(f"  Color: {['Green', 'Blue', 'Red', 'Cyan', 'Magenta', 'Yellow'][(person_num-1) % 6]}")
                        print(f"  → Place bubble at: ({cx - 125}, {head_y - 200})")
                        
                        # Draw bounding box with unique color
                        cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), 
                                    color, 4)
                        
                        # Draw head position with same color
                        cv2.circle(img, (cx, head_y), 15, color, -1)
                        
                        # Draw person label with same color
                        cv2.putText(img, f"Person {person_num}", (int(x1), int(y1)-10),
                                  cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                        
                        # Draw bubble position indicator with lighter shade
                        bubble_x = cx - 125
                        bubble_y = head_y - 200
                        bubble_color = tuple([int(c * 0.7) for c in color])
                        cv2.rectangle(img, (bubble_x, bubble_y), 
                                    (bubble_x + 250, bubble_y + 80),
                                    bubble_color, 3)
                        cv2.putText(img, f"Bubble {person_num}", (bubble_x + 10, bubble_y + 40),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, bubble_color, 2)
                        
                        all_detections.append({
                            'bbox': (int(x1), int(y1), int(x2), int(y2)),
                            'center': (cx, cy),
                            'head': (cx, head_y),
                            'confidence': conf_val
                        })
            
            # Save visualization
            output_file = 'detected_people_visualization.png'
            cv2.imwrite(output_file, img)
            print()
            print("="*70)
            print(f"✅ Saved visualization: {output_file}")
            print("="*70)
            print()
            print("Legend:")
            print("  🟢 Person 1 = Green")
            print("  🔵 Person 2 = Blue")
            print("  🔴 Person 3 = Red")
            print("  🩵 Person 4+ = Cyan/Magenta/Yellow")
            print()
            print("Each person has:")
            print("  • Thick colored box around them")
            print("  • Colored circle at head position")
            print("  • Lighter colored box showing bubble placement")
            print()
            print(f"Open {output_file} to see all detections!")
            
            # ===== ADD CAIRO BUBBLES WITH TEXT =====
            print()
            print("="*70)
            print("ADDING CAIRO BUBBLES WITH TEXT")
            print("="*70)
            
            try:
                import cairo
                from PIL import Image as PILImage
                
                # Load the manga as background
                manga_bg = PILImage.open(manga_file).convert('RGBA')
                
                # Sort detections left to right (reading order)
                sorted_dets = sorted(all_detections, key=lambda d: d['head'][0])
                
                # Get dialogues from command line or use defaults
                dialogues = []
                if len(sys.argv) > 2:
                    dialogues = sys.argv[2:]
                else:
                    dialogues = [f"Character {i+1}" for i in range(len(sorted_dets))]
                
                # Ensure we have enough dialogues
                while len(dialogues) < len(sorted_dets):
                    dialogues.append(f"Character {len(dialogues)+1}")
                
                print()
                # Process each detected person
                for i, det in enumerate(sorted_dets):
                    head_x, head_y = det['head']
                    text = dialogues[i]
                    
                    # Create Cairo bubble canvas
                    bubble_canvas_w, bubble_canvas_h = 500, 400
                    bubble_surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, 
                                                     bubble_canvas_w, bubble_canvas_h)
                    ctx = cairo.Context(bubble_surf)
                    
                    # Transparent background
                    ctx.set_source_rgba(0, 0, 0, 0)
                    ctx.paint()
                    
                    # Calculate bubble placement - far enough to not cover face
                    # Get person's bounding box to avoid covering them
                    bbox_x1, bbox_y1, bbox_x2, bbox_y2 = det['bbox']
                    person_width = bbox_x2 - bbox_x1
                    person_height = bbox_y2 - bbox_y1
                    
                    # Random bubble placement with face avoidance
                    # Seed for reproducibility (based on person index + image name)
                    seed = hash(manga_file) + i
                    random.seed(seed)
                    
                    # Define possible placement zones (offset from head)
                    placement_zones = [
                        # (x_offset, y_offset, name)
                        (-(person_width//2 + 200), -(person_height*0.7 + 150), "top-left"),
                        (0, -(person_height*0.8 + 180), "top-center"),
                        (person_width//2 + 200, -(person_height*0.7 + 150), "top-right"),
                        (-(person_width + 250), -(person_height*0.3), "left"),
                        (person_width + 250, -(person_height*0.3), "right"),
                        (-(person_width//2 + 180), -(person_height*0.5 + 100), "upper-left"),
                        (person_width//2 + 180, -(person_height*0.5 + 100), "upper-right"),
                    ]
                    
                    # Calculate face region (upper 30% of person bounding box)
                    face_top = bbox_y1
                    face_bottom = bbox_y1 + (bbox_y2 - bbox_y1) * 0.3
                    face_left = bbox_x1
                    face_right = bbox_x2
                    
                    # Try random zones until we find one that doesn't cover face
                    zone_idx = random.randint(0, len(placement_zones) - 1)
                    bubble_offset_x, bubble_offset_y, zone_name = placement_zones[zone_idx]
                    
                    # Calculate initial paste position
                    temp_paste_x = head_x + bubble_offset_x - bubble_canvas_w // 2
                    temp_paste_y = head_y + bubble_offset_y - bubble_canvas_h // 2
                    
                    # Check if bubble would overlap face
                    bubble_left = temp_paste_x
                    bubble_right = temp_paste_x + bubble_canvas_w
                    bubble_top = temp_paste_y
                    bubble_bottom = temp_paste_y + bubble_canvas_h
                    
                    overlaps_face = not (
                        bubble_right < face_left or
                        bubble_left > face_right or
                        bubble_bottom < face_top or
                        bubble_top > face_bottom
                    )
                    
                    # If overlaps, try next zones
                    attempts = 0
                    while overlaps_face and attempts < len(placement_zones):
                        zone_idx = (zone_idx + 1) % len(placement_zones)
                        bubble_offset_x, bubble_offset_y, zone_name = placement_zones[zone_idx]
                        
                        # Recalculate paste position
                        temp_paste_x = head_x + bubble_offset_x - bubble_canvas_w // 2
                        temp_paste_y = head_y + bubble_offset_y - bubble_canvas_h // 2
                        
                        bubble_left = temp_paste_x
                        bubble_right = temp_paste_x + bubble_canvas_w
                        bubble_top = temp_paste_y
                        bubble_bottom = temp_paste_y + bubble_canvas_h
                        
                        overlaps_face = not (
                            bubble_right < face_left or
                            bubble_left > face_right or
                            bubble_bottom < face_top or
                            bubble_top > face_bottom
                        )
                        
                        attempts += 1
                    
                    bubble_center_x = bubble_canvas_w // 2
                    bubble_center_y = bubble_canvas_h // 2
                    
                    # Where bubble will be pasted on manga
                    paste_x = head_x + bubble_offset_x - bubble_center_x
                    paste_y = head_y + bubble_offset_y - bubble_center_y
                    
                    # Bubble center in manga coordinates
                    bubble_manga_cx = paste_x + bubble_center_x
                    bubble_manga_cy = paste_y + bubble_center_y
                    
                    # Calculate direction from bubble center TO head
                    dx = head_x - bubble_manga_cx
                    dy = head_y - bubble_manga_cy
                    distance = math.sqrt(dx*dx + dy*dy) or 1.0
                    
                    # Normalize direction vector
                    ux = dx / distance
                    uy = dy / distance
                    
                    # Draw bubble ellipse FIRST (no tail yet)
                    radius_x, radius_y = 140, 70
                    
                    ctx.save()
                    ctx.translate(bubble_center_x, bubble_center_y)
                    ctx.scale(radius_x, radius_y)
                    ctx.arc(0, 0, 1, 0, 2 * 3.14159)
                    ctx.restore()
                    
                    # Fill white
                    ctx.set_source_rgba(1, 1, 1, 1)
                    ctx.fill_preserve()
                    
                    # Black outline
                    ctx.set_source_rgba(0, 0, 0, 1)
                    ctx.set_line_width(3)
                    ctx.stroke()
                    
                    # NOW draw tail pointing toward head
                    # Find where tail attaches on ellipse (in direction of head)
                    angle_to_head = math.atan2(uy, ux)
                    
                    # Point on ellipse boundary in direction of head
                    attach_x = bubble_center_x + radius_x * math.cos(angle_to_head)
                    attach_y = bubble_center_y + radius_y * math.sin(angle_to_head)
                    
                    # Tail extends from attach point toward head
                    tail_length = 60
                    tip_x = attach_x + ux * tail_length
                    tip_y = attach_y + uy * tail_length
                    
                    # Perpendicular vector for tail width
                    px = -uy
                    py = ux
                    tail_width = 25
                    
                    # Triangle vertices (base on bubble, tip toward head)
                    p1x = attach_x + px * tail_width
                    p1y = attach_y + py * tail_width
                    p2x = attach_x - px * tail_width
                    p2y = attach_y - py * tail_width
                    
                    # Draw tail triangle
                    ctx.move_to(p1x, p1y)
                    ctx.line_to(p2x, p2y)
                    ctx.line_to(tip_x, tip_y)
                    ctx.close_path()
                    
                    ctx.set_source_rgba(1, 1, 1, 1)
                    ctx.fill_preserve()
                    ctx.set_source_rgba(0, 0, 0, 1)
                    ctx.set_line_width(3)
                    ctx.stroke()
                    
                    # Add text (word wrap if needed)
                    ctx.select_font_face('Arial', cairo.FONT_SLANT_NORMAL, 
                                        cairo.FONT_WEIGHT_BOLD)
                    font_size = 28
                    ctx.set_font_size(font_size)
                    
                    # Simple word wrap
                    words = text.split()
                    lines = []
                    current_line = []
                    max_width = radius_x * 2 - 40
                    
                    for word in words:
                        test_line = ' '.join(current_line + [word])
                        x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = \
                            ctx.text_extents(test_line)
                        
                        if text_width > max_width and current_line:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                        else:
                            current_line.append(word)
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    
                    # Draw each line centered
                    line_height = font_size * 1.2
                    total_text_height = len(lines) * line_height
                    start_y = bubble_center_y - total_text_height / 2 + font_size
                    
                    ctx.set_source_rgba(0, 0, 0, 1)
                    for j, line in enumerate(lines):
                        x_bearing, y_bearing, text_width, text_height, x_advance, y_advance = \
                            ctx.text_extents(line)
                        ctx.move_to(bubble_center_x - text_width / 2, start_y + j * line_height)
                        ctx.show_text(line)
                    
                    # Convert Cairo surface to PIL
                    bubble_pil = PILImage.frombuffer(
                        'RGBA',
                        (bubble_canvas_w, bubble_canvas_h),
                        bubble_surf.get_data(),
                        'raw', 'BGRA', 0, 1
                    )
                    
                    # Keep bubble in bounds (paste_x and paste_y already calculated above)
                    paste_x = max(0, min(paste_x, manga_bg.width - bubble_canvas_w))
                    paste_y = max(0, min(paste_y, manga_bg.height - bubble_canvas_h))
                    
                    # Composite onto manga
                    manga_bg.paste(bubble_pil, (paste_x, paste_y), bubble_pil)
                    
                    print(f"  ✅ Added bubble for Person {i+1}: '{text[:30]}...'")
                    print(f"     Zone: {zone_name}, Offset: ({bubble_offset_x:.0f}, {bubble_offset_y:.0f})")
                
                # Save final result
                output_with_bubbles = 'manga_with_cairo_bubbles.png'
                manga_bg.save(output_with_bubbles)
                print()
                print("="*70)
                print(f"✅ SUCCESS! Saved final manga: {output_with_bubbles}")
                print("="*70)
                print()
                print("Generated files:")
                print(f"  1. {output_file} - Detection visualization")
                print(f"  2. {output_with_bubbles} - Final manga with bubbles")
                
            except ImportError as e:
                print(f"⚠️  Cairo not available: {e}")
                print("   Install with: pip3 install pycairo")
                print("   Skipping bubble generation...")
            except Exception as e:
                print(f"⚠️  Error adding bubbles: {e}")
                import traceback
                traceback.print_exc()
                print("   Detection visualization still saved!")
        
        if person_count == 0:
            print()
            print("⚠️  YOLO couldn't detect people in this image.")
            print()
            print("Possible reasons:")
            print("  1. Manga art too stylized (YOLO trained on photos)")
            print("  2. Characters too small or partial")
            print("  3. Heavy shadows/occlusion")
            print()
            print("Solutions:")
            print("  • Use anime-face-detector (pip install anime-face-detector)")
            print("  • Use manual click method (simple_manga_test.py)")
            print("  • Train custom YOLO on your manga style")
    else:
        print()
        print("Usage: python3 test_yolo_simple.py your_manga.png")
        
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

print()
print("="*70)
print("DIAGNOSTIC COMPLETE")
print("="*70)

