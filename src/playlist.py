from __future__ import annotations

import yt_dlp


def fetch_info(url: str) -> tuple[str, list[dict]]:
    """Return (playlist_title, entries) where each entry has keys: id, title, url.

    For a single video URL, playlist_title is empty and entries has one item.
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if info.get("_type") == "playlist":
        title = info.get("title") or "Playlist"
        entries = [
            {
                "id": e.get("id", ""),
                "title": e.get("title") or e.get("id", ""),
                "url": e.get("url") or f"https://www.youtube.com/watch?v={e['id']}",
            }
            for e in (info.get("entries") or [])
            if e
        ]
        return title, entries

    return "", [{"id": info["id"], "title": info.get("title", ""), "url": url}]
