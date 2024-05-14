from PyQt5 import QtWidgets, QtCore as qtc
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi


class ViewLogin(QDialog):

    btn_login_pressed = qtc.pyqtSignal(str, str)

    def __init__(self):
        """
        self.loginView_email: QLineEdit for entry username \n
        self.loginView_password: QLineEdit for entry password \n
        self.loginView_btn_login: QPushButton for confirmation \n
        self.loginView_feedback: QLabel for feedback from the app \n
        """
        super(ViewLogin, self).__init__()
        loadUi("view/ui_files/loginView.ui", self)

        self.loginView_password.setEchoMode(QtWidgets.QLineEdit.Password)  # make password text points
        self.username = None
        self.password = None

        self._bind()

    def _bind(self):

        self.loginView_btn_login.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        """
        Signal to ControlMain
        """
        self.username = self.loginView_email.text()
        self.password = self.loginView_password.text()
        self.btn_login_pressed.emit(self.username, self.password)


