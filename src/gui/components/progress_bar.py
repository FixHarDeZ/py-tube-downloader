from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.gui.theme import CANCELLED, ERROR, PRIMARY, SUCCESS, TEXT_MUTED
from src.i18n import lang_manager, t

_STRIP_RADIUS = "border-radius: 10px 0 0 10px;"


class DownloadItem(QFrame):
    cancel_requested = pyqtSignal(str)  # task_id

    def __init__(self, task_id: str, title: str, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self._state = "downloading"
        self._error_msg = ""

        self.setObjectName("download_card")
        self.setStyleSheet("""
            QFrame#download_card {
                background: white;
                border: 1px solid #E8EAED;
                border-radius: 10px;
            }
        """)

        # ── Layout: status strip + content ──────────────────
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 10, 0)
        row.setSpacing(0)

        self._strip = QFrame()
        self._strip.setFixedWidth(5)
        self._strip.setMinimumHeight(52)
        self._set_strip(PRIMARY)
        row.addWidget(self._strip)

        body = QWidget()
        body.setStyleSheet("background: transparent;")
        col = QVBoxLayout(body)
        col.setContentsMargins(12, 8, 0, 8)
        col.setSpacing(6)

        # title row
        title_row = QHBoxLayout()
        title_row.setSpacing(8)

        self._title_lbl = QLabel(title)
        self._title_lbl.setStyleSheet("font-weight: 600; font-size: 13px; background: transparent;")
        self._title_lbl.setMaximumWidth(460)

        self._speed_lbl = QLabel("")
        self._speed_lbl.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px; background: transparent;")

        self._cancel_btn = QPushButton("✕")
        self._cancel_btn.setObjectName("cancel_btn")
        self._cancel_btn.setFixedSize(22, 22)
        self._cancel_btn.setToolTip(t("cancel_tooltip"))
        self._cancel_btn.clicked.connect(lambda: self.cancel_requested.emit(self.task_id))

        title_row.addWidget(self._title_lbl, 1)
        title_row.addWidget(self._speed_lbl)
        title_row.addWidget(self._cancel_btn)

        # progress bar
        self._progress = QProgressBar()
        self._progress.setRange(0, 100)
        self._progress.setValue(0)
        self._progress.setTextVisible(False)
        self._progress.setFixedHeight(5)

        col.addLayout(title_row)
        col.addWidget(self._progress)
        row.addWidget(body, 1)

        lang_manager.language_changed.connect(self._retranslate)

    # ── Public API ───────────────────────────────────────────

    def update_progress(self, percent: int, speed: str) -> None:
        self._progress.setValue(percent)
        self._speed_lbl.setText(speed)

    def set_finished(self) -> None:
        self._state = "done"
        self._progress.setObjectName("bar_success")
        self._progress.setStyle(self._progress.style())
        self._progress.setValue(100)
        self._speed_lbl.setText(t("done_label"))
        self._speed_lbl.setStyleSheet(f"color: {SUCCESS}; font-size: 11px; font-weight: 600; background: transparent;")
        self._set_strip(SUCCESS)
        self._cancel_btn.setEnabled(False)

    def set_error(self, message: str) -> None:
        self._state = "error"
        self._error_msg = message
        self._apply_error()

    def set_cancelled(self) -> None:
        self._state = "cancelled"
        self._progress.setObjectName("bar_cancelled")
        self._progress.setStyle(self._progress.style())
        self._speed_lbl.setText(t("cancelled_label"))
        self._speed_lbl.setStyleSheet(f"color: {CANCELLED}; font-size: 11px; background: transparent;")
        self._set_strip(CANCELLED)
        self._cancel_btn.setEnabled(False)

    # ── Internals ────────────────────────────────────────────

    def _apply_error(self) -> None:
        self._progress.setObjectName("bar_error")
        self._progress.setStyle(self._progress.style())
        short = self._error_msg[:55] + "…" if len(self._error_msg) > 55 else self._error_msg
        self._speed_lbl.setText(t("error_label"))
        self._speed_lbl.setStyleSheet(f"color: {ERROR}; font-size: 11px; font-weight: 600; background: transparent;")
        self._title_lbl.setToolTip(short)
        self._set_strip(ERROR)
        self._cancel_btn.setEnabled(False)

    def _set_strip(self, color: str) -> None:
        self._strip.setStyleSheet(f"background: {color}; {_STRIP_RADIUS}")

    def _retranslate(self) -> None:
        self._cancel_btn.setToolTip(t("cancel_tooltip"))
        if self._state == "done":
            self._speed_lbl.setText(t("done_label"))
        elif self._state == "error":
            self._speed_lbl.setText(t("error_label"))
        elif self._state == "cancelled":
            self._speed_lbl.setText(t("cancelled_label"))
