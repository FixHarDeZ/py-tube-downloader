import json
from pathlib import Path

_CONFIG_PATH = Path.home() / ".config" / "py-tube-downloader" / "settings.json"

_DEFAULTS: dict = {
    "output_folder": str(Path.home() / "Downloads"),
    "default_quality": "best",
    "default_format": "mp4",
    "max_concurrent": 3,
    "language": "en",
}


def load() -> dict:
    if _CONFIG_PATH.exists():
        try:
            with _CONFIG_PATH.open() as f:
                data = json.load(f)
            return {**_DEFAULTS, **data}
        except (json.JSONDecodeError, OSError):
            pass
    return dict(_DEFAULTS)


def save(settings: dict) -> None:
    _CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _CONFIG_PATH.open("w") as f:
        json.dump(settings, f, indent=2)
