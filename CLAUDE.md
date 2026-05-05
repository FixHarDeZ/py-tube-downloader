# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python desktop application for downloading YouTube videos and playlists. GUI built with PyQt6; download engine is `yt-dlp` using the `android_vr` player client.

## Setup & Commands

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt   # also needs ffmpeg system binary

python3 main.py                   # or ./run.sh (auto-creates venv)

pytest                            # run all tests
pytest tests/test_downloader.py::test_name   # single test
ruff check .                      # lint
ruff format .                     # format
```

## Architecture

```
py-tube-downloader/
├── main.py                              # Entry point
├── run.sh                               # Auto-venv launcher
├── src/
│   ├── downloader.py                    # yt-dlp wrapper + QThread worker
│   ├── playlist.py                      # Playlist metadata (flat extract)
│   ├── i18n.py                          # EN/TH singleton LanguageManager + t()
│   ├── gui/
│   │   ├── app.py                       # MainWindow — orchestrates all panels
│   │   ├── theme.py                     # APP_STYLE (QSS) + color constants
│   │   └── components/
│   │       ├── progress_bar.py          # DownloadItem card widget
│   │       └── settings_panel.py        # Format/quality/folder controls
│   └── utils/
│       ├── file_manager.py              # Output path + filename sanitize
│       └── config.py                    # Persistent settings (~/.config/…/settings.json)
└── tests/
```

### Key Design Decisions

**YouTube player client — `android_vr`:** YouTube's 2024 GVS PO-token enforcement blocks `android`/`ios` clients for adaptive streams (returns only 360p format 18). The `android_vr` client bypasses this and returns the full format list (144p–2160p) without requiring authentication or cookies.

**Threading model:** Downloads run in `QThread` workers. Each `DownloadWorker` emits `progress(str, int, str)`, `finished(str)`, and `error(str, str)` signals back to the main thread. `_FetchWorker` handles playlist metadata without blocking the GUI.

**Format selection:** `QUALITY_FORMATS` in `downloader.py` maps quality labels to yt-dlp format strings. `merge_output_format="mp4"` instructs ffmpeg to mux the result. MP3 uses `FFmpegExtractAudio` postprocessor.

**i18n:** `lang_manager` singleton in `src/i18n.py`. All widgets call `t("key")` for text and connect to `lang_manager.language_changed` to retranslate in place.

**Theme:** `src/gui/theme.py` exports `APP_STYLE` (QSS string) applied to `QApplication` at startup, plus color constants (`PRIMARY`, `SUCCESS`, `ERROR`, etc.) used by `progress_bar.py` for dynamic status strip colors.

**Config persistence:** `src/utils/config.py` reads/writes `~/.config/py-tube-downloader/settings.json` (output folder, quality, format, language).

## Dependencies

- `yt-dlp` — download engine
- `PyQt6` — GUI framework
- `ffmpeg` (system binary) — required for muxing and MP3 extraction
- `pytest` — testing
- `ruff` — linting/formatting
