from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore as qtc


class Login(QDialog):

    def __init__(self):
        """
        email entry field: loginView_email \n
        password entry field: loginView_password \n
        login button: loginView_btn_login \n
        label for user feedback: loginView_feedback \n
        sign up button: loginView_btn_signUp \n
        """
        super(Login, self).__init__()
        loadUi("view/ui_files/loginView.ui", self)

        self.loginView_password.setEchoMode(QtWidgets.QLineEdit.Password)  # make password text points






