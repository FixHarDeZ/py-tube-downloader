from __future__ import annotations

import uuid
from collections import deque

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from src.downloader import DownloadWorker
from src.gui.components.progress_bar import DownloadItem
from src.gui.components.settings_panel import SettingsPanel
from src.gui.theme import APP_STYLE
from src.i18n import lang_manager, t
from src.utils import config as config_module


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._config = config_module.load()
        self._workers: dict[str, DownloadWorker] = {}
        self._items: dict[str, DownloadItem] = {}
        self._queue: deque[dict] = deque()

        lang_manager.set_lang(self._config.get("language", "en"))
        lang_manager.language_changed.connect(self._retranslate)

        QApplication.instance().setStyleSheet(APP_STYLE)
        self._build_ui()

    # ── UI construction ───────────────────────────────────────

    def _build_ui(self) -> None:
        central = QWidget()
        central.setStyleSheet("background: #F8F9FA;")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(12)

        # URL bar
        url_row = QHBoxLayout()
        url_row.setSpacing(8)
        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText(t("url_placeholder"))
        self._url_input.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #DADCE0;
                border-radius: 8px;
                padding: 8px 14px;
                background: white;
                font-size: 14px;
            }
            QLineEdit:focus { border-color: #1967D2; }
            QLineEdit:disabled { background: #F1F3F4; color: #9AA0A6; }
        """)
        self._url_input.returnPressed.connect(self._start)

        self._download_btn = QPushButton(t("download_btn"))
        self._download_btn.setObjectName("primary")
        self._download_btn.setFixedWidth(120)
        self._download_btn.clicked.connect(self._start)

        self._lang_btn = QPushButton(t("lang_btn"))
        self._lang_btn.setObjectName("secondary")
        self._lang_btn.setFixedWidth(105)
        self._lang_btn.clicked.connect(self._toggle_lang)

        url_row.addWidget(self._url_input, 1)
        url_row.addWidget(self._download_btn)
        url_row.addWidget(self._lang_btn)
        root.addLayout(url_row)

        # Settings card
        self._settings = SettingsPanel(self._config)
        self._settings.folder_changed.connect(self._on_folder_changed)
        root.addWidget(self._settings)

        # Downloads section
        self._downloads_label = QLabel(t("downloads_label"))
        self._downloads_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #5F6368; padding: 2px 0;")
        root.addWidget(self._downloads_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._list_widget = QWidget()
        self._list_widget.setStyleSheet("background: transparent;")
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self._list_layout.setSpacing(6)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        scroll.setWidget(self._list_widget)
        root.addWidget(scroll, 1)

        self.setWindowTitle(t("app_title"))
        self.setMinimumSize(700, 540)
        self.statusBar().showMessage(t("ready_status"))

    # ── Language ──────────────────────────────────────────────

    def _toggle_lang(self) -> None:
        lang_manager.toggle()
        self._config["language"] = lang_manager.lang
        config_module.save(self._config)

    def _retranslate(self) -> None:
        self.setWindowTitle(t("app_title"))
        self._url_input.setPlaceholderText(t("url_placeholder"))
        self._download_btn.setText(t("download_btn"))
        self._lang_btn.setText(t("lang_btn"))
        self._downloads_label.setText(t("downloads_label"))
        msg = self.statusBar().currentMessage()
        if not msg or msg in ("Ready", "พร้อม"):
            self.statusBar().showMessage(t("ready_status"))

    # ── Download flow ─────────────────────────────────────────

    def _start(self) -> None:
        url = self._url_input.text().strip()
        if not url:
            return

        task_id = str(uuid.uuid4())
        item = DownloadItem(task_id, url)
        item.cancel_requested.connect(self._cancel_task)
        self._list_layout.addWidget(item)
        self._items[task_id] = item
        self._queue.append({"task_id": task_id, "url": url})

        self._url_input.clear()
        self.statusBar().showMessage(t("queued_status"))
        self._drain_queue()

    def _drain_queue(self) -> None:
        max_concurrent: int = self._config.get("max_concurrent", 3)
        while self._queue and len(self._workers) < max_concurrent:
            self._launch_worker(self._queue.popleft())

    def _launch_worker(self, task: dict) -> None:
        worker = DownloadWorker(
            task_id=task["task_id"],
            url=task["url"],
            output_folder=self._settings.output_folder,
            fmt=self._settings.format,
            quality=self._settings.quality,
            write_subs=self._settings.write_subs,
        )
        worker.progress.connect(self._on_progress)
        worker.finished.connect(self._on_finished)
        worker.error.connect(self._on_error)
        self._workers[task["task_id"]] = worker
        worker.start()

    # ── Worker handlers ───────────────────────────────────────

    def _on_progress(self, task_id: str, percent: int, speed: str) -> None:
        if item := self._items.get(task_id):
            item.update_progress(percent, speed)

    def _on_finished(self, task_id: str) -> None:
        if item := self._items.get(task_id):
            item.set_finished()
        self._workers.pop(task_id, None)
        self._drain_queue()
        self._update_status()
        self._save_config()

    def _on_error(self, task_id: str, message: str) -> None:
        if item := self._items.get(task_id):
            item.set_error(message)
        self._workers.pop(task_id, None)
        self._drain_queue()
        self._update_status()

    def _cancel_task(self, task_id: str) -> None:
        if worker := self._workers.get(task_id):
            worker.cancel()
        else:
            self._queue = deque(task for task in self._queue if task["task_id"] != task_id)
            if item := self._items.get(task_id):
                item.set_cancelled()

    # ── Helpers ───────────────────────────────────────────────

    def _on_folder_changed(self, folder: str) -> None:
        self._config["output_folder"] = folder
        self._save_config()

    def _update_status(self) -> None:
        active = len(self._workers)
        queued = len(self._queue)
        if active or queued:
            self.statusBar().showMessage(t("active_queued_status", active=active, queued=queued))
        else:
            self.statusBar().showMessage(t("all_complete_status"))

    def _save_config(self) -> None:
        self._config["default_format"] = self._settings.format
        self._config["default_quality"] = self._settings.quality
        self._config["output_folder"] = self._settings.output_folder
        self._config["language"] = lang_manager.lang
        config_module.save(self._config)

    def closeEvent(self, event) -> None:
        for worker in list(self._workers.values()):
            worker.cancel()
            worker.wait(2000)
        self._save_config()
        super().closeEvent(event)
