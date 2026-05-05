from __future__ import annotations

PRIMARY    = "#1967D2"
SUCCESS    = "#1E8E3E"
ERROR      = "#D93025"
CANCELLED  = "#9AA0A6"
SURFACE    = "#FFFFFF"
BORDER     = "#E8EAED"
TEXT       = "#202124"
TEXT_MUTED = "#5F6368"

APP_STYLE = f"""
/* ── Buttons ──────────────────────────────────────────── */
QPushButton#primary {{
    background: {PRIMARY};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 22px;
    font-weight: bold;
    font-size: 13px;
}}
QPushButton#primary:hover   {{ background: #1557B0; }}
QPushButton#primary:pressed {{ background: #0F4C8F; }}
QPushButton#primary:disabled {{ background: #BDC1C6; color: white; }}

QPushButton#secondary {{
    border: 1.5px solid {BORDER};
    border-radius: 8px;
    padding: 7px 14px;
    font-weight: 600;
    font-size: 13px;
    color: {TEXT};
    background: {SURFACE};
}}
QPushButton#secondary:hover {{
    border-color: {PRIMARY};
    color: {PRIMARY};
    background: #F0F4FF;
}}
QPushButton#secondary:disabled {{
    color: {CANCELLED};
    border-color: {BORDER};
}}

QPushButton#cancel_btn {{
    border: none;
    background: transparent;
    color: #BDC1C6;
    border-radius: 4px;
    font-size: 12px;
    padding: 2px 5px;
    min-width: 0;
    min-height: 0;
}}
QPushButton#cancel_btn:hover {{
    background: #FCE8E6;
    color: {ERROR};
}}
QPushButton#cancel_btn:disabled {{ color: {BORDER}; }}

/* ── Progress bars ────────────────────────────────────── */
QProgressBar {{
    border: none;
    border-radius: 3px;
    background: #E8EAED;
    max-height: 5px;
    text-align: center;
    font-size: 0px;
}}
QProgressBar::chunk               {{ border-radius: 3px; background: {PRIMARY};   }}
QProgressBar#bar_success::chunk   {{ background: {SUCCESS};   }}
QProgressBar#bar_error::chunk     {{ background: {ERROR};     }}
QProgressBar#bar_cancelled::chunk {{ background: {CANCELLED}; }}

/* ── Scroll bar ───────────────────────────────────────── */
QScrollBar:vertical {{
    width: 6px;
    background: transparent;
    margin: 2px 0;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 30px;
}}
QScrollBar::handle:vertical:hover {{ background: {CANCELLED}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
QScrollBar::add-page:vertical,  QScrollBar::sub-page:vertical {{
    height: 0; background: none; border: none;
}}
QScrollArea {{ border: none; background: transparent; }}

/* ── Status bar ───────────────────────────────────────── */
QStatusBar {{
    border-top: 1px solid {BORDER};
    color: {TEXT_MUTED};
    font-size: 12px;
    padding: 2px 10px;
}}
"""
