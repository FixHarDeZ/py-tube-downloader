from __future__ import annotations

import re

import yt_dlp
from PyQt6.QtCore import QThread, pyqtSignal

from src.utils.file_manager import build_output_template

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*[mGKHF]")


def _clean(text: str) -> str:
    return _ANSI_RE.sub("", text).strip()


# android_vr returns the full format list (144p–2160p) without GVS PO tokens.
# android/ios require GVS PO tokens for https adaptive streams (YouTube 2024+).
QUALITY_FORMATS: dict[str, str] = {
    "best": "bestvideo+bestaudio/b",
    "1080p": "bestvideo[height<=1080]+bestaudio/b[height<=1080]/b",
    "720p":  "bestvideo[height<=720]+bestaudio/b[height<=720]/b",
    "480p":  "bestvideo[height<=480]+bestaudio/b[height<=480]/b",
    "360p":  "bestvideo[height<=360]+bestaudio/b[height<=360]/b",
}


class DownloadWorker(QThread):
    progress = pyqtSignal(str, int, str)  # task_id, percent, speed
    finished = pyqtSignal(str)            # task_id
    error    = pyqtSignal(str, str)       # task_id, message

    def __init__(
        self,
        task_id: str,
        url: str,
        output_folder: str,
        fmt: str = "mp4",
        quality: str = "best",
        write_subs: bool = False,
        parent=None,
    ):
        super().__init__(parent)
        self.task_id = task_id
        self.url = url
        self.output_folder = output_folder
        self.fmt = fmt
        self.quality = quality
        self.write_subs = write_subs
        self._cancelled = False

    def cancel(self) -> None:
        self._cancelled = True

    def run(self) -> None:
        outtmpl = build_output_template(self.output_folder)

        ydl_opts: dict = {
            "outtmpl": outtmpl,
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "progress_hooks": [self._hook],
            "noplaylist": True,
            "extractor_args": {"youtube": {"player_client": ["android_vr", "web"]}},
        }

        if self.fmt == "mp3":
            ydl_opts["format"] = "bestaudio/b"
            ydl_opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        else:
            ydl_opts["format"] = QUALITY_FORMATS.get(self.quality, QUALITY_FORMATS["best"])
            ydl_opts["merge_output_format"] = "mp4"

        if self.write_subs:
            ydl_opts["writesubtitles"] = True
            ydl_opts["subtitleslangs"] = ["en", "th"]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            if not self._cancelled:
                self.finished.emit(self.task_id)
        except yt_dlp.utils.DownloadError as e:
            if not self._cancelled:
                self.error.emit(self.task_id, _clean(str(e)))
        except Exception as e:
            if not self._cancelled:
                self.error.emit(self.task_id, _clean(f"Unexpected error: {e}"))

    def _hook(self, d: dict) -> None:
        if self._cancelled:
            raise yt_dlp.utils.DownloadError("Cancelled by user")
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            percent = int(downloaded / total * 100) if total else 0
            speed = d.get("_speed_str", "").strip()
            self.progress.emit(self.task_id, percent, speed)
