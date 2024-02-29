from view.py_delete_user_admin import DeleteUserDialog
from databases.datatase_handler import Database


class ControlDeleteUserAdmin(object):

    def __init__(self, model, username):
        """ Works only at admin logged in """

        self.model = model
        self.username = username
        self.delete_user_dialog = None
        if self.model.current_rights == "admin":
            self.delete_user_dialog = DeleteUserDialog()
            self.delete_user_dialog.fill_table_with_entry(self.username)
            self.delete_user_dialog.show()

    def deletion_pressed_signal_fct(self, username: str):
        db = Database("databases/db_main.db")
        db.connect()
        print(f'username = {username}, type(username) = {type(username)}')
        statement_for_deprecation_change = """
                                            UPDATE table_users
                                            SET deprecated = "1"
                                            WHERE name = ?"""
        db.execute_query(query=statement_for_deprecation_change, params=(username,))
        db.close()
        self.delete_user_dialog.close()


