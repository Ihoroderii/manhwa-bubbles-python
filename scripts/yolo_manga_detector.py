#!/usr/bin/env python3
"""
YOLO-based manga character detection and bubble placement.

This script uses YOLO to detect people/characters in manga panels,
then automatically positions speech bubbles above them.

Install dependencies:
    pip3 install ultralytics opencv-python pillow
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False
    print("⚠️  ultralytics not installed. Run: pip3 install ultralytics")

try:
    from manhwa_bubbles import speech_bubble
    MANHWA_AVAILABLE = True
except ImportError:
    MANHWA_AVAILABLE = False
    print("⚠️  manhwa_bubbles not available, will use basic bubbles")


class MangaPersonDetector:
    """Detect people/characters in manga using YOLO."""
    
    def __init__(self, model_name='yolov8n.pt', confidence=0.25):
        """
        Initialize YOLO detector.
        
        Args:
            model_name: YOLO model to use (yolov8n.pt, yolov8s.pt, etc.)
            confidence: Detection confidence threshold (0-1)
        """
        if not YOLO_AVAILABLE:
            raise ImportError("ultralytics not installed. Run: pip3 install ultralytics")
        
        print(f"Loading YOLO model: {model_name}...")
        self.model = YOLO(model_name)
        self.confidence = confidence
        print("✅ YOLO model loaded")
    
    def detect_people(self, image_path, visualize=False):
        """
        Detect people in manga image.
        
        Args:
            image_path: Path to manga image
            visualize: If True, show detection visualization
        
        Returns:
            List of dictionaries with detection info:
            [{
                'bbox': (x1, y1, x2, y2),
                'center': (cx, cy),
                'head_pos': (hx, hy),  # Estimated head position
                'confidence': float
            }, ...]
        """
        # Run YOLO detection
        results = self.model(image_path, conf=self.confidence, verbose=False)
        
        detections = []
        
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                # Get class (0 = person in COCO dataset)
                cls = int(box.cls[0])
                
                # Only process 'person' class
                if cls == 0:  # person class
                    # Get bounding box
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    conf = float(box.conf[0])
                    
                    # Calculate center and estimated head position
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2
                    
                    # Head is typically in upper 20% of bounding box
                    head_y = y1 + (y2 - y1) * 0.15
                    head_x = cx
                    
                    detections.append({
                        'bbox': (int(x1), int(y1), int(x2), int(y2)),
                        'center': (int(cx), int(cy)),
                        'head_pos': (int(head_x), int(head_y)),
                        'confidence': conf
                    })
        
        print(f"✅ Detected {len(detections)} people")
        
        if visualize and detections:
            self._visualize_detections(image_path, detections)
        
        return detections
    
    def _visualize_detections(self, image_path, detections):
        """Show detection results visually."""
        img = cv2.imread(str(image_path))
        
        for i, det in enumerate(detections):
            x1, y1, x2, y2 = det['bbox']
            head_x, head_y = det['head_pos']
            conf = det['confidence']
            
            # Draw bounding box
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Draw head marker
            cv2.circle(img, (head_x, head_y), 10, (255, 0, 0), -1)
            
            # Add label
            label = f"Person {i+1}: {conf:.2f}"
            cv2.putText(img, label, (x1, y1-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save visualization
        output_path = 'detected_people.png'
        cv2.imwrite(output_path, img)
        print(f"📊 Saved detection visualization: {output_path}")
        
        # Also display if possible
        try:
            cv2.imshow('Detected People (Press any key)', img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        except:
            pass  # Headless environment


def add_bubbles_to_detected_people(manga_path, detections, dialogues, 
                                   bubble_offset_y=200, output_path='manga_with_yolo_bubbles.png'):
    """
    Add speech bubbles above detected people.
    
    Args:
        manga_path: Path to manga image
        detections: List of detection dicts from detect_people()
        dialogues: List of text strings for each person
        bubble_offset_y: Pixels above head to place bubble
        output_path: Where to save result
    """
    # Load manga
    manga = Image.open(manga_path).convert('RGBA')
    draw = ImageDraw.Draw(manga)
    
    # Sort detections left-to-right (reading order)
    sorted_dets = sorted(detections, key=lambda d: d['head_pos'][0])
    
    # Add bubble for each detected person
    for i, det in enumerate(sorted_dets):
        if i >= len(dialogues):
            break  # No more dialogue to add
        
        head_x, head_y = det['head_pos']
        text = dialogues[i]
        
        # Position bubble above head
        bubble_x = head_x - 125
        bubble_y = head_y - bubble_offset_y
        
        # Ensure bubble stays in bounds
        bubble_x = max(10, min(bubble_x, manga.width - 260))
        bubble_y = max(10, bubble_y)
        
        # Add speech bubble
        if MANHWA_AVAILABLE:
            speech_bubble(draw, (bubble_x, bubble_y, 250, 80),
                         text, bubble_type='oval', tail_dir='down')
        else:
            # Fallback: simple bubble
            draw.ellipse((bubble_x, bubble_y, bubble_x+250, bubble_y+80),
                        fill='white', outline='black', width=3)
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 16)
            except:
                font = ImageFont.load_default()
            draw.text((bubble_x+20, bubble_y+30), text, fill='black', font=font)
        
        print(f"  Added bubble {i+1}: '{text[:20]}...' at ({bubble_x}, {bubble_y})")
    
    # Save result
    manga.save(output_path)
    print(f"\n✅ Saved result: {output_path}")
    return manga


def demo_yolo_detection():
    """Demo: Detect people and add bubbles automatically."""
    
    print("="*70)
    print("YOLO MANGA CHARACTER DETECTION + BUBBLE PLACEMENT")
    print("="*70)
    print()
    
    # Create a test manga panel
    print("Creating test manga panel...")
    test_manga = create_test_manga_panel()
    test_path = 'test_manga_for_yolo.png'
    test_manga.save(test_path)
    print(f"✅ Created: {test_path}")
    print()
    
    # Initialize detector with lower confidence for simple art
    try:
        detector = MangaPersonDetector(model_name='yolov8n.pt', confidence=0.1)
    except Exception as e:
        print(f"❌ Error loading YOLO: {e}")
        print("\nInstall YOLO:")
        print("  pip3 install ultralytics")
        return
    
    # Detect people
    print("Running person detection...")
    detections = detector.detect_people(test_path, visualize=True)
    
    if not detections:
        print("⚠️  No people detected. Try lowering confidence threshold.")
        print("   Or use a more realistic manga image.")
        return
    
    # Add bubbles
    print("\nAdding speech bubbles...")
    dialogues = [
        "We have to work together!",
        "I'm ready!",
        "Let's do this!"
    ]
    
    add_bubbles_to_detected_people(
        test_path,
        detections,
        dialogues,
        bubble_offset_y=220
    )
    
    print("\n" + "="*70)
    print("✅ COMPLETE!")
    print("="*70)
    print("\nGenerated files:")
    print("  - test_manga_for_yolo.png (original)")
    print("  - detected_people.png (detection visualization)")
    print("  - manga_with_yolo_bubbles.png (final result)")


def create_test_manga_panel():
    """Create a simple test manga panel with characters."""
    width, height = 1000, 1400
    manga = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(manga)
    
    # Panel border
    draw.rectangle([20, 20, width-20, height-20], outline='black', width=4)
    
    # Draw three characters (simple human shapes)
    characters = [
        {'x': 250, 'y': 900, 'color': (100, 150, 200)},
        {'x': 500, 'y': 950, 'color': (150, 100, 150)},
        {'x': 750, 'y': 920, 'color': (200, 100, 100)},
    ]
    
    for char in characters:
        x, y = char['x'], char['y']
        color = char['color']
        
        # Head
        draw.ellipse([x-50, y-100, x+50, y], fill=color, outline='black', width=2)
        
        # Body (rectangle)
        draw.rectangle([x-40, y, x+40, y+150], fill=color, outline='black', width=2)
        
        # Arms
        draw.line([x-40, y+30, x-80, y+100], fill='black', width=5)
        draw.line([x+40, y+30, x+80, y+100], fill='black', width=5)
        
        # Legs
        draw.line([x-20, y+150, x-40, y+250], fill='black', width=5)
        draw.line([x+20, y+150, x+40, y+250], fill='black', width=5)
    
    # Add background elements
    draw.text((width//2-100, 100), "TEST MANGA PANEL", fill='black')
    
    return manga


def process_your_manga(manga_path, dialogues, confidence=0.25):
    """
    Process your own manga image with YOLO detection.
    
    Args:
        manga_path: Path to your manga file
        dialogues: List of dialogue strings for each detected person
        confidence: Detection confidence threshold (lower = more detections)
    
    Example:
        process_your_manga('my_manga.png', 
                          ['Hello!', 'How are you?', 'Great!'],
                          confidence=0.3)
    """
    print(f"Processing: {manga_path}")
    
    # Initialize detector
    detector = MangaPersonDetector(confidence=confidence)
    
    # Detect people
    detections = detector.detect_people(manga_path, visualize=True)
    
    if not detections:
        print("⚠️  No people detected.")
        print("Try:")
        print("  - Lower confidence (e.g., confidence=0.15)")
        print("  - Check if image has visible people/characters")
        return None
    
    # Add bubbles
    result = add_bubbles_to_detected_people(
        manga_path,
        detections,
        dialogues,
        output_path=f'output_{Path(manga_path).name}'
    )
    
    return result


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # Process provided manga file
        manga_file = sys.argv[1]
        dialogues = sys.argv[2:] if len(sys.argv) > 2 else ["Test dialogue"]
        
        print(f"Processing: {manga_file}")
        print(f"Dialogues: {dialogues}")
        process_your_manga(manga_file, dialogues)
    else:
        # Run demo
        demo_yolo_detection()
        
        print("\n" + "="*70)
        print("💡 TIP: Process your own manga:")
        print("="*70)
        print("\n  python3 yolo_manga_detector.py my_manga.png 'Text 1' 'Text 2' 'Text 3'")
        print()
        print("Or in your code:")
        print("""
from yolo_manga_detector import process_your_manga

process_your_manga('my_manga.png', 
                   ['Hello!', 'How are you?', 'Great!'],
                   confidence=0.3)
""")

