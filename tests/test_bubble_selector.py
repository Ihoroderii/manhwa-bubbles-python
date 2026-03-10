"""Tests for manhwa_bubbles.bubble_selector."""
import pytest
from manhwa_bubbles.bubble_selector import (
    BubbleStyle,
    select_bubble_style,
    list_emotions,
    list_all_keywords,
    get_candidates,
    _resolve_alias,
)


class TestListEmotions:
    def test_returns_sorted_list(self):
        emotions = list_emotions()
        assert emotions == sorted(emotions)

    def test_no_aliases(self):
        emotions = list_emotions()
        assert "neutral" not in emotions  # alias of "normal"
        assert "normal" in emotions

    def test_all_keywords_superset(self):
        emotions = set(list_emotions())
        all_kw = set(list_all_keywords())
        assert emotions.issubset(all_kw)
        assert len(all_kw) > len(emotions)


class TestSelectBubbleStyle:
    def test_returns_bubble_style(self):
        result = select_bubble_style("normal", seed=1)
        assert isinstance(result, BubbleStyle)

    def test_deterministic_with_seed(self):
        a = select_bubble_style("shouting", seed=42)
        b = select_bubble_style("shouting", seed=42)
        assert a.name == b.name

    def test_unknown_emotion_falls_back_to_normal(self):
        result = select_bubble_style("xyzzy_nonexistent", seed=1)
        normal_candidates = get_candidates("normal")
        assert result.name in normal_candidates

    @pytest.mark.parametrize("emotion", [
        "normal", "shouting", "whispering", "thinking", "laughing",
        "crying", "scared", "narration", "magic", "horror",
        "digital", "sarcastic", "cold", "drunk", "sleepy",
        "romantic", "dark", "sfx", "echo", "telepathy", "ghost",
    ])
    def test_every_primary_emotion_returns_style(self, emotion):
        style = select_bubble_style(emotion, seed=0)
        assert style.name
        assert style.engine in ("pil", "cairo_circle", "cairo_square")

    def test_alias_resolves(self):
        a = get_candidates("angry")
        b = get_candidates("shouting")
        assert a == b

    def test_narration_uses_narrator_or_cairo(self):
        for seed in range(20):
            style = select_bubble_style("narration", seed=seed)
            assert style.name.startswith("narrator") or style.name.startswith("cairo")

    def test_prefer_cairo_false_excludes_cairo(self):
        for seed in range(30):
            style = select_bubble_style("laughing", seed=seed, prefer_cairo=False)
            assert style.engine == "pil"


class TestGetCandidates:
    def test_normal_has_candidates(self):
        c = get_candidates("normal")
        assert len(c) >= 1

    def test_shouting_has_multiple(self):
        c = get_candidates("shouting")
        assert len(c) >= 2

    def test_alias_works(self):
        assert get_candidates("yelling") == get_candidates("shouting")
