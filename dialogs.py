import sqlite3
import bcrypt
import uuid
import re
import os
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QHeaderView, QAbstractItemView
from ui.ui_dialogs import (
    Ui_Dialog_Sign,
    Ui_Dialog_User_Add_Fish,
    Ui_Dialog_Profile,
    Ui_Dialog_Registration,
    Ui_Dialog_Reset_Password,
    Ui_Dialog_Hotkeys,
)
from config import resource_path, base_path
from security import (
    is_safe_image,
    user_registration,
    check_user_registration,
    get_user_id,
)


class Hotkeys(QtWidgets.QDialog, Ui_Dialog_Hotkeys):
    def __init__(self, /, parent):
        super().__init__(parent)
        self.setupUi(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()


class SignInDialog(QtWidgets.QDialog, Ui_Dialog_Sign):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.FramelessWindowHint
        )

        self.label.setStyleSheet("font-size: 10pt; font-weight: normal; padding: 0;")
        self.label_2.setStyleSheet("font-size: 10pt; font-weight: normal; padding: 0;")
        self.setModal(True)
        self.line_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.btn_sign_in.clicked.connect(self.sign)
        self.btn_create_account.clicked.connect(self.accept)
        self.reset_password.setText('<a href="#">Забыли пароль?</a>')
        self.reset_password.linkActivated.connect(self.show_reset_message)

        self.btn_create_account.clicked.connect(self.open_registration)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.sign()
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def open_registration(self):
        self._register_dialog = UserRegistration(self)
        self._register_dialog.exec()

    def show_reset_message(self):
        self._reset = ResetPassword(self)
        self._reset.exec()

    def sign(self):
        login, password = self.line_login.text(), self.line_password.text()

        valid = check_user_registration(login, password)

        if valid:
            self.accept()
        else:
            QMessageBox.critical(self, "Ошибка", "что то введенно неправильно")
            return

    def get_login(self):
        return self.line_login.text()


class ResetPassword(QtWidgets.QDialog, Ui_Dialog_Reset_Password):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.btn_change.clicked.connect(self.btn_change_pushed)
        self.btn_close.clicked.connect(self.btn_close_pushed)
        self._register = SignInDialog(self)

    def btn_change_pushed(self):
        login = self.line_user_login.text()
        second_name = self.line_user_secon_name.text()
        new_password = self.line_new_password.text()
        new_password_repeat = self.line_repeat_new_password.text()

        if new_password != new_password_repeat:
            QMessageBox.critical(self, "Ошибка", "Пароли разные")
            return

        if len(new_password) < 4:
            QMessageBox.critical(self, "Ошибка", "Пароль слишком короткий")

        password = new_password.encode("utf-8")
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password, salt).decode("utf-8")

        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """SELECT user_info.login, user_info.second_name
            FROM user_info
            LEFT JOIN users ON
            users.user_login = user_info.login
            WHERE user_info.login = ? AND user_info.second_name = ?;"""

            user = cur.execute(
                query,
                (
                    login,
                    second_name,
                ),
            ).fetchone()

            if not user:
                QMessageBox.critical(self, "Ошибка", "Данные введены неверно")
                return

            query = """UPDATE users
            SET user_pass = ?
            WHERE user_login = ?"""

            cur.execute(
                query,
                (
                    hash_password,
                    login,
                ),
            ).fetchone()

        QMessageBox.information(self, "Успешно", "Ваш пароль сменён")

        self.accept()
        self._register.exec()

    def btn_close_pushed(self):
        self.reject()


class AddFishDialog(QtWidgets.QDialog, Ui_Dialog_User_Add_Fish):
    def __init__(self, parent=None, login=None):
        super().__init__(parent)
        self.setupUi(self)
        self.login = login
        self.btn_close_add.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.add_fish)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            self.add_fish()

    def add_fish(self):
        fish_name = self.line_fish_name_add.text().strip()
        location = self.line_location_ip.text().strip()
        fish_weight = self.fish_weight.text().strip()
        wobbler = self.box_combo_vobler.currentText()

        if not bool(re.match(r"^\d+\.\d+$", fish_weight)):
            QtWidgets.QMessageBox.warning(
                self, "Ошибка", "Некорректное написание веса рыбы"
            )
            return
        if not fish_name or not location:
            QtWidgets.QMessageBox.warning(
                self, "Не все данные заполнены", "Укажите рыбу и локацию."
            )
            return

        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """INSERT INTO user_fishes (user_id, location, fish, weight, wobbler) VALUES (?, ?, ?, ?, ?);"""

            user_id = get_user_id(self.login)

            cur.execute(
                query,
                (
                    user_id,
                    location,
                    fish_name,
                    fish_weight,
                    wobbler,
                ),
            ).fetchall()
            self.accept()


class ProfileDialog(QtWidgets.QDialog, Ui_Dialog_Profile):
    def __init__(self, login, view=0, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.login = login
        self.view = view
        self.btn_menu_user.clicked.connect(self.close)

        self.user_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.user_table.setSortingEnabled(True)
        self.user_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.btn_show_best_user.installEventFilter(self)
        self.btn_user_delete_fish.installEventFilter(self)
        self.btn_user_delete_fish.setText("🗑️")

        if self.view == 1:
            self.btn_add_user_fish.setVisible(False)
            self.btn_user_delete_fish.setVisible(False)

            self.user_table.setDragEnabled(False)
            self.user_table.setDragDropMode(QAbstractItemView.DragDropMode.NoDragDrop)

            self.btn_show_best_user.setAcceptDrops(False)
            self.btn_user_delete_fish.setAcceptDrops(False)
        else:
            self.btn_add_user_fish.setFixedSize(50, 120)
            self.btn_add_user_fish.setText("+")
            self.btn_add_user_fish.clicked.connect(self.open_add_fish)

            self.user_table.setDragEnabled(True)
            self.user_table.setDragDropMode(QAbstractItemView.DragDropMode.DragOnly)

            self.btn_show_best_user.setAcceptDrops(True)
            self.btn_show_best_user.clicked.connect(self.reset_show)
            self.btn_user_delete_fish.setAcceptDrops(True)
            self.valid_info()

        self.show_info()
        self.load_table()
        self.valid_info(view=self.view)

    def reset_show(self):
        pass

    def valid_info(self, view=0):
        try:
            _fish, _weight = self.btn_show_best_user.text().split("|")
            fish, weight = _fish.split()[-1], _weight.split()[-1]
        except:
            return
        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """SELECT COUNT(user_fishes.fish)
                       FROM user_fishes
                       LEFT JOIN user_info ON user_info.user_id = user_fishes.user_id
                       WHERE user_info.login = ? 
                         AND user_fishes.is_delete = 0 
                         AND user_fishes.fish = ? 
                         AND user_fishes.weight = ?"""

            res = cur.execute(
                query,
                (
                    self.login,
                    fish,
                    weight,
                ),
            ).fetchone()[0]

            if view == 0:
                if res == 0:
                    self.btn_show_best_user.setText("Выберите улов на показ")
                    query = """UPDATE user_info 
                            SET selected_fish = NULL, selected_fish_weight = NULL
                            WHERE login = ?;"""
                    cur.execute(query, (self.login,))
            if view == 1:
                if res == 0:
                    self.btn_show_best_user.setText("Пользователь не выбрал улов")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            cur_idx = self.user_table.currentIndex()
            if cur_idx.isValid():
                row = cur_idx.row()
                model = self.user_table.model()
                fish_data = str(model.index(row, 1).data())
                weight_data = str(model.index(row, 2).data())
                with sqlite3.connect(base_path("projectFish.db")) as con:
                    cur = con.cursor()
                    query = """
                    UPDATE user_fishes
                    SET is_delete = 1
                    WHERE rowid = (
                        SELECT rowid 
                        FROM user_fishes 
                        WHERE user_id = ? AND fish = ? AND weight = ? AND is_delete = 0
                        LIMIT 1
                    )
                    """
                    cur.execute(
                        query,
                        (
                            get_user_id(self.login),
                            fish_data,
                            weight_data,
                        ),
                    )

                self.load_table()
                self.show_info()
        if event.key() == Qt.Key.Key_Plus:
            self.open_add_fish()

    def open_add_fish(self):
        dialog = AddFishDialog(self, login=self.login)
        dialog.exec()
        self.load_table()
        self.show_info()

    def show_info(self):
        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """SELECT first_name, second_name, avatar, selected_fish, selected_fish_weight
            FROM user_info
            WHERE login = ?;"""

            res = cur.execute(query, (self.login,)).fetchone()

            name = f"{res[0]} {res[1]}"
            photo_path = res[2]

            if res[3]:
                self.btn_show_best_user.setText(f"Вид: {res[3]}  |  Вес: {res[4]}")

            query = """SELECT COUNT(user_fishes.fish) FROM user_fishes
            LEFT JOIN users ON users.user_id = user_fishes.user_id
            WHERE users.user_login = ? and user_fishes.is_delete = 0"""

            amount = cur.execute(query, (self.login,)).fetchone()

            query = """SELECT MAX(user_fishes.weight) FROM user_fishes
            LEFT JOIN users ON users.user_id = user_fishes.user_id
            WHERE users.user_login = ? and user_fishes.is_delete = 0"""

            max_weight = cur.execute(query, (self.login,)).fetchone()

            self.user_stats.setText(
                f"Всего рыб поймано - {amount[0]}  |  Максимальный вес рыбы - {max_weight[0]}"
            )

        self.user_photo.setPixmap(QtGui.QPixmap(photo_path))
        self.user_name.setText(name)

    def load_table(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Локация", "Рыба", "Вес"])

        with sqlite3.connect(base_path("projectFish.db")) as con:
            cur = con.cursor()

            query = """SELECT user_fishes.location, user_fishes.fish, user_fishes.weight
            from user_fishes
            LEFT JOIN users ON users.user_id = user_fishes.user_id
            WHERE users.user_login = ? and user_fishes.is_delete = 0
            ORDER BY user_fishes.weight DESC;"""

            res = cur.execute(query, (self.login,)).fetchall()

        for line in res:
            items = [QStandardItem(str(field)) for field in line]
            model.appendRow(items)

        self.user_table.setModel(model)

        self.user_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

    def eventFilter(self, obj, event):
        if self.view == 1:
            return super().eventFilter(obj, event)

        if obj is self.btn_show_best_user:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasText() or event.mimeData().hasFormat(
                    "application/x-qabstractitemmodeldatalist"
                ):
                    event.acceptProposedAction()
                    return True
            elif event.type() == QEvent.Type.Drop:
                cur_idx = self.user_table.currentIndex()
                if cur_idx.isValid():
                    row = cur_idx.row()
                    model = self.user_table.model()

                    fish_data = str(model.index(row, 1).data())
                    weight_data = str(model.index(row, 2).data())

                    self.btn_show_best_user.setText(
                        f"Вид: {fish_data}  |  Вес: {weight_data}"
                    )

                    with sqlite3.connect(base_path("projectFish.db")) as con:
                        cur = con.cursor()

                        query = """UPDATE user_info 
                        SET selected_fish = ?, selected_fish_weight = ?
                        WHERE login = ?;"""

                        cur.execute(
                            query,
                            (
                                fish_data,
                                weight_data,
                                self.login,
                            ),
                        ).fetchall()

                event.acceptProposedAction()
                return True
        elif obj is self.btn_user_delete_fish:
            if event.type() == QEvent.Type.DragEnter:
                if event.mimeData().hasText() or event.mimeData().hasFormat(
                    "application/x-qabstractitemmodeldatalist"
                ):
                    event.acceptProposedAction()
                    return True
            elif event.type() == QEvent.Type.Drop:
                cur_idx = self.user_table.currentIndex()
                if cur_idx.isValid():
                    row = cur_idx.row()
                    model = self.user_table.model()

                    fish_data = str(model.index(row, 1).data())
                    weight_data = str(model.index(row, 2).data())

                    with sqlite3.connect(base_path("projectFish.db")) as con:
                        cur = con.cursor()

                        query = """
                        UPDATE user_fishes
                        SET is_delete = 1
                        WHERE rowid = (
                            SELECT rowid 
                            FROM user_fishes 
                            WHERE user_id = ? AND fish = ? AND weight = ? AND is_delete = 0
                            LIMIT 1
                        )
                        """

                        cur.execute(
                            query,
                            (
                                get_user_id(self.login),
                                fish_data,
                                weight_data,
                            ),
                        )

                self.load_table()
                self.show_info()
                self.valid_info()
                event.acceptProposedAction()
                return True

        return super().eventFilter(obj, event)


class UserRegistration(QtWidgets.QDialog, Ui_Dialog_Registration):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowFlags(
            QtCore.Qt.WindowType.Tool | QtCore.Qt.WindowType.FramelessWindowHint
        )
        # стили потому что хз чето ломаются, скорее всего из за названия, но исправил как то так
        self.label.setStyleSheet(
            "font-size: 12pt; font-weight: normal; padding: 0; background: transparent; border: none;"
        )
        self.label_2.setStyleSheet(
            "font-size: 12pt; font-weight: normal; padding: 0; background: transparent; border: none;"
        )
        self.label_3.setStyleSheet(
            "font-size: 12pt; font-weight: normal; padding: 0; background: transparent; border: none;"
        )
        self.label_4.setStyleSheet(
            "font-size: 12pt; font-weight: normal; padding: 0; background: transparent; border: none;"
        )
        self.label_5.setStyleSheet(
            "font-size: 12pt; font-weight: normal; padding: 0; background: transparent; border: none;"
        )

        # default photo
        pix = QPixmap(resource_path("no-photo.png"))
        self.label_photo.setPixmap(pix)

        self.btn_select_photo.clicked.connect(self.select_photo)

        self.btn_close_reg.clicked.connect(self.close_register)

        self.btn_confirm_reg.clicked.connect(self.confirm_registration)

        self._sign_dialog = SignInDialog()

    def select_photo(self):
        self.photo_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фото", "", "Изображения (*.png *.jpg *.jpeg)"
        )

        valid = is_safe_image(self.photo_path)
        if not valid:
            return

        if self.photo_path:
            pix = QPixmap(self.photo_path)
            scale_pix = pix.scaled(
                self.label_photo.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            self.label_photo.setPixmap(scale_pix)

    def close_register(self):
        self.close()
        self._sign_dialog.exec()

    def confirm_registration(self):
        login = self.line_new_login.text().strip()
        password = self.line_new_password.text().strip()
        conf_password = self.line_repeat_password.text().strip()
        first_name = self.line_user_fisrt_name.text().strip()
        second_name = self.line_user_second_name.text().strip()
        user_photo = self.label_photo.pixmap()

        # valid
        if not login:
            QMessageBox.critical(self, "Ошибка", "Введите логин")
            return
        if len(password) < 4 or bool(re.search(r"\s", password)):
            QMessageBox.critical(self, "Ошибка", "Пароль не меньше 4 символов")
            return
        if password != conf_password:
            QMessageBox.critical(self, "Ошибка", "Пароли отличаются")
            return
        if not first_name:
            QMessageBox.critical(self, "Ошибка", "Ваше имя не заполнено")
            return
        if not second_name:
            QMessageBox.critical(self, "Ошибка", "Ваша фамилия не заполнена")
            return

        unique_file = f"{uuid.uuid4().hex}.png"
        full_path = os.path.join("avatars", unique_file)

        new_user_id = user_registration(login, password)

        if not new_user_id:
            QMessageBox.critical(
                self, "Ошибка", "Пользователь с таким логином уже существует"
            )
            if os.path.exists(full_path):
                os.remove(full_path)
            return

        try:
            with sqlite3.connect(base_path("projectFish.db")) as con:
                cur = con.cursor()
                query_info = """INSERT INTO user_info 
                                (user_id, login, first_name, second_name, avatar) 
                                VALUES (?, ?, ?, ?, ?)"""

                cur.execute(
                    query_info, (new_user_id, login, first_name, second_name, full_path)
                )
                con.commit()

                if user_photo and not user_photo.isNull():
                    user_photo.save(full_path, "PNG")

                QMessageBox.information(self, "Успех", "Вы успешно зарегистрированы!")
                self.accept()

                self._sign_dialog.exec()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка БД", f"Не удалось создать профиль: {e}")
