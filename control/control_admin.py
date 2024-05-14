from view.py_adminView import AdminView
from view.py_newUser_adminsubView import AdminNewUserWidget
from databases.datatase_handler import Database
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore, Qt
from control.control_delete_user_admin_dialog import ControlDeleteUserAdmin


class ControlAdmin(object):

    def __init__(self, model):
        """
        Admin Rights are Initiated
            * AdminView is called here.
        """
        self.model = model
        self.adminView = AdminView()
        self.adminView.show()
        self.admin_newUser_subView = None
        self.rowCount = 0
        self.table = self.adminView.user_tableWidget  # must be before self._put_entries_in()
        self._bind()
        self._put_entries_in()
        self.delete_user_control = None
        # ToDo: Autolayout for the table missing.

    def _bind(self):
        self.adminView.make_user.connect(self.create_user)
        self.adminView.admin_cell_clicked.connect(self.delete_user)

    def _put_entries_in(self):
        db = Database("databases/db_main.db")
        db.connect()
        get_all_users = "SELECT * FROM table_users WHERE deprecated = 0;"

        rows = db.fetch_data(get_all_users)

        for element in rows:
            name = element[0]
            password = element[1]
            right = element[2]
            notes = element[3]
            deprecated = element[4]

            if deprecated == '0':
                self.put_entries_in_table(name, password, right, notes)

    def put_entries_in_table(self, name: str, password: str, rights: str, notes: str):

        self.rowCount += 1
        self.table.setRowCount(self.rowCount)
        element_list = [name, password, rights, notes]
        i = 0
        for entry in element_list:
            item = QTableWidgetItem(entry)
            self.table.setItem(self.rowCount-1, i, item)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            i += 1

    def create_user(self):
        self.admin_newUser_subView = AdminNewUserWidget()
        self.admin_newUser_subView.show()
        self.admin_newUser_subView.user_created_pressed.connect(self.put_user_in_db)

    def put_user_in_db(self, name: str, password: str, right: str):
        """
        comes from a signal: Prepares Database query and puts new user in db correctly.
        """
        if self.admin_newUser_subView is not None:
            if right not in self.model.rights_list:
                self.admin_newUser_subView.feedback_label.setText("Right doesn't exist.")
                return None
            elif name == "" or password == "" or right == "":
                self.admin_newUser_subView.feedback_label.setText("Empty cell.")
                return None
            else:
                self.admin_newUser_subView.close()
                db = Database("databases/db_main.db")
                db.connect()

                query = """INSERT INTO table_users (name, password, rights, notes, deprecated) 
                VALUES (?,?,?,?,?);"""
                params = (name, password, right, "None yet", "0")
                db.execute_query(query=query, params=params)
                db.close()
                self.create_user_db_and_table(name=name)
                self.update_user_table()

    @staticmethod
    def create_user_db_and_table(name: str):
        db = Database(f"databases/db_{name}_tasks.db")
        db.connect()
        query = """CREATE TABLE IF NOT EXISTS user_tasks (
                        date CHAR(30),
                        task CHAR(30),
                        workflow CHAR(30),
                        task_begin INT,
                        task_end INT,
                        order_name CHAR(30),
                        deprecated INT
                        )"""

        db.execute_query(query)
        db.close()

    def update_user_table(self):

        self.rowCount = 0

        db = Database("databases/db_main.db")
        db.connect()
        statement = "SELECT * FROM table_users WHERE deprecated = 0;"
        all_entries = db.fetch_data(statement)
        db.close()

        for element in all_entries:
            name = element[0]
            password = element[1]
            right = element[2]
            notes = element[3]
            deprecated = element[4]

            if deprecated == '0':
                self.put_entries_in_table(name, password, right, notes)

    def delete_user(self, row: int, column: int, mouse_button):
        username = self.table.item(row, 0).text()
        self.delete_user_control = ControlDeleteUserAdmin(model=self.model, username=username)
        self.delete_user_control.delete_user_dialog.deletion_pressed_signal.connect(self.delete_user_control.deletion_pressed_signal_fct)
        self.table.clear()
        self.update_user_table()
        #ToDo: Fix Bug: User Table after deletion of a user not immediately updated correctly.
