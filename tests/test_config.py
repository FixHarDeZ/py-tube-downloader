from pathlib import Path
from unittest.mock import patch

from src.utils import config as config_module


def test_load_returns_defaults_when_no_file():
    missing = Path("/nonexistent/__test__/settings.json")
    with patch.object(config_module, "_CONFIG_PATH", missing):
        cfg = config_module.load()
    assert "output_folder" in cfg
    assert "default_format" in cfg
    assert "default_quality" in cfg
    assert "max_concurrent" in cfg


def test_load_merges_saved_values_with_defaults(tmp_path):
    cfg_path = tmp_path / "settings.json"
    with patch.object(config_module, "_CONFIG_PATH", cfg_path):
        config_module.save({"output_folder": "/tmp/test", "default_format": "mp3"})
        loaded = config_module.load()
    assert loaded["output_folder"] == "/tmp/test"
    assert loaded["default_format"] == "mp3"
    # defaults still present for keys not saved
    assert "max_concurrent" in loaded


def test_load_falls_back_on_corrupt_json(tmp_path):
    cfg_path = tmp_path / "settings.json"
    cfg_path.write_text("not valid json")
    with patch.object(config_module, "_CONFIG_PATH", cfg_path):
        cfg = config_module.load()
    assert cfg == config_module._DEFAULTS


def test_save_creates_parent_dirs(tmp_path):
    nested = tmp_path / "a" / "b" / "c" / "settings.json"
    with patch.object(config_module, "_CONFIG_PATH", nested):
        config_module.save({"output_folder": "/tmp"})
    assert nested.exists()
