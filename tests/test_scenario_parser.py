"""Tests for manhwa_bubbles.scenario_parser."""
import json
import pytest
from manhwa_bubbles.scenario_parser import (
    CharacterPosition,
    DialogueEntry,
    PanelData,
    Scenario,
    ScenarioParseError,
    parse_scenario,
)


VALID_SCENARIO = {
    "panels": [
        {
            "panel_id": 1,
            "image": "panel_001.png",
            "dialogues": [
                {
                    "character": "Hero",
                    "text": "Let's go!",
                    "emotion": "shouting",
                    "position_hint": "left",
                },
                {
                    "character": "Narrator",
                    "text": "And so it began...",
                    "emotion": "narration",
                },
            ],
        }
    ]
}


class TestParseScenario:
    def test_valid_dict(self):
        sc = parse_scenario(VALID_SCENARIO)
        assert isinstance(sc, Scenario)
        assert len(sc.panels) == 1

    def test_valid_json_string(self):
        sc = parse_scenario(json.dumps(VALID_SCENARIO))
        assert len(sc.panels) == 1

    def test_panel_fields(self):
        sc = parse_scenario(VALID_SCENARIO)
        panel = sc.panels[0]
        assert panel.panel_id == 1
        assert panel.image == "panel_001.png"
        assert len(panel.dialogues) == 2

    def test_dialogue_fields(self):
        sc = parse_scenario(VALID_SCENARIO)
        d = sc.panels[0].dialogues[0]
        assert d.character == "Hero"
        assert d.text == "Let's go!"
        assert d.emotion == "shouting"
        assert d.position_hint == "left"

    def test_narration_detected(self):
        sc = parse_scenario(VALID_SCENARIO)
        d = sc.panels[0].dialogues[1]
        assert d.is_narration()

    def test_speech_vs_narration_properties(self):
        sc = parse_scenario(VALID_SCENARIO)
        panel = sc.panels[0]
        assert len(panel.speech_dialogues) == 1
        assert len(panel.narration_dialogues) == 1


class TestEmotionNormalization:
    def test_unknown_emotion_becomes_normal(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "dialogues": [{"text": "Hi", "emotion": "xyzzy"}],
            }]
        }
        sc = parse_scenario(data)
        assert sc.panels[0].dialogues[0].emotion == "normal"

    def test_case_insensitive(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "dialogues": [{"text": "Hi", "emotion": "SHOUTING"}],
            }]
        }
        sc = parse_scenario(data)
        assert sc.panels[0].dialogues[0].emotion == "shouting"

    def test_default_emotion_is_normal(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "dialogues": [{"text": "Hi"}],
            }]
        }
        sc = parse_scenario(data)
        assert sc.panels[0].dialogues[0].emotion == "normal"


class TestPositionHint:
    def test_valid_hints(self):
        for hint in ("left", "right", "center", "top", "bottom"):
            data = {
                "panels": [{
                    "panel_id": 1, "image": "x.png",
                    "dialogues": [{"text": "Hi", "position_hint": hint}],
                }]
            }
            sc = parse_scenario(data)
            assert sc.panels[0].dialogues[0].position_hint == hint

    def test_invalid_hint_becomes_none(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "dialogues": [{"text": "Hi", "position_hint": "middle-nowhere"}],
            }]
        }
        sc = parse_scenario(data)
        assert sc.panels[0].dialogues[0].position_hint is None


class TestParseErrors:
    def test_invalid_json_string(self):
        with pytest.raises(ScenarioParseError, match="Invalid JSON"):
            parse_scenario("{not valid")

    def test_missing_panels_key(self):
        with pytest.raises(ScenarioParseError, match="Missing 'panels'"):
            parse_scenario({"dialogues": []})

    def test_panels_not_list(self):
        with pytest.raises(ScenarioParseError, match="must be a list"):
            parse_scenario({"panels": "not_a_list"})

    def test_empty_panels(self):
        with pytest.raises(ScenarioParseError, match="empty"):
            parse_scenario({"panels": []})

    def test_panel_missing_image(self):
        with pytest.raises(ScenarioParseError, match="image"):
            parse_scenario({"panels": [{"panel_id": 1, "dialogues": []}]})

    def test_dialogue_empty_text(self):
        with pytest.raises(ScenarioParseError, match="text"):
            parse_scenario({
                "panels": [{
                    "panel_id": 1, "image": "x.png",
                    "dialogues": [{"text": ""}],
                }]
            })

    def test_root_not_dict(self):
        with pytest.raises(ScenarioParseError):
            parse_scenario([1, 2, 3])


class TestCharacterPositions:
    def test_characters_parsed(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "characters": [
                    {"name": "Hero", "bbox": [10, 20, 100, 200], "head": [55, 47]},
                    {"name": "Villain", "bbox": [300, 20, 400, 200]},
                ],
                "dialogues": [{"text": "Hi"}],
            }]
        }
        sc = parse_scenario(data)
        panel = sc.panels[0]
        assert len(panel.characters) == 2
        assert panel.characters[0].name == "Hero"
        assert panel.characters[0].bbox == (10, 20, 100, 200)
        assert panel.characters[0].head == (55, 47)

    def test_head_auto_estimated(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "characters": [{"name": "A", "bbox": [0, 0, 100, 200]}],
                "dialogues": [{"text": "Hi"}],
            }]
        }
        sc = parse_scenario(data)
        c = sc.panels[0].characters[0]
        assert c.head is not None
        assert c.head == (50, 30)

    def test_no_characters_ok(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "dialogues": [{"text": "Hi"}],
            }]
        }
        sc = parse_scenario(data)
        assert sc.panels[0].characters == []

    def test_invalid_bbox_raises(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "characters": [{"name": "A", "bbox": [1, 2]}],
                "dialogues": [{"text": "Hi"}],
            }]
        }
        with pytest.raises(ScenarioParseError, match="bbox"):
            parse_scenario(data)

    def test_missing_name_raises(self):
        data = {
            "panels": [{
                "panel_id": 1, "image": "x.png",
                "characters": [{"bbox": [0, 0, 100, 200]}],
                "dialogues": [{"text": "Hi"}],
            }]
        }
        with pytest.raises(ScenarioParseError, match="name"):
            parse_scenario(data)
