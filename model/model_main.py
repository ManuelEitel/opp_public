class ModelMain(object):
    def __init__(self):

        """user_types: login_viewing_rights, Operator, User, Sales, Developer, Controller, CEO, Admin"""

        self.current_rights = "login_viewing_rights"

        self.rights_list = ["login_viewing_rights", "Operator", "User", "Sales",
                            "developer", "controller", "ceo", "admin"]

    def change_rights_to(self, rights: str):
        if rights in self.rights_list:
            self.current_rights = rights

