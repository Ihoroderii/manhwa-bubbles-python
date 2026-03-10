"""Quick visual test: generates a bubble with the new smooth curved tail."""
from PIL import Image, ImageDraw
from manhwa_bubbles.speech_bubbles import draw_tail

W, H = 600, 400
img = Image.new("RGB", (W, H), "#f0f0f0")
draw = ImageDraw.Draw(img)

# Draw a simple oval bubble
cx, cy, rw, rh = 300, 130, 180, 90
draw.ellipse([cx - rw, cy - rh, cx + rw, cy + rh],
             fill="white", outline="black", width=3)

# Draw the new smooth tail pointing down (toward character)
draw_tail(draw, cx, cy + rh, direction="down", length=60, width=30)

# Add label
draw.text((cx - 80, cy - 15), "Smooth curved tail!", fill="black")
draw.text((10, 10), "Tail test - should be curved, not triangular", fill="gray")

img.save("tail_test_result.png")
print("Saved: tail_test_result.png")
print("Open it to verify the tail is smooth/curved, not a flat triangle.")
