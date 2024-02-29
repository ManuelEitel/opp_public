from PyQt5 import QtCore as qtc, Qt
from PyQt5.uic import loadUi
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt


class AdminNewUserWidget(QWidget):

    user_created_pressed = qtc.pyqtSignal(str, str, str)

    def __init__(self):
        """ That little window that admin uses to create a new user """

        super().__init__()

        loadUi("view/ui_files/admin_newUser.ui", self)
        self.setWindowModality(Qt.ApplicationModal)
        self._bind()

    def _bind(self):
        self.createBtn.clicked.connect(self.created_user)

    def created_user(self):
        user_name = self.newUser_name.text()
        password = self.newUser_password.text()
        user_rights = self.newUser_rights.text()
        self.user_created_pressed.emit(user_name, password, user_rights)

