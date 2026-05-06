from __future__ import annotations

import re
from pathlib import Path


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "_", name)
    name = name.strip(". ")
    return name[:200] or "video"


def build_output_template(output_folder: str) -> str:
    return str(Path(output_folder) / "%(title)s.%(ext)s")
