import sqlite3
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from ui.ui_main import Ui_MainWindow
from themes import LIGHT_THEME, DARK_THEME, OCEAN_THEME
from html1 import HTML_CODE
from dialogs import SignInDialog, AddFishDialog, ProfileDialog
from config import base_path


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, login):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("FishSpot")
        self.login = login

        self.pushButton_4.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_icon)
        )
        self.pushButton_3.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_rating)
        )
        self.pushButton_2.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.page_places)
        )

        self.account_menu = self.menuBar().addMenu("Аккаунт")
        self.action_profile = self.account_menu.addAction("Профиль")
        self.action_add_fish = self.account_menu.addAction("Добавить улов")
        self.action_profile.triggered.connect(self.open_profile)
        self.action_add_fish.triggered.connect(self.open_add_fish)

        self._sign_in_dialog = None
        self._profile_dialog = None
        self._add_fish_dialog = None

        self.themes = {
            "light": ("Светлая", LIGHT_THEME),
            "dark": ("Тёмная", DARK_THEME),
            "ocean": ("Ocean", OCEAN_THEME),
        }
        self.theme_settings = QtCore.QSettings("FishSpot", "FishSpot")
        self.current_theme = self.theme_settings.value("theme", "light")
        if self.current_theme not in self.themes:
            self.current_theme = "light"

        self.theme_menu = QtWidgets.QMenu(self)
        self.theme_actions = {}
        for theme_key, (theme_title, _) in self.themes.items():
            action = self.theme_menu.addAction(theme_title)
            action.triggered.connect(
                lambda checked=False, key=theme_key: self.set_theme(key)
            )
            self.theme_actions[theme_key] = action

        self.pushButton.clicked.connect(self.show_theme_menu)
        self.set_theme(self.current_theme)

        self.widget.loadFinished.connect(self.on_map_loaded)
        self.widget.setHtml(HTML_CODE, baseUrl=QUrl("https://localhost"))
        self.get_rand_location()
        self.pushButton_3.clicked.connect(self.load_trofic)
        self.pushButton_4.clicked.connect(self.load_peoples)

    def load_peoples(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Имя", "Рыб поймано", "Общий вес"])

        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """SELECT user_info.login, COUNT(user_fishes.fish) AS total_count, COALESCE(SUM(user_fishes.weight), 0) AS total_weight
            FROM user_fishes
            LEFT JOIN user_info ON
            user_info.user_id = user_fishes.user_id
            WHERE user_fishes.is_delete = 0
            GROUP BY user_info.login
            ORDER BY total_weight DESC, total_count DESC"""

            res = cur.execute(query).fetchall()

            for line in res:
                items = [QStandardItem(str(field)) for field in line]
                model.appendRow(items)

            self.tableView_2.setModel(model)

            self.tableView_2.clicked.connect(self.people_row_cliked)

            self.tableView_2.setEditTriggers(
                QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
            )
            self.tableView_2.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch
            )

    def people_row_cliked(self, index):
        row = index.row()

        model = self.tableView_2.model()

        user_login = model.item(row, 0).text()

        self._profile_dialog = ProfileDialog(login=user_login, view=1)
        self._profile_dialog.exec()

    def load_trofic(self):
        pass

    def on_map_loaded(self, success):
        if not success:
            print("ne work")
            return

        self.get_rand_location()

    def get_rand_location(self):
        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            cur.execute("""SELECT ip, name 
            FROM locations
            ORDER BY RANDOM()
            LIMIT 1""")

            location = cur.fetchone()

            if location and location[0]:
                latitude, longitude = map(float, location[0].split(","))
                self.widget.page().runJavaScript(
                    f"window.showWaterbody({latitude}, {longitude}, '{location[1]}')"
                )

    def show_theme_menu(self):
        self.theme_menu.exec(
            self.pushButton.mapToGlobal(QtCore.QPoint(0, self.pushButton.height()))
        )

    def set_theme(self, theme_key):
        if theme_key not in self.themes:
            return
        self.current_theme = theme_key
        app = QtWidgets.QApplication.instance()
        if app is not None:
            app.setStyleSheet(self.themes[theme_key][1])
        self.pushButton.setText(f"Тема: {self.themes[theme_key][0]}  ▾")
        for key, action in self.theme_actions.items():
            action.setCheckable(True)
            action.setChecked(key == theme_key)
        self.theme_settings.setValue("theme", theme_key)

    def open_sign_in(self):
        self._sign_in_dialog = SignInDialog(self)
        self._sign_in_dialog.exec()

    def open_profile(self):
        self._profile_dialog = ProfileDialog(login=self.login)
        self._profile_dialog.exec()

    def open_add_fish(self):
        self._add_fish_dialog = AddFishDialog(self, login=self.login)
        self._add_fish_dialog.exec()
