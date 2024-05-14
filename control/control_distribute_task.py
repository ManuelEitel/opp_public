from view.py_distribute_tasks_show_window import DistributeOverView
from databases.datatase_handler import Database
from users.user_tasks_other_users import CheckOtherUserTasks
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from users.user_tasks import ManageUserTasks
from control_timetable.workhours_manager import WorkHoursManager


class ControlDistributeTask(object):

    def __init__(self, model, view, workflow_to_implement, item_name):

        self.model = model
        self.view = view
        self.workflow_to_implement = workflow_to_implement

        self.item_name = item_name

        self.rowCount = 0
        self.control_dist_to_user = None
        self.workflow_elements = None
        self.clicked_row = None

        self.task_name = None  # query relevant
        self.task_name_row = None  # ui relevant
        self.user_name = None  # query relevant

        self.manage_user_table = None  # class call for user tasks management
        self.check_other_user_tasks = None

        self.button_state_ready_for_putting = 0
        self.over_view = DistributeOverView()  # loads the window with the buttons
        self.over_view.distribute_cell_clicked.connect(self.select_task)
        self.over_view.employees_tw_clicked.connect(self.finish_button)

        self._autofill_workflow_tw_with_tasks()

        self.over_view.giveTask.clicked.connect(self.give_task_pressed_fct)  # ToDo: Recreate USER task Database
        self._autofill_employees_with_user_rights()

        self._auto_fill_wf_users_into_wf_tw()
        self._name()
        self.over_view.show()

    def _name(self):
        """
        For some reason, this function is not being shown, but it is called!
        """
        self.over_view.usertype_label.setText(self.model.current_rights)
        self.over_view.label.setText(f'Order: {self.item_name}')

    def finish_button(self, row: int, column: int):
        if self.over_view.giveTask.text()[-2:] == "to":
            self.user_name = self.over_view.tw_employees.item(row, 0).text()
            new_text = f"{self.over_view.giveTask.text()} {self.user_name}"
            self.over_view.giveTask.setText(new_text)
            self.over_view.giveTask.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
            self.button_state_ready_for_putting = 1


        else:
            self.over_view.giveTask.setText("Give Task")
            self.over_view.giveTask.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
            self.user_name = None
            self.task_name = None
            self.task_name_row = None
            self.button_state_ready_for_putting = 0


    def set_task_visually(self):
        item = QTableWidgetItem(self.user_name)
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.over_view.tw_tasks.setItem(self.task_name_row, 2, item)

    def erase_traces_of_old_non_deprecated_tasks(self):
        self.check_other_user_tasks = CheckOtherUserTasks(user_name=self.user_name, task=self.task_name,
                                                          workflow=self.workflow_to_implement, date=None,
                                                          order=self.item_name)

    def put_task_to_user(self):
        """
        Actual Complex Code
        """
        # set up user tasks table
        self.manage_user_table = ManageUserTasks(user_name=self.user_name, task=self.task_name,
                                                 workflow=self.workflow_to_implement, date=None, order=self.item_name)

        # pull_user_tasks = [('14.05.2024', 'Step1', 'TestWorkflow', 480, 510, 'CustomerName1', 0)]
        pull_user_tasks = self.manage_user_table.pull_non_deprecated_user_tasks()

        self.erase_traces_of_old_non_deprecated_tasks()

        if pull_user_tasks:  # user has at least one task
            task_is_done = self.check_if_task_is_done_already(task_name=self.task_name)

            if not task_is_done:

                task_done_state = self.task_is_scheduled_already(task_name=self.task_name)
                deprecated_state = task_done_state[0]
                user_currently = task_done_state[1]

                if deprecated_state == 0 and user_currently:
                    self.erase_user_from_db_wf(task_name=self.task_name, user_currently=user_currently)  # no doubling

                time_of_entry, time_of_end, date_of_entry, string = (
                    self.manage_user_table.put_into_next_timeslot_when_data_there_alrdy())
                return date_of_entry, time_of_entry, time_of_end, string

        if not pull_user_tasks:  # user has no non deprecated task ever
            """ This seems done. """
            task_is_done = self.check_if_task_is_done_already(task_name=self.task_name)
            if not task_is_done:
                # next_monday, 480, end_time, f"{next_monday}, 480, {end_time}"
                date, time_start, time_end, time_string = (
                    self.manage_user_table.find_next_timeslot_if_tables_empty_and_put_task_there())
                return date, time_start, time_end, time_string

    def erase_user_from_db_wf(self, task_name: str, user_currently: str):
        order_name = self.item_name
        workflow = self.workflow_to_implement

        table_name = f"wf_{workflow}_ordr_{order_name}"

        db = Database(f"databases/db_{user_currently}_tasks.db")
        db.connect()

        query = f"DELETE FROM user_tasks WHERE task = ? AND workflow = ? AND order_name = ? AND deprecated = 0"
        params = (task_name, workflow, order_name)

        db.execute_query(query=query, params=params)

        db.close()

    def task_is_scheduled_already(self, task_name: str):
        """ Finds out, if the task is currently given to some other user and removes it. It is not deprecated, since
        task_is_done - check is done before this function with self.check_if_task_is_done_already """
        order_name = self.item_name
        workflow = self.workflow_to_implement

        table_name = f"wf_{workflow}_ordr_{order_name}"

        db = Database(f"databases/db_wf_usr_conn.db")
        db.connect()

        query = f"SELECT deprecated, user_name FROM {table_name} WHERE step_name = ?"

        params = (task_name,)

        data = db.fetch_data(query=query, params=params)

        db.close()
        deprecated_state = data[0][0]
        user_currently = data[0][1]

        if not data:
            return []
        else:
            return [deprecated_state, user_currently]

    def is_task_deprecated(self) -> bool:
        """
        Checks in the task table self.over_view.tw_tasks, if the selected task in self.clicked_row is
        already deprecated or not and returns true, if the task is deprecated
        """
        task_deprecation_state = self.over_view.tw_tasks.item(self.clicked_row, 4).text()
        if int(task_deprecation_state) == 1:  # task is indeed deprecated already
            return True
        else:
            return False

    def set_user_task(self):

        self.set_task_visually()  # Sets the task visually into the window table cell

        self.create_or_fill_table_wf_usr_conn()

        return_dates = self.put_task_to_user()

        if return_dates:
            date, time_start, time_end, time_string = return_dates

            print(F'date, time_start, time_end, time_string = {date, time_start, time_end, time_string}')

            hours = time_start // 60
            minutes = time_start % 60
            if minutes == 0:
                minutes = "00"
            task_begin_time = f'{hours}:{minutes}'
            # print(f'task_begin_time = {task_begin_time}')
            end_hours = time_end // 60
            end_mins = time_end % 60
            if end_mins == 0:
                end_mins = "00"
            task_end_time = f'{end_hours}:{end_mins}'

            item_at = QTableWidgetItem(f'{date} at {task_begin_time} until {task_end_time}')
            self.over_view.tw_tasks.setItem(self.clicked_row, 3, item_at)
            item_at.setFlags(QtCore.Qt.ItemIsEnabled)

    def give_task_pressed_fct(self):
        """
        Checks, if the button state is correct, so that the necessary data is there for distributing the task.
        """
        if self.button_state_ready_for_putting == 1:  # distribute task is a operator mode
            if not self.is_task_deprecated():  # quick check, if the task is already done
                self.set_user_task()

    def get_wf_steps_and_data(self):
        """
        'Distribute a wf Task Onto a User' is pressed. For this, we need to collect the wf data\n
            * Steps of wf including
                * Step Place (e.g. Computer)
                * Step Name (e.g. Initial Step)
                * Step Time (e.g. '2:00')
                * Previous Step (e.g. Zeroeth Step)
                * Next Step (e.g. Second Step)
                * The User, that is being connected currently to that step (E.g. 'User1')
                * Comment (e.g. 'Not yet')
        """

        db = Database("databases/db_workflows.db")
        db.connect()
        query = f"""SELECT * FROM {self.workflow_to_implement}"""

        data = db.fetch_data(query)

        db.close()
        return data

    def get_table_name_wf_usr_conn(self) -> str:
        """
        self.workflow_to_implement: Is preselected
        self.item_name: Name of Order
        """
        return f'wf_{self.workflow_to_implement}_ordr_{self.item_name}'

    @staticmethod
    def check_table_wf_usr_conn(table_name: str) -> list:
        db = Database('databases/db_wf_usr_conn.db')
        db.connect()
        # Check if the table exists
        table_check = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        result = db.fetch_data(table_check)  # result is either [], or [('wf_Test_Workflow_2_ordr_ThirdOrder',)]
        db.close()

        return result

    def check_or_create_table_wf_usr_conn(self, table_name: str):
        """
        Checks if the connecting table exists, or creates it. \n
        """

        result = self.check_table_wf_usr_conn(table_name=table_name)

        if not result:
            self.create_wf_usr_conn_initially(table_name)

    @staticmethod
    def update_wf_urs_conn(query: str, params):
        """
        Fill the wf_usr_conn_db with the entrance query
        """

        db = Database('databases/db_wf_usr_conn.db')
        db.connect()

        db.execute_query(query, params)
        db.close()

    def create_wf_usr_conn_initially(self, table_name: str):
        query_create_table = f"""
                             CREATE TABLE IF NOT EXISTS {table_name} (
                                 step_name VARCHAR(30),
                                 user_name VARCHAR(30),
                                 user_time VARCHAR(30),
                                 deprecated INT(1)
                             )
                             """
        self.update_wf_urs_conn(query=query_create_table, params=None)

    def fill_wf_usr_conn_steps_initially_by_element(self, element: tuple, query_fill: str):
        """ Fills table wf_usr_conn element by element. This function is called inside a loop """

        step_name = element[1]
        user_name = self.user_name if step_name == self.task_name else "not yet"

        user_time = "still empty"

        self.update_wf_urs_conn(query=query_fill, params=(step_name, user_name, user_time))

    def create_or_fill_table_wf_usr_conn(self):

        table_name = self.get_table_name_wf_usr_conn()
        self.check_or_create_table_wf_usr_conn(table_name)

        query_fill = f"""UPDATE {table_name} SET user_name = ? WHERE step_name = ?"""
        self.update_wf_urs_conn(query=query_fill, params=(self.user_name, self.task_name))

    def select_task(self, row: int, column: int):
        """ Callback function when the table with the steps and users is clicked """
        self.clicked_row = row
        if not self.over_view.tw_tasks.item(row, 2):  # first time opening this, the cell will be empty
            workflow = self.over_view.tw_tasks.item(row, 1).text()
            self.task_name = self.over_view.tw_tasks.item(row, 0).text()
            self.task_name_row = row

            self.over_view.giveTask.setText(f'Give Task {self.task_name} to')
            self.over_view.giveTask.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
            self.button_state_ready_for_putting = 0
        elif self.over_view.tw_tasks.item(row, 2):
            currently_given_user_name = self.over_view.tw_tasks.item(row, 2).text()

            workflow = self.over_view.tw_tasks.item(row, 1).text()
            self.task_name = self.over_view.tw_tasks.item(row, 0).text()
            self.task_name_row = row
            self.over_view.giveTask.setText(f'Give Task {self.task_name} to')
            self.over_view.giveTask.setStyleSheet('background-color: rgb(244, 242, 255); font: 12pt "Segoe UI";')
            self.button_state_ready_for_putting = 0

    def check_if_task_is_done_already(self, task_name: str) -> bool:
        """
        This is being called after self.task, self.wf and self.order_name are given.\n
        Checks, if the task is deprecated = 1 and returns True, if so.\n
        Else, returns False.
        """
        order_name = self.item_name
        workflow = self.workflow_to_implement

        table_name = f"wf_{workflow}_ordr_{order_name}"

        db = Database(f"databases/db_wf_usr_conn.db")
        db.connect()

        query = f"SELECT deprecated FROM {table_name} WHERE step_name = ?"

        params = (task_name,)

        data = db.fetch_data(query=query, params=params)

        db.close()

        if not data:
            return False  # task is not yet done
        elif data[0][0] == 1:
            return True  # task is done already
        else:

            return False  # task is not yet done

    def __put_user_into_user_tw(self, user: tuple):
        """ Visually puts the user in the table """
        user_name = user[0]

        self.rowCount += 1

        self.over_view.tw_employees.setRowCount(self.rowCount)

        item = QTableWidgetItem(user_name)
        self.over_view.tw_employees.setItem(self.rowCount - 1, 0, item)
        item.setFlags(QtCore.Qt.ItemIsEnabled)

    def _autofill_employees_with_user_rights(self):

        db = Database("databases/db_main.db")
        db.connect()

        table_name = 'table_users'
        user_rights = 'rights'
        value = 'User'
        query = f"SELECT * FROM {table_name} WHERE {user_rights} = ?"

        # Execute the query
        users = db.fetch_data(query, (value,))
        self.rowCount = 0
        for element in users:
            self.__put_user_into_user_tw(user=element)

        db.close()

    def _autofill_workflow_tw_with_tasks(self):

        db1 = Database("databases/db_workflows.db")
        db1.connect()

        table_name = self.workflow_to_implement
        statement = f"""SELECT * FROM {table_name}"""
        self.workflow_elements = db1.fetch_data(statement)
        self.rowCount = 0
        db1.close()

        if self.workflow_elements:
            for element in self.workflow_elements:
                self.__put_wf_into_wf_tw(element)

    def _auto_fill_wf_users_into_wf_tw(self):
        table_name = f'wf_{self.workflow_to_implement}_ordr_{self.item_name}'
        db = Database('databases/db_wf_usr_conn.db')
        db.connect()

        # Check if the table exists
        table_check = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
        result = db.fetch_data(table_check)
        db.close()
        self.rowCount = 0
        if result:

            db_table = Database('databases/db_wf_usr_conn.db')
            query = f"SELECT * FROM {table_name}"
            db_table.connect()
            data = db_table.fetch_data(query)  # all the data, that has this workflow-usr-conn database table
            db_table.close()

            i = 0
            for element in data:
                usr_name = element[1]
                deprecation_status = element[3]

                date, task_begin_time, task_end_time = self.get_current_worked_time(user_name=usr_name,
                                                                                    wf_name=self.workflow_to_implement,
                                                                                    order_name=self.item_name)

                self.rowCount += 1
                item = QTableWidgetItem(usr_name)
                item_date = QTableWidgetItem(f'{date} at {task_begin_time} until {task_end_time}')
                item_deprecated = QTableWidgetItem(f"{str(deprecation_status)}")

                self.over_view.tw_tasks.setItem(i, 2, item)
                self.over_view.tw_tasks.setItem(i, 3, item_date)
                self.over_view.tw_tasks.setItem(i, 4, item_deprecated)

                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item_date.setFlags(QtCore.Qt.ItemIsEnabled)
                item_deprecated.setFlags(QtCore.Qt.ItemIsEnabled)
                i += 1

    def get_current_worked_time(self, user_name: str, wf_name: str, order_name: str):

        db = Database(f"databases/db_{user_name}_tasks.db")
        db.connect()

        query = f"SELECT date, task_begin, task_end, deprecated FROM user_tasks WHERE workflow = ? AND order_name = ?"
        params = (wf_name, order_name)

        all_data = db.fetch_data(query=query, params=params)
        db.close()
        # print(f'all_data = {all_data}')

        date = all_data[0][0]
        begin = int(all_data[0][1])
        end = int(all_data[0][2])
        # print(F'testi testie begin = {begin}; end = {end}')
        deprecated_status = all_data[0][3]
        # print(f'deprecated_status = {deprecated_status}')

        hours = begin // 60
        minutes = begin % 60
        if minutes == 0:
            minutes = "00"
        task_begin_time = f'{hours}:{minutes}'
        # print(f'task_begin_time = {task_begin_time}')
        end_hours = end // 60
        end_mins = end % 60
        if end_mins == 0:
            end_mins = "00"
        task_end_time = f'{end_hours}:{end_mins}'
        # print(f'returning : {date, str(task_begin_time), str(task_end_time)}')
        return date, str(task_begin_time), str(task_end_time)

    def __put_wf_into_wf_tw(self, element: tuple):

        self.rowCount += 1

        self.over_view.tw_tasks.setRowCount(self.rowCount)
        element_list = [element[1], element[0]]
        i = 0
        for entry in element_list:
            item = QTableWidgetItem(entry)
            self.over_view.tw_tasks.setItem(self.rowCount - 1, i, item)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            i += 1
