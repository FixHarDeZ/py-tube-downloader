from src.utils.file_manager import build_output_template, sanitize_filename


def test_sanitize_removes_illegal_chars():
    result = sanitize_filename('file<>:"/\\|?*name')
    assert "<" not in result
    assert ">" not in result
    assert ":" not in result
    assert '"' not in result
    assert "\\" not in result
    assert "|" not in result
    assert "?" not in result
    assert "*" not in result


def test_sanitize_strips_leading_trailing_dots_and_spaces():
    assert sanitize_filename("  ..name..  ") == "name"


def test_sanitize_truncates_long_names():
    assert len(sanitize_filename("a" * 300)) <= 200


def test_sanitize_fallback_on_empty():
    assert sanitize_filename("...") == "video"
    assert sanitize_filename("   ") == "video"


def test_build_output_template():
    result = build_output_template("/downloads")
    assert result == "/downloads/%(title)s.%(ext)s"
