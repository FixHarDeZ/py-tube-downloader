from __future__ import annotations

import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = name.strip(". ")
    return name[:200] or "video"


def build_output_template(output_folder: str, playlist_name: str | None = None) -> str:
    base = Path(output_folder)
    if playlist_name:
        base = base / sanitize_filename(playlist_name)
    return str(base / "%(title)s.%(ext)s")
