from __future__ import annotations

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from src.i18n import lang_manager, t


class SettingsPanel(QFrame):
    folder_changed = pyqtSignal(str)

    def __init__(self, config: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_card")
        self.setStyleSheet("""
            QFrame#settings_card {
                background: white;
                border: 1px solid #E8EAED;
                border-radius: 12px;
            }
            QLabel { background: transparent; }
        """)

        layout = QFormLayout(self)
        layout.setContentsMargins(20, 14, 20, 14)
        layout.setHorizontalSpacing(16)
        layout.setVerticalSpacing(10)

        # Format
        self._fmt = QComboBox()
        self._fmt.addItems(["MP4", "MP3"])
        if config.get("default_format", "mp4").lower() == "mp3":
            self._fmt.setCurrentIndex(1)
        self._fmt_label = QLabel(t("format_label"))
        layout.addRow(self._fmt_label, self._fmt)

        # Quality
        self._quality = QComboBox()
        self._quality.addItems(["Best", "1080p", "720p", "480p", "360p"])
        q = config.get("default_quality", "best").lower()
        self._quality.setCurrentIndex({"best": 0, "1080p": 1, "720p": 2, "480p": 3, "360p": 4}.get(q, 0))
        self._quality_label = QLabel(t("quality_label"))
        layout.addRow(self._quality_label, self._quality)

        # Output folder
        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        self._folder = QLineEdit(config.get("output_folder", ""))
        self._folder.setPlaceholderText(t("save_to_label") + "…")
        self._browse = QPushButton(t("browse_btn"))
        self._browse.setObjectName("secondary")
        self._browse.setFixedWidth(90)
        self._browse.clicked.connect(self._pick_folder)
        folder_row.addWidget(self._folder, 1)
        folder_row.addWidget(self._browse)
        self._folder_label = QLabel(t("save_to_label"))
        layout.addRow(self._folder_label, folder_row)

        # Subtitles
        self._subs = QCheckBox(t("subs_checkbox"))
        layout.addRow("", self._subs)

        lang_manager.language_changed.connect(self._retranslate)

    def _pick_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, t("select_folder_title"), self._folder.text())
        if folder:
            self._folder.setText(folder)
            self.folder_changed.emit(folder)

    def _retranslate(self) -> None:
        self._fmt_label.setText(t("format_label"))
        self._quality_label.setText(t("quality_label"))
        self._folder_label.setText(t("save_to_label"))
        self._browse.setText(t("browse_btn"))
        self._subs.setText(t("subs_checkbox"))

    @property
    def format(self) -> str:
        return self._fmt.currentText().lower()

    @property
    def quality(self) -> str:
        return self._quality.currentText().lower()

    @property
    def output_folder(self) -> str:
        return self._folder.text()

    @property
    def write_subs(self) -> bool:
        return self._subs.isChecked()
