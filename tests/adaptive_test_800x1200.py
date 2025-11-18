import cairo
from adaptive_bubbles import adaptive_circle_bubble, adaptive_square_bubble

PANEL_SIZE = (800,1200)  # width, height

TEST_TEXTS = [
    "QUIET WHISPER",
    "INTENSE ENERGY SURGE",
    "A VERY LONG LINE THAT SHOULD WRAP OR SHRINK"
]

VARIANTS = ['radial5','radial6','radial7']

def main():
    for idx, t in enumerate(TEST_TEXTS):
        base_slug = t.lower().replace(' ','_')[:30]
        for v in VARIANTS:
            tail_args = {}
            if idx == 0 and v == 'radial5':
                tail_args = {'tail_target': (200, 1000)}  # example speaker position
            surf, meta = adaptive_circle_bubble(t, variant=v, canvas_size=PANEL_SIZE, target_inner_padding=32,
                                                max_panel_fraction=0.3, min_font_size=14, wrap=True, max_lines=2,
                                                ensure_inside=True, whitespace_scale=1.6, auto_whitespace=True, **tail_args)
            out = f"adaptive_{base_slug}_{v}_800x1200.png"
            surf.write_to_png(out)
            print(out, meta)
        # square
        square_tail_args = {}
        if idx == 0:
            square_tail_args = {'tail_target': (650, 1050)}
        sq_surf, sq_meta = adaptive_square_bubble(t, canvas_size=PANEL_SIZE, target_inner_padding=28, aspect_ratio=1.3,
                                                  max_panel_fraction=0.3, min_font_size=14, wrap=True, max_lines=2,
                                                  ensure_inside=True, whitespace_scale=1.5, auto_whitespace=True, **square_tail_args)
        out_sq = f"adaptive_{base_slug}_square_800x1200.png"
        sq_surf.write_to_png(out_sq)
        print(out_sq, sq_meta)

if __name__ == '__main__':
    main()
