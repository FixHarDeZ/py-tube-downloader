from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal

_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "app_title": "py-tube-downloader",
        "url_placeholder": "Paste YouTube video URL here…",
        "download_btn": "Download",
        "format_label": "Format",
        "quality_label": "Quality",
        "save_to_label": "Save to",
        "browse_btn": "Browse…",
        "subs_checkbox": "Download subtitles (EN / TH)",
        "downloads_label": "Downloads",
        "ready_status": "Ready",
        "queued_status": "Added to queue",
        "active_queued_status": "{active} active, {queued} queued",
        "all_complete_status": "All downloads complete",
        "error_fetch_title": "Error",
        "error_fetch_msg": "Could not fetch video info:\n\n{message}",
        "cancel_tooltip": "Cancel",
        "done_label": "Done",
        "error_label": "Error",
        "cancelled_label": "Cancelled",
        "select_folder_title": "Select output folder",
        "lang_btn": "ภาษาไทย",
    },
    "th": {
        "app_title": "py-tube-downloader",
        "url_placeholder": "วางลิงก์ YouTube วิดีโอที่นี่…",
        "download_btn": "ดาวน์โหลด",
        "format_label": "รูปแบบ",
        "quality_label": "คุณภาพ",
        "save_to_label": "บันทึกไปที่",
        "browse_btn": "เลือก…",
        "subs_checkbox": "ดาวน์โหลดคำบรรยาย (EN / TH)",
        "downloads_label": "รายการดาวน์โหลด",
        "ready_status": "พร้อม",
        "queued_status": "เพิ่มในคิวแล้ว",
        "active_queued_status": "กำลังดาวน์โหลด {active} รายการ, รอ {queued} รายการ",
        "all_complete_status": "ดาวน์โหลดเสร็จทั้งหมด",
        "error_fetch_title": "เกิดข้อผิดพลาด",
        "error_fetch_msg": "ไม่สามารถดึงข้อมูลวิดีโอได้:\n\n{message}",
        "cancel_tooltip": "ยกเลิก",
        "done_label": "เสร็จแล้ว",
        "error_label": "ผิดพลาด",
        "cancelled_label": "ยกเลิกแล้ว",
        "select_folder_title": "เลือกโฟลเดอร์ปลายทาง",
        "lang_btn": "English",
    },
}


class LanguageManager(QObject):
    language_changed = pyqtSignal()

    def __init__(self) -> None:
        super().__init__()
        self._lang = "en"

    @property
    def lang(self) -> str:
        return self._lang

    def set_lang(self, lang: str) -> None:
        if lang != self._lang and lang in _TRANSLATIONS:
            self._lang = lang
            self.language_changed.emit()

    def toggle(self) -> None:
        self.set_lang("th" if self._lang == "en" else "en")

    def t(self, key: str, **kwargs: object) -> str:
        text = _TRANSLATIONS[self._lang].get(key) or _TRANSLATIONS["en"].get(key) or key
        return text.format(**kwargs) if kwargs else text


lang_manager = LanguageManager()


def t(key: str, **kwargs: object) -> str:
    return lang_manager.t(key, **kwargs)
