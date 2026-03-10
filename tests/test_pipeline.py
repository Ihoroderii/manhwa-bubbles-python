"""Tests for manhwa_bubbles.pipeline (end-to-end)."""
import os
import tempfile
import pytest
from PIL import Image

from manhwa_bubbles.pipeline import (
    PipelineResult,
    process_manga_page,
    process_panel,
    process_all_panels,
)
from manhwa_bubbles.scenario_parser import parse_scenario


@pytest.fixture
def tmp_panel(tmp_path):
    """Create a simple white panel image and return its path."""
    img = Image.new("RGB", (800, 1200), "white")
    path = str(tmp_path / "panel.png")
    img.save(path)
    return path


BASIC_SCENARIO = {
    "panels": [{
        "panel_id": 1,
        "image": "panel.png",
        "dialogues": [
            {"character": "A", "text": "Hello world!", "emotion": "normal"},
            {"character": "B", "text": "Goodbye!", "emotion": "sad"},
        ],
    }]
}

MIXED_SCENARIO = {
    "panels": [{
        "panel_id": 1,
        "image": "panel.png",
        "dialogues": [
            {"character": "Hero", "text": "Attack!", "emotion": "shouting"},
            {"character": "Narrator", "text": "It was a dark day.", "emotion": "narration"},
            {"character": "Ghost", "text": "Boo...", "emotion": "ghost"},
        ],
    }]
}


class TestProcessMangaPage:
    def test_produces_output_file(self, tmp_panel, tmp_path):
        out = str(tmp_path / "result.png")
        result = process_manga_page(
            tmp_panel, BASIC_SCENARIO, output_path=out,
            use_yolo=False, seed=1,
        )
        assert isinstance(result, PipelineResult)
        assert os.path.exists(out)

    def test_output_is_valid_image(self, tmp_panel, tmp_path):
        out = str(tmp_path / "result.png")
        process_manga_page(
            tmp_panel, BASIC_SCENARIO, output_path=out,
            use_yolo=False, seed=1,
        )
        img = Image.open(out)
        assert img.size[0] == 800
        assert img.size[1] == 1200

    def test_placements_count_matches_dialogues(self, tmp_panel, tmp_path):
        out = str(tmp_path / "result.png")
        result = process_manga_page(
            tmp_panel, BASIC_SCENARIO, output_path=out,
            use_yolo=False, seed=1,
        )
        assert len(result.placements) == 2

    def test_default_output_path(self, tmp_panel):
        result = process_manga_page(
            tmp_panel, BASIC_SCENARIO,
            use_yolo=False, seed=1,
        )
        assert result.output_path.endswith("_bubbles.png")
        assert os.path.exists(result.output_path)
        os.remove(result.output_path)

    def test_accepts_json_string(self, tmp_panel, tmp_path):
        import json
        out = str(tmp_path / "result.png")
        result = process_manga_page(
            tmp_panel, json.dumps(BASIC_SCENARIO), output_path=out,
            use_yolo=False, seed=1,
        )
        assert len(result.placements) == 2

    def test_mixed_emotions(self, tmp_panel, tmp_path):
        out = str(tmp_path / "result.png")
        result = process_manga_page(
            tmp_panel, MIXED_SCENARIO, output_path=out,
            use_yolo=False, seed=1,
        )
        assert len(result.placements) == 3
        emotions = [p.dialogue.emotion for p in result.placements]
        assert "shouting" in emotions
        assert "narration" in emotions
        assert "ghost" in emotions


class TestProcessAllPanels:
    def test_multiple_panels(self, tmp_path):
        for i in range(3):
            img = Image.new("RGB", (400, 600), "white")
            img.save(str(tmp_path / f"p{i}.png"))

        scenario = {
            "panels": [
                {
                    "panel_id": i + 1,
                    "image": f"p{i}.png",
                    "dialogues": [{"character": "X", "text": f"Line {i}", "emotion": "normal"}],
                }
                for i in range(3)
            ]
        }
        results = process_all_panels(
            scenario, image_dir=str(tmp_path), output_dir=str(tmp_path),
            use_yolo=False, seed=1,
        )
        assert len(results) == 3
        for r in results:
            assert os.path.exists(r.output_path)
