from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi



class SignUp(QDialog):
    def __init__(self):
        """
        email entry field: signUp_email \n
        password entry field: signUp_password \n
        password confirmation field: signUp_password2 \n
        signUp button: signUp_button_login \n
        feedback label: label_signUpView_userFeedback \n
        back button: signUp_button_back
        """
        super(SignUp, self).__init__()
        loadUi("view/ui_files/signUpView.ui", self)
        self.signUp_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signUp_password2.setEchoMode(QtWidgets.QLineEdit.Password)

        # self.signUp_button_login.clicked.connect(self.signUpfunction)

        # self.signUp_button_back.clicked.connect(self.go_to_loginView)

    def signUpfunction(self):
        email = self.signUp_email.text()
        if self.signUp_password.text() == self.signUp_password2.text() and not self.signUp_password.text() == "":
            password = self.signUp_password.text()
            print(f'Signed up succesfully with email: {email} and password {password}')
            login = Login()
            login.label_userFeedback.setText("Succesfully created Account. Welcome!")
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex()+1)
        elif self.signUp_password.text() != self.signUp_password2.text():
            self.label_signUpView_userFeedback.setText("Password not matching!")

    def go_to_loginView(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)