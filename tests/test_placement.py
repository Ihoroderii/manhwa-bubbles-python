"""Tests for manhwa_bubbles.placement."""
import pytest
from manhwa_bubbles.placement import (
    BubblePlacement,
    Detection,
    Rect,
    build_name_to_detection_map,
    compute_placements,
    estimate_bubble_size,
    merge_detections,
    positions_to_detections,
)
from manhwa_bubbles.bubble_selector import select_bubble_style
from manhwa_bubbles.scenario_parser import CharacterPosition, DialogueEntry


class TestRect:
    def test_properties(self):
        r = Rect(10, 20, 100, 50)
        assert r.x2 == 110
        assert r.y2 == 70
        assert r.cx == 60
        assert r.cy == 45

    def test_overlaps_true(self):
        a = Rect(0, 0, 100, 100)
        b = Rect(50, 50, 100, 100)
        assert a.overlaps(b)

    def test_overlaps_false(self):
        a = Rect(0, 0, 50, 50)
        b = Rect(100, 100, 50, 50)
        assert not a.overlaps(b)

    def test_adjacent_no_overlap(self):
        a = Rect(0, 0, 50, 50)
        b = Rect(51, 0, 50, 50)
        assert not a.overlaps(b)


class TestDetection:
    def test_face_rect_centered_on_head(self):
        d = Detection(bbox=(100, 200, 300, 600), head=(200, 260))
        face = d.face_rect
        assert face.x < 200 < face.x + face.w
        assert face.y >= 260

    def test_face_rect_is_tight(self):
        d = Detection(bbox=(0, 0, 1000, 1000), head=(500, 150))
        face = d.face_rect
        assert face.w <= 150
        assert face.h <= 100

    def test_width_height(self):
        d = Detection(bbox=(0, 0, 100, 200), head=(50, 30))
        assert d.width == 100
        assert d.height == 200


class TestEstimateBubbleSize:
    def test_short_text(self):
        w, h = estimate_bubble_size("Hi", 800, 1200)
        assert w >= 180
        assert h >= 80

    def test_long_text_clamped(self):
        w, h = estimate_bubble_size("x" * 500, 800, 1200)
        assert w <= int(800 * 0.35)

    def test_min_dimensions(self):
        w, h = estimate_bubble_size("", 800, 1200, min_w=200, min_h=100)
        assert w >= 200
        assert h >= 100


class TestComputePlacements:
    def _make_entry(self, text="Hello!", emotion="normal", hint=None):
        return DialogueEntry(
            character="Test", text=text, emotion=emotion, position_hint=hint,
        )

    def _style(self, emotion="normal"):
        return select_bubble_style(emotion, seed=0)

    def test_single_speech_no_detection(self):
        entry = self._make_entry()
        placements = compute_placements(
            [(entry, self._style())], 800, 1200, seed=1,
        )
        assert len(placements) == 1
        p = placements[0]
        assert isinstance(p, BubblePlacement)
        assert p.rect.w > 0
        assert p.rect.h > 0

    def test_narration_goes_to_edge(self):
        entry = self._make_entry(text="Narration text", emotion="narration")
        placements = compute_placements(
            [(entry, self._style("narration"))], 800, 1200, seed=1,
        )
        p = placements[0]
        assert p.tail_target is None
        assert p.rect.y < 100 or p.rect.y > 1000

    def test_with_detection_has_tail(self):
        entry = self._make_entry(text="Speech", hint="left")
        det = Detection(bbox=(100, 400, 300, 900), head=(200, 475))
        placements = compute_placements(
            [(entry, self._style())], 800, 1200,
            detections=[det], seed=1,
        )
        p = placements[0]
        assert p.tail_target is not None
        assert p.tail_target == (200, 475)

    def test_no_face_overlap(self):
        entry = self._make_entry()
        det = Detection(bbox=(300, 300, 500, 800), head=(400, 375))
        placements = compute_placements(
            [(entry, self._style())], 800, 1200,
            detections=[det], seed=1,
        )
        p = placements[0]
        face = det.face_rect
        assert not p.rect.overlaps(face)

    def test_multiple_bubbles_no_overlap(self):
        entries = [
            (self._make_entry(f"Text {i}"), self._style())
            for i in range(3)
        ]
        dets = [
            Detection(bbox=(50 + i * 250, 400, 200 + i * 250, 900),
                      head=(125 + i * 250, 460))
            for i in range(3)
        ]
        placements = compute_placements(entries, 800, 1200, detections=dets, seed=1)
        rects = [p.rect for p in placements]
        for i in range(len(rects)):
            for j in range(i + 1, len(rects)):
                assert not rects[i].overlaps(rects[j]), (
                    f"Bubble {i} overlaps bubble {j}"
                )

    def test_bubble_within_image_bounds(self):
        entry = self._make_entry()
        det = Detection(bbox=(0, 0, 100, 200), head=(50, 30))
        placements = compute_placements(
            [(entry, self._style())], 800, 600,
            detections=[det], seed=42,
        )
        r = placements[0].rect
        assert r.x >= 0
        assert r.y >= 0
        assert r.x2 <= 800
        assert r.y2 <= 600

    def test_seed_reproducibility(self):
        entry = self._make_entry()
        args = ([(entry, self._style())], 800, 1200)
        a = compute_placements(*args, seed=99)
        b = compute_placements(*args, seed=99)
        assert a[0].rect.x == b[0].rect.x
        assert a[0].rect.y == b[0].rect.y

    def test_with_character_positions(self):
        """Bubbles should anchor near named characters."""
        hero_entry = DialogueEntry(character="Hero", text="Attack!", emotion="normal")
        villain_entry = DialogueEntry(character="Villain", text="Never!", emotion="normal")

        characters = [
            CharacterPosition(name="Hero", bbox=(50, 300, 200, 800), head=(125, 375)),
            CharacterPosition(name="Villain", bbox=(600, 300, 750, 800), head=(675, 375)),
        ]
        style = self._style()
        placements = compute_placements(
            [(hero_entry, style), (villain_entry, style)],
            1000, 1200,
            characters=characters,
            seed=42,
        )

        assert len(placements) == 2
        assert placements[0].tail_target is not None
        assert placements[1].tail_target is not None
        hero_cx = placements[0].rect.cx
        villain_cx = placements[1].rect.cx
        assert hero_cx < villain_cx, "Hero bubble should be left of Villain bubble"

    def test_character_name_matching(self):
        """Character names in dialogue match to positions by name."""
        entry = DialogueEntry(character="Alice", text="Hello!", emotion="normal")
        characters = [
            CharacterPosition(name="Bob", bbox=(50, 300, 200, 800)),
            CharacterPosition(name="Alice", bbox=(600, 300, 750, 800)),
        ]
        style = self._style()
        placements = compute_placements(
            [(entry, style)], 1000, 1200,
            characters=characters, seed=1,
        )
        assert placements[0].tail_target is not None
        assert placements[0].tail_target[0] > 500


class TestPositionsToDetections:
    def test_basic_conversion(self):
        chars = [
            CharacterPosition(name="A", bbox=(10, 20, 100, 200), head=(55, 47)),
        ]
        dets = positions_to_detections(chars)
        assert len(dets) == 1
        assert dets[0].bbox == (10, 20, 100, 200)
        assert dets[0].head == (55, 47)
        assert dets[0].confidence == 1.0

    def test_head_auto_estimated(self):
        chars = [CharacterPosition(name="A", bbox=(0, 0, 100, 200))]
        dets = positions_to_detections(chars)
        assert dets[0].head == (50, 30)

    def test_sorted_by_x(self):
        chars = [
            CharacterPosition(name="Right", bbox=(600, 0, 700, 200)),
            CharacterPosition(name="Left", bbox=(100, 0, 200, 200)),
        ]
        dets = positions_to_detections(chars)
        assert dets[0].head[0] < dets[1].head[0]


class TestMergeDetections:
    def test_no_overlap_merges_all(self):
        yolo = [Detection(bbox=(0, 0, 100, 200), head=(50, 30))]
        manual = [Detection(bbox=(500, 0, 600, 200), head=(550, 30))]
        merged = merge_detections(yolo, manual)
        assert len(merged) == 2

    def test_overlapping_keeps_yolo(self):
        yolo = [Detection(bbox=(0, 0, 100, 200), head=(50, 30), confidence=0.8)]
        manual = [Detection(bbox=(10, 10, 90, 190), head=(50, 30))]
        merged = merge_detections(yolo, manual)
        assert len(merged) == 1
        assert merged[0].confidence == 0.8

    def test_empty_inputs(self):
        assert merge_detections([], []) == []
        d = Detection(bbox=(0, 0, 100, 200), head=(50, 30))
        assert merge_detections([d], []) == [d]
        assert merge_detections([], [d]) == [d]


class TestBuildNameToDetectionMap:
    def test_maps_by_proximity(self):
        chars = [
            CharacterPosition(name="Left", bbox=(50, 0, 150, 200), head=(100, 30)),
            CharacterPosition(name="Right", bbox=(500, 0, 600, 200), head=(550, 30)),
        ]
        dets = [
            Detection(bbox=(40, 0, 160, 200), head=(100, 30)),
            Detection(bbox=(490, 0, 610, 200), head=(550, 30)),
        ]
        name_map = build_name_to_detection_map(chars, dets)
        assert name_map["left"] == 0
        assert name_map["right"] == 1
