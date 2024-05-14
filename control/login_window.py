from control.control_mainwindow import ControlMainwindow
from databases.datatase_handler import Database
from control.control_user_tasks import ControlUserTasks


class ControlLoginView(object):
    def __init__(self, model, view):
        """
        Controls the behaviour of the login Window \n
        """
        self.model = model
        self.view = view
        self.view.view_login.show()
        self.view.view_login.btn_login_pressed.connect(self.login_clicked)
        self.main_window = None

    def login_clicked(self, username: str, password: str):
        """
        This function manages the transition from the login window to the main window and tells the mainwindow
        who is logging in, regarding what they are allowed to do (Roles and permissions)
        """
        self.set_up_db()

        if username == "" or password == "":
            self.view.view_login.loginView_feedback.setText("No valid input.")

        else:
            db = Database("databases/db_main.db")
            db.connect()
            select_query = "SELECT * FROM table_users WHERE name = ? AND password = ?;"
            params = (username, password)
            rows = db.fetch_data(select_query, params)
            if rows[0][2] in self.model.rights_list:
                """ Here the rights are being taken into decision making which window opens next """
                self.model.current_rights = rows[0][2]

                if self.model.current_rights == "admin" or self.model.current_rights == "Operator":
                    self.login_admin_create_tables()
                    self.main_window = ControlMainwindow(self.model, self.view, self.model.current_rights)
                    self.view.view_login.close()

                if self.model.current_rights == "User":
                    self.main_window = ControlUserTasks(model=self.model, user_name=username)
                    self.view.view_login.close()

    @staticmethod
    def set_up_db():
        db = Database("databases/db_main.db")
        db.connect()
        table_users_statement = """CREATE TABLE IF NOT EXISTS table_users (
                name VARCHAR(10),
                password VARCHAR(30), 
                rights VARCHAR(30),
                notes VARCHAR(30), 
                deprecated VARCHAR(1)
            )
        """

        db.execute_query(table_users_statement)
        ask_if_admin_needed = """SELECT COUNT(*) FROM table_users"""
        rows = db.fetch_data(ask_if_admin_needed)
        if rows[0][0] == 0:
            insert_admin_query = """INSERT INTO table_users (name, password, rights, notes, deprecated)
                                    VALUES ('admin', 'admin', 'admin', 'admin', 0)"""
            db.execute_query(insert_admin_query)
        db.close()

    @staticmethod
    def login_admin_create_tables():
        db = Database("databases/db_main.db")
        db.connect()
        table_orders_statement = """CREATE TABLE IF NOT EXISTS table_orders (
                id INTEGER PRIMARY KEY,
                name VARCHAR(30), 
                progress VARCHAR(30), 
                workflow VARCHAR(30),
                marker1 VARCHAR(30),
                marker2 VARCHAR(30),
                due_date VARCHAR(30),
                notes VARCHAR(1000), 
                deprecated VARCHAR(1)
            )
            """
        db.execute_query(table_orders_statement)

        table_users_statement = """CREATE TABLE IF NOT EXISTS table_users (
                name VARCHAR(10),
                password VARCHAR(30), 
                rights VARCHAR(30), 
                notes VARCHAR(30), 
                deprecated VARCHAR(1)
            )
        """
        db.execute_query(table_users_statement)

        # Is admin in table? -> If no entry in table, then put him in.
        ask_if_admin_needed = """SELECT COUNT(*) FROM table_users"""
        rows = db.fetch_data(ask_if_admin_needed)
        if rows[0][0] == 0:
            insert_admin_query = """INSERT INTO table_users (name, password, rights, notes, deprecated)
                                    VALUES ('admin', 'admin', 'admin', 'admin', 0)"""
            db.execute_query(insert_admin_query)

        db.close()






