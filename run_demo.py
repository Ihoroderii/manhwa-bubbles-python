#!/usr/bin/env python3
"""Real end-to-end demo of the manga bubble pipeline.

Creates a manga panel with characters, defines a scenario, and runs the
full pipeline to produce a final page with auto-placed, emotion-styled bubbles.

Usage:
    python3 run_demo.py                         # uses built-in test panel
    python3 run_demo.py your_manga_image.png    # uses your own image
"""
import sys
import os
from PIL import Image, ImageDraw, ImageFont

from manhwa_bubbles.pipeline import process_manga_page, process_panel
from manhwa_bubbles.scenario_parser import parse_scenario
from manhwa_bubbles.bubble_selector import select_bubble_style, list_emotions


def create_manga_panel():
    """Draw a simple manga panel with 3 characters so placement has something to work with."""
    W, H = 1000, 1400
    img = Image.new("RGB", (W, H), "#f5f0e8")
    draw = ImageDraw.Draw(img)

    # Panel border
    draw.rectangle([20, 20, W - 20, H - 20], outline="black", width=4)

    # Background: simple gradient sky
    for y in range(21, 400):
        shade = int(180 + (y / 400) * 60)
        draw.line([(21, y), (W - 21, y)], fill=(shade, shade + 10, 255))

    # Ground
    draw.rectangle([21, 900, W - 21, H - 21], fill="#8B7355")
    draw.rectangle([21, 880, W - 21, 920], fill="#6B8E23")

    characters = [
        {"x": 220, "y": 650, "color": (70, 130, 200), "name": "Hero"},
        {"x": 500, "y": 700, "color": (180, 60, 60), "name": "Villain"},
        {"x": 780, "y": 660, "color": (100, 170, 100), "name": "Sidekick"},
    ]

    for ch in characters:
        x, y = ch["x"], ch["y"]
        c = ch["color"]
        darker = tuple(max(0, v - 40) for v in c)

        # Head
        draw.ellipse([x - 45, y - 90, x + 45, y + 10], fill=c, outline="black", width=2)
        # Eyes
        draw.ellipse([x - 20, y - 55, x - 8, y - 40], fill="white", outline="black")
        draw.ellipse([x + 8, y - 55, x + 20, y - 40], fill="white", outline="black")
        draw.ellipse([x - 16, y - 50, x - 12, y - 43], fill="black")
        draw.ellipse([x + 12, y - 50, x + 16, y - 43], fill="black")
        # Mouth
        draw.arc([x - 12, y - 30, x + 12, y - 15], start=0, end=180, fill="black", width=2)

        # Body
        draw.rectangle([x - 35, y + 10, x + 35, y + 160], fill=darker, outline="black", width=2)
        # Arms
        draw.line([x - 35, y + 30, x - 75, y + 100], fill="black", width=4)
        draw.line([x + 35, y + 30, x + 75, y + 100], fill="black", width=4)
        # Legs
        draw.line([x - 15, y + 160, x - 30, y + 250], fill="black", width=4)
        draw.line([x + 15, y + 160, x + 30, y + 250], fill="black", width=4)

    path = "demo_manga_panel.png"
    img.save(path)
    return path


DEMO_SCENARIO = {
    "panels": [{
        "panel_id": 1,
        "image": "demo_manga_panel.png",
        "characters": [
            {
                "name": "Hero",
                "bbox": [175, 560, 265, 900],
                "head": [220, 600],
            },
            {
                "name": "Villain",
                "bbox": [465, 610, 535, 860],
                "head": [500, 650],
            },
            {
                "name": "Sidekick",
                "bbox": [745, 570, 815, 910],
                "head": [780, 610],
            },
        ],
        "dialogues": [
            {
                "character": "Hero",
                "text": "We have to stop him before it's too late!",
                "emotion": "shouting",
                "position_hint": "left",
            },
            {
                "character": "Villain",
                "text": "Fools... you cannot comprehend my power.",
                "emotion": "dark",
                "position_hint": "center",
            },
            {
                "character": "Sidekick",
                "text": "I-I'm scared... but I'll fight!",
                "emotion": "simple",
                "position_hint": "right",
            },
            {
                "character": "Narrator",
                "text": "The final confrontation was about to begin...",
                "emotion": "narration",
            },
        ],
    }]
}


def run_demo(image_path=None):
    from manhwa_bubbles.placement import detect_characters

    print("=" * 60)
    print("  MANGA BUBBLE PIPELINE - LIVE DEMO")
    print("=" * 60)

    # Step 1: Get or create the panel image
    if image_path and os.path.exists(image_path):
        print(f"\nUsing your image: {image_path}")
    else:
        if image_path:
            print(f"\nImage not found: {image_path}")
        print("Creating demo manga panel...")
        image_path = create_manga_panel()
        print(f"  -> Saved: {image_path}")

    img = Image.open(image_path)
    print(f"  -> Size: {img.size[0]}x{img.size[1]}")

    # Step 2: Try YOLO detection
    print("\nRunning YOLO character detection...")
    yolo_dets = detect_characters(image_path, confidence=0.15)
    if yolo_dets:
        print(f"  YOLO found {len(yolo_dets)} character(s):")
        for i, d in enumerate(yolo_dets):
            print(f"    [{i}] bbox={d.bbox} head={d.head} conf={d.confidence:.2f}")
    else:
        print("  YOLO found 0 characters (using scenario character positions instead)")

    panel_data = DEMO_SCENARIO["panels"][0]
    chars = panel_data.get("characters", [])
    if chars:
        print(f"\n  Scenario provides {len(chars)} known character position(s):")
        for c in chars:
            print(f"    {c['name']:10s} bbox={c['bbox']} head={c.get('head', 'auto')}")

    # Step 3: Show the scenario
    print("\nScenario (what the LLM would generate):")
    for d in panel_data["dialogues"]:
        emotion = d.get("emotion", "normal")
        style = select_bubble_style(emotion, seed=0)
        print(f'  {d["character"]:10s} [{emotion:10s}] -> {style.name} ({style.engine})')
        print(f'  {"":10s} "{d["text"]}"')

    # Step 4: Run the pipeline (YOLO + manual positions merged automatically)
    print("\nRunning pipeline...")
    output_path = "demo_result.png"
    result = process_manga_page(
        image_path,
        DEMO_SCENARIO,
        output_path=output_path,
        use_yolo=True,
        seed=42,
    )

    # Step 5: Report results
    print(f"\nResult saved: {result.output_path}")
    print(f"Detections used: {len(result.detections)}")
    print(f"Bubbles placed: {len(result.placements)}")
    for p in result.placements:
        tail_info = ""
        if p.tail_target:
            tail_info = f" -> tail to ({p.tail_target[0]},{p.tail_target[1]})"
        print(f"  [{p.style.name:25s}] ({p.rect.x:4d},{p.rect.y:4d}) "
              f"{p.rect.w}x{p.rect.h}  \"{p.dialogue.text[:35]}...\"{tail_info}")

    print("\n" + "=" * 60)
    print(f"  Open {output_path} to see the result!")
    print("=" * 60)

    # Step 6: Show all available emotions
    print("\nAll supported emotions:")
    emotions = list_emotions()
    for i in range(0, len(emotions), 5):
        row = emotions[i:i+5]
        print("  " + ", ".join(row))


if __name__ == "__main__":
    user_image = sys.argv[1] if len(sys.argv) > 1 else None
    run_demo(user_image)
