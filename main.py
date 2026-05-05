import sys

from PyQt6.QtWidgets import QApplication

from src.gui.app import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName("py-tube-downloader")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
