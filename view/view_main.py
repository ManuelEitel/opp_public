from view.view_login import ViewLogin


class ViewMain(object):

    def __init__(self):
        """
        ViewMain calls the ViewLogin, manages the changes from ViewLogin to MainWindowOperator and MainWindowSales \n
        self.widget: There the User Login is being shown \n
        self.main_window_operator: There the operator and admin control the application mostly \n
        self.main_window_sales: There the sales team controls the application mostly \n
        """

        self.view_login = ViewLogin()

    def _bind(self):
        login_button = self.control_login.btn_login
        login_button.clicked.connect(self.authenticate_user)

    def authenticate_user(self):
        #  ToDo: Shove this into the control_main_window_class and use db to check for pw and name (much later; v2.0)
        text = self.control_login.email.text()
        password = self.control_login.password.text()
        if self.is_operator(text_name=text, text_password=password):
            self.stacked_widget.close()
            self.model_main.current_rights = "Operator"
            self.model_main.update_rights_dict()  # self.rights_dict is updated to operator now.
            self.control_main_window = ControlMainwindow(self.model_main)
        else:
            print(f'THIS CASE STILL NEEDS TO BE IMPLEMENTED WITH THE FUNCTIONS RIGHT BENEATH THIS')

    def is_operator(self, text_name: str, text_password: str) -> bool:
        """
        Checks for name and password of operator -> then returns bool
        Done here this easy way, instead of a seperate db with passwords
        # ToDo: Make this good
        """
        if text_name == "ff" and text_password == "ff":
            return True
        else:
            return False

    def is_admin(self, text_name: str, text_password: str) -> bool:
        """
        Checks for name and password of operator -> then returns bool
        Done here this easy way, instead of a seperate db with passwords
        # ToDo: Make this good
        """
        if text_name == "asdf" and text_password == "asdf":
            return True
        else:
            return False

    def is_develop(self, text_name: str, text_password: str) -> bool:
        """
        Checks for name and password of operator -> then returns bool
        Done here this easy way, instead of a seperate db with passwords
        # ToDo: Make this good
        """
        if text_name == "dev" and text_password == "dev":
            return True
        else:
            return False

    def is_sales(self, text_name: str, text_password: str) -> bool:
        """
        Checks for name and password of operator -> then returns bool
        Done here this easy way, instead of a seperate db with passwords
        # ToDo: Make this good
        """
        if text_name == "sales" and text_password == "sales":
            return True
        else:
            return False
