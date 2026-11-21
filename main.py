import sys
from PyQt6.QtWidgets import QApplication, QDialog
from PyQt6 import QtGui
from main_window import MainWindow
from dialogs import SignInDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    app.setFont(QtGui.QFont("Segoe UI", 10))

    sign_in = SignInDialog()

    if sign_in.exec() == QDialog.DialogCode.Accepted:
        login = sign_in.get_login()

        window = MainWindow(login=login)
        window.show()

        sys.exit(app.exec())

    else:
        sys.exit(0)
