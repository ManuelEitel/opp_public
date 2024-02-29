from view.py_signUpView import SignUp


class ControlSignUpView:
    def __init__(self):

        self.signUp = SignUp()  # SignUp() is just the UI

        self._bind()

    def _bind(self):
        self.email_init = self.signUp.signUp_email
        self.password_init = self.signUp.signUp_password
        self.password_init_confirm = self.signUp.signUp_password2
        self.btn_signUp_init = self.signUp.signUp_button_login.clicked.connect(self.testfunction)
        self.userFeedback_init = self.signUp.label_signUpView_userFeedback

        self.btn_back_init = self.signUp.signUp_button_back.clicked.connect(self.call_Control_loginView)
        # lambda x: print(f'test')
        self.email_init.setText('sdf')

    def testfunction(self) -> None:
        print(f'testestet')

    def call_Control_loginView(self) -> None:
        """
        changes to login Field by -1 to the widget index
        """
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)


