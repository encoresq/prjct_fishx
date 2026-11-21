LIGHT_THEME = """
QWidget {
    background-color: #f5f6f8;
    color: #252a31;
    font-family: "Segoe UI", "Arial";
    font-size: 10pt;
    selection-background-color: #dce8f2;
    selection-color: #202832;
}
QMainWindow, QDialog, QWidget#centralwidget { background: #f5f6f8; }
QStackedWidget, QWidget#page_places, QWidget#page_icon, QWidget#page_rating {
    background: #ffffff; border: 1px solid #e5e8ed; border-radius: 14px;
}
QLabel { color: #303640; background: transparent; }
QLabel#label_6, QLabel#label_5, QLabel#label {
    color: #202630; font-size: 18pt; font-weight: 700; padding: 12px 8px;
}
QLabel#label_2, QLabel#label_3, QLabel#label_4 {
    background: #edf1f5; border: 1px solid #e2e7ed; border-radius: 12px;
    padding: 6px;
}
QPushButton {
    background: #ffffff; color: #303640; border: 1px solid #e1e5ea;
    border-radius: 9px; padding: 9px 14px; min-height: 20px;
}
QPushButton:hover { background: #eef2f6; border-color: #c8d2dd; }
QPushButton:pressed { background: #e3eaf1; }
QPushButton#pushButton_4, QPushButton#pushButton_3, QPushButton#pushButton_2 {
    text-align: left; min-width: 145px; padding: 12px 14px;
    background: transparent; border: 1px solid transparent;
}
QPushButton#pushButton_4:hover, QPushButton#pushButton_3:hover,
QPushButton#pushButton_2:hover { background: #e9eef3; border-color: #dce3ea; }
QPushButton#pushButton { background: #e8edf2; border: 1px solid #d9e0e7; font-weight: 600; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDateEdit {
    background: #ffffff; color: #252a31; border: 1px solid #dce1e7;
    border-radius: 8px; padding: 8px 10px;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus { border: 1px solid #9aabbc; }
QTableView, QTableWidget {
    background: #ffffff; alternate-background-color: #f5f7f9; color: #303640;
    gridline-color: #e6e9ed; border: 1px solid #e3e7eb; border-radius: 9px;
    selection-background-color: #e1eaf2; selection-color: #202832;
}
QHeaderView::section { background: #f0f3f6; color: #39424d; border: none;
    border-bottom: 1px solid #dce2e8; padding: 9px; font-weight: 600; }
QMenuBar, QMenu { background: #ffffff; color: #303640; border: 1px solid #e2e6eb; padding: 5px; }
QMenuBar::item, QMenu::item { padding: 7px 14px; border-radius: 6px; }
QMenuBar::item:selected, QMenu::item:selected { background: #edf1f5; }
QStatusBar { background: #f0f2f5; color: #68717d; border-top: 1px solid #e2e6eb; }
QScrollBar:vertical { background: #f1f3f5; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: #c5cdd6; border-radius: 5px; min-height: 25px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #f1f3f5; height: 10px; margin: 2px; }
QScrollBar::handle:horizontal { background: #c5cdd6; border-radius: 5px; min-width: 25px; }
QToolTip { background: #ffffff; color: #252a31; border: 1px solid #cbd3dc; padding: 5px; }
"""


DARK_THEME = """
QWidget {
    background-color: #151719; color: #e5e7e9;
    font-family: "Segoe UI", "Arial"; font-size: 10pt;
    selection-background-color: #3b4147; selection-color: #ffffff;
}
QMainWindow, QDialog, QWidget#centralwidget { background: #151719; }
QStackedWidget, QWidget#page_places, QWidget#page_icon, QWidget#page_rating {
    background: #1c1f22; border: 1px solid #2b3035; border-radius: 14px;
}
QLabel { color: #dfe2e5; background: transparent; }
QLabel#label_6, QLabel#label_5, QLabel#label {
    color: #f2f3f4; font-size: 18pt; font-weight: 650; padding: 12px 8px;
}
QLabel#label_2, QLabel#label_3, QLabel#label_4 {
    background: #eceff2; border: 1px solid #dfe3e7; border-radius: 12px;
    padding: 6px;
}
QPushButton {
    background: #24282c; color: #e5e7e9; border: 1px solid #343a40;
    border-radius: 9px; padding: 9px 14px; min-height: 20px;
}
QPushButton:hover { background: #2c3136; border-color: #50575e; }
QPushButton:pressed { background: #343a40; }
QPushButton:disabled { color: #777e85; background: #202326; }
QPushButton#pushButton_4, QPushButton#pushButton_3, QPushButton#pushButton_2 {
    text-align: left; min-width: 145px; padding: 12px 14px;
    background: transparent; border: 1px solid transparent;
}
QPushButton#pushButton_4:hover, QPushButton#pushButton_3:hover,
QPushButton#pushButton_2:hover { background: #24292d; border-color: #343a40; }
QPushButton#pushButton { background: #292e33; border: 1px solid #3a4148; font-weight: 600; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDateEdit {
    background: #202428; color: #e7e9eb; border: 1px solid #3a4148;
    border-radius: 8px; padding: 8px 10px;
}
QLineEdit:focus, QComboBox:focus, QTextEdit:focus { border: 1px solid #727c86; }
QTableView, QTableWidget {
    background: #1b1f22; alternate-background-color: #22272b; color: #e1e4e7;
    gridline-color: #30363c; border: 1px solid #30363c; border-radius: 9px;
    selection-background-color: #3a4249; selection-color: #ffffff;
}
QHeaderView::section { background: #252a2f; color: #d9dde1; border: none;
    border-bottom: 1px solid #414950; padding: 9px; font-weight: 600; }
QMenuBar, QMenu { background: #1c2024; color: #e5e7e9; border: 1px solid #343a40; padding: 5px; }
QMenuBar::item, QMenu::item { padding: 7px 14px; border-radius: 6px; }
QMenuBar::item:selected, QMenu::item:selected { background: #30363c; }
QStatusBar { background: #1b1f22; color: #929aa2; border-top: 1px solid #30363c; }
QScrollBar:vertical { background: #1b1f22; width: 10px; margin: 2px; }
QScrollBar::handle:vertical { background: #454d55; border-radius: 5px; min-height: 25px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #1b1f22; height: 10px; margin: 2px; }
QScrollBar::handle:horizontal { background: #454d55; border-radius: 5px; min-width: 25px; }
QToolTip { background: #292e33; color: #f2f3f4; border: 1px solid #50575e; padding: 5px; }
"""


OCEAN_THEME = """
QWidget {
    background-color: #101c2a;
    color: #e8f1f5;
    font-family: "Segoe UI", "Arial";
    font-size: 10pt;
    selection-background-color: #16a6a1;
    selection-color: #ffffff;
}
QMainWindow, QDialog { background-color: #101c2a; }
QWidget#centralwidget { background-color: #101c2a; }
QStackedWidget, QWidget#page_places, QWidget#page_icon, QWidget#page_rating {
    background-color: #172638;
    border: 1px solid #263b50;
    border-radius: 16px;
}
QLabel { color: #e8f1f5; background: transparent; }
QLabel#label_2, QLabel#label_3, QLabel#label_4 {
    background-color: #edf2f5;
    border: 1px solid #d6e0e7;
    border-radius: 12px;
    padding: 6px;
}
QLabel#label_6, QLabel#label_5, QLabel#label {
    color: #f4fbff;
    font-size: 19pt;
    font-weight: 700;
    padding: 14px 8px;
}
QPushButton {
    background-color: #20384d;
    color: #eaf7fa;
    border: 1px solid #31536a;
    border-radius: 10px;
    padding: 10px 16px;
    min-height: 20px;
    font-weight: 600;
}
QPushButton:hover { background-color: #28516a; border-color: #23b7ad; }
QPushButton:pressed { background-color: #147e82; }
QPushButton:disabled { color: #718494; background-color: #1a2937; }
QPushButton#pushButton_4, QPushButton#pushButton_3, QPushButton#pushButton_2 {
    text-align: left;
    min-width: 145px;
    padding: 13px 15px;
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 11px;
}
QPushButton#pushButton_4:hover, QPushButton#pushButton_3:hover,
QPushButton#pushButton_2:hover {
    background-color: #203c50;
    border-color: #31566b;
}
QPushButton#pushButton {
    background-color: #087f83;
    border: none;
    color: white;
}
QPushButton#pushButton:hover { background-color: #0b9998; }
QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDateEdit {
    background-color: #0d1722;
    color: #edf7fa;
    border: 1px solid #344b60;
    border-radius: 9px;
    padding: 9px 11px;
    selection-background-color: #087f83;
}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #21b8ad;
}
QLineEdit::placeholder { color: #8295a5; }
QTableView, QTableWidget {
    background-color: #122131;
    alternate-background-color: #192c3e;
    color: #e8f1f5;
    gridline-color: #2a4054;
    border: 1px solid #2b4358;
    border-radius: 10px;
    padding: 5px;
    selection-background-color: #176c70;
}
QHeaderView::section {
    background-color: #20384d;
    color: #dff7f5;
    border: none;
    border-bottom: 2px solid #16a6a1;
    padding: 10px 8px;
    font-weight: 700;
}
QTableCornerButton::section { background-color: #20384d; border: none; }
QMenuBar { background-color: #0c1722; color: #e8f1f5; padding: 5px; }
QMenuBar::item { background: transparent; padding: 8px 12px; border-radius: 7px; }
QMenuBar::item:selected { background-color: #20384d; }
QMenu { background-color: #172638; color: #e8f1f5; border: 1px solid #35516a; padding: 5px; }
QMenu::item { padding: 8px 28px 8px 12px; border-radius: 5px; }
QMenu::item:selected { background-color: #087f83; }
QStatusBar { background-color: #0c1722; color: #91a9b8; border-top: 1px solid #263b50; }
QScrollBar:vertical { background: #122131; width: 11px; margin: 2px; }
QScrollBar::handle:vertical { background: #36566b; min-height: 25px; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background: #16a6a1; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { background: #122131; height: 11px; margin: 2px; }
QScrollBar::handle:horizontal { background: #36566b; min-width: 25px; border-radius: 5px; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QToolTip { background-color: #20384d; color: #ffffff; border: 1px solid #16a6a1; padding: 6px; }
QMessageBox { background-color: #172638; }
"""
