from view.py_user_tasks import UserTasksView
from model.model_main import ModelMain
from databases.datatase_handler import Database
from timetable.dates_manager import TimetableDateManager
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore
import regex as re


class ControlUserTasks:
    def __init__(self, model: ModelMain, user_name: str):
        # ToDo: The user tasks are not being put into their place nicely
        # The User has tasks on the same day, that i put into the db at 7.30
        # The tasks are not in order, as they should be
        # that's perhaps why they are not beind displayed nicely in the user
        # window.
        self.model = model
        self.user_name = user_name
        self.user_tasks_view = UserTasksView(model)

        self.task = None
        self.wf = None
        self.order_name = None
        self.current_date = None
        self.task_row = None

        self.current_observed_day = None
        self.current_observed_day_index = 0



        self.today_user_tasks = self._pull_all_user_tasks_of_this_day()
        self.rowCount = 0

        self._set_label_text()

        self._put_user_tasks_of_this_day_into_tw()
        self._set_current_observed_day_index()

        self.user_tasks_view.show()
        self.user_tasks_view.cell_clicked_user.connect(self.on_cell_clicked_fct)
        self.user_tasks_view.btn_book.clicked.connect(self.set_task_deprecated_after_done)

        self.user_tasks_view.prior_week_clicked.connect(self.switch_week_view)
        self.user_tasks_view.next_week_clicked.connect(self.switch_week_view)

    def _set_label_text(self):
        self.user_tasks_view.usertype_label.setText(f"{self.user_name}")
        timetable_dates = TimetableDateManager()
        self.current_date = timetable_dates.current_date
        self.user_tasks_view.label.setText(f"Tasks for the date: {self.current_date}")

    def on_cell_clicked_fct(self, row: int, column: int):

        self.task = self.user_tasks_view.tableWidget.item(row, 0).text()
        self.wf = self.user_tasks_view.tableWidget.item(row, 2).text()
        self.order_name = self.user_tasks_view.tableWidget.item(row, 3).text()

        self.user_tasks_view.btn_book.setText(f"Book Time / Task Done for {self.task}?")

        self.task_row = row

    def switch_week_view(self, switch_idicator: int):
        """ return: List of all tasks given to the user  and has a small error handling for doubling """
        # print(f'switch_indicator = {switch_idicator}')

        # change self.current_observed_day_index
        self.carry_current_observed_day(index_counter=switch_idicator)

        time_table_stuff = TimetableDateManager()
        new_date = (
            time_table_stuff.weeks)[self.current_observed_day_index[0]][1][self.current_observed_day_index[1]]

        new_date_tasks = self.get_user_tasks_acc_to_date(date=new_date)
        # print(f"tasks from date {new_date}: {new_date_tasks}")
        self.put_user_tasks_of_certain_date_into_tw(date_tasks=new_date_tasks)

        self.update_label_date(new_date)

    def update_label_date(self, date: str):
        # print(f'')
        self.user_tasks_view.label.setText(f"Tasks for the date: {date}")

    def get_user_tasks_acc_to_date(self, date: str) -> list:
        """ Put in a date an get the tasks from said date. """
        db_file_name = f"databases/db_{self.user_name}_tasks.db"
        db = Database(db_file_name)
        db.connect()

        query = "SELECT * FROM user_tasks WHERE date = ?"
        today_tasks = db.fetch_data(query=query, params=(date,))

        # Error handling of small kind
        today_tasks_non_doubles = self.error_handler_one_doubles_in_daily_tasks(today_tasks)  # adding error handling

        return today_tasks_non_doubles

    def put_user_tasks_of_certain_date_into_tw(self, date_tasks: list):
        """ After getting daily tasks (self.today_user_tasks) fill the tableWidget with them """
        # Check, how many rows there is something inside the TableWidget
        # clear TableWidget
        if self.user_tasks_view.tableWidget.rowCount() > 0:
            self.user_tasks_view.tableWidget.clearContents()  # Clear the cell contents
            self.user_tasks_view.tableWidget.setRowCount(0)

        # fill the widget
        self.rowCount = 1
        if date_tasks:
            for element in date_tasks:

                self.user_tasks_view.tableWidget.setRowCount(self.rowCount)

                task_name = element[1]
                task_time = int(element[4]) - int(element[3])
                wf_name = element[2]
                order_name = element[5]
                deprecation = str(element[6])

                item_name = QTableWidgetItem(task_name)
                item_time = QTableWidgetItem(str(task_time))
                item_task_name = QTableWidgetItem(wf_name)
                item_order_name = QTableWidgetItem(order_name)
                item_deprecation = QTableWidgetItem(deprecation)

                self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 0, item_name)
                self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 1, item_time)
                self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 2, item_task_name)
                self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 3, item_order_name)
                self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 4, item_deprecation)

                item_name.setFlags(QtCore.Qt.ItemIsEnabled)
                item_time.setFlags(QtCore.Qt.ItemIsEnabled)
                item_task_name.setFlags(QtCore.Qt.ItemIsEnabled)
                item_order_name.setFlags(QtCore.Qt.ItemIsEnabled)
                item_deprecation.setFlags(QtCore.Qt.ItemIsEnabled)
                self.rowCount += 1

    def _set_current_observed_day_index(self):
        """
        Get index to date: Observe the [1] in the weeks print
        print(f'test: current_date needs to be today: {weeks[current_week_index-1][1][index_in_curr_week]}')
        """
        timetable_date_manager = TimetableDateManager()
        weeks = timetable_date_manager.weeks

        current_week_index = timetable_date_manager.current_week_index
        current_date = timetable_date_manager.current_date

        index_in_curr_week = None

        for index, element in enumerate(weeks[current_week_index-1][1]):
            if current_date == element:
                index_in_curr_week = index

        self.current_observed_day_index = (current_week_index-1, index_in_curr_week)

    def carry_current_observed_day(self, index_counter: int):
        """
        Change the index self.current_observed_day_index according to the input (pressing of the button)
        """

        current_week_index = self.current_observed_day_index[0]
        day_index = self.current_observed_day_index[1]

        new_day_index = day_index + index_counter

        if new_day_index == 7:
            new_day_index = 0
            current_week_index = current_week_index + 1
            self.current_observed_day_index = (current_week_index, new_day_index)
            # print(f'new self.current_observed_day_index = {self.current_observed_day_index}')
        elif new_day_index == -1:
            new_day_index = 6
            current_week_index = current_week_index - 1
            self.current_observed_day_index = (current_week_index, new_day_index)
            # print(f'new self.current_observed_day_index = {self.current_observed_day_index}')
        else:
            self.current_observed_day_index = (current_week_index, new_day_index)
            # print(f'new self.current_observed_day_index = {self.current_observed_day_index}')

    def set_task_deprecated_after_done(self):
        """
        Needs to be deprecated in the following databases:
        db_{user}_tasks.db, db_wf_usr_conn.db, db_main.db
        """
        if self.task:
            self.set_db_user_tasks_db_deprecated_after_done()
            self.set_db_wf_usr_conn_db_deprecated_after_done()
            self.update_db_main_table_orders_progress()

            self.item_row_deprecation_status = self.user_tasks_view.tableWidget.item(self.task_row, 0).text()

            if self.item_row_deprecation_status == 1:
                pass
            else:
                self.user_tasks_view.tableWidget.setItem(self.task_row, 4, "1")



    def update_db_main_table_orders_progress(self):
        """ Gets only called when self.task is not None; deprecates user task in db_{user}_tasks.db"""
        # read out the table_orders progress

        db = Database("databases/db_main.db")
        db.connect()

        query = f"SELECT progress FROM table_orders WHERE name = ? AND workflow = ?"
        params = (self.order_name, self.wf)

        data = db.fetch_data(query=query, params=params)

        db.close()
        if data:

            time = data[0][0]  # data is of the form [(string,)]

            #print(f'time = {time}; seen in update_db_main_table_orders_progress in control_user_tasks.py')

            int_list = self.string_progress_reader(time)
            if int_list:
                int_got = int_list[0]
                int_from = int_list[1]

                if int_got < int_from:
                    int_got += int_got

                    db = Database("databases/db_main.db")
                    db.connect()

                    query = f"UPDATE table_orders SET progress = ? WHERE name = ? AND workflow = ?"
                    params = (self.order_name, self.wf)

                    db.execute_query(query=query, params=params)

                    db.close()

                    print(f'good look that this works first try. ')

    def string_progress_reader(self, time: str):
        """
        Makes the 0/4 string into two nice ints as [0,4] and checks, if they are nice.
        """

        match = re.findall(r'\d*/', time)
        match = match[0][:-1]
        match2 = re.findall(r'/\d*', time)
        match2 = match2[0][1:]
        int_got = int(match)
        int_from = int(match2)

        if int_got <= int_from:
            return [int_got, int_from]
        else:
            return []

    def set_db_wf_usr_conn_db_deprecated_after_done(self):
        """ Gets only called when self.task is not None; deprecates user task in db_{user}_tasks.db"""

        table_name = f"wf_{self.wf}_ordr_{self.order_name}"

        db = Database("databases/db_wf_usr_conn.db")
        db.connect()

        query = f"UPDATE {table_name} SET deprecated = 1 WHERE user_name = ? AND step_name = ?"
        params = (self.user_name, self.task)

        db.execute_query(query=query, params=params)
        db.close()

    def set_db_user_tasks_db_deprecated_after_done(self):
        """ Gets only called when self.task is not None; deprecates user task in db_{user}_tasks.db"""

        db_name = f"databases/db_{self.user_name}_tasks.db"

        db = Database(db_name)
        db.connect()

        query = f"UPDATE user_tasks SET deprecated = 1 WHERE task = ? AND workflow = ? AND order_name = ?"
        params = (self.task, self.wf, self.order_name)

        db.execute_query(query=query, params=params)

        db.close()

    def _put_user_tasks_of_this_day_into_tw(self):
        """ After getting daily tasks (self.today_user_tasks) fill the tableWidget with them """

        self.rowCount = 1
        for element in self.today_user_tasks:

            self.user_tasks_view.tableWidget.setRowCount(self.rowCount)

            task_name = element[1]
            task_time = int(element[4]) - int(element[3])
            wf_name = element[2]
            order_name = element[5]
            deprecation = str(element[6])

            item_name = QTableWidgetItem(task_name)
            item_time = QTableWidgetItem(str(task_time))
            item_task_name = QTableWidgetItem(wf_name)
            item_order_name = QTableWidgetItem(order_name)
            item_deprecation = QTableWidgetItem(deprecation)

            self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 0, item_name)
            self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 1, item_time)
            self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 2, item_task_name)
            self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 3, item_order_name)
            self.user_tasks_view.tableWidget.setItem(self.rowCount-1, 4, item_deprecation)

            item_name.setFlags(QtCore.Qt.ItemIsEnabled)
            item_time.setFlags(QtCore.Qt.ItemIsEnabled)
            item_task_name.setFlags(QtCore.Qt.ItemIsEnabled)
            item_order_name.setFlags(QtCore.Qt.ItemIsEnabled)
            item_deprecation.setFlags(QtCore.Qt.ItemIsEnabled)
            self.rowCount += 1

    def _pull_all_user_tasks_of_this_day(self) -> list:
        """ return: List of all tasks given to the user  and has a small error handling for doubling """

        self.timetable_date_manager = TimetableDateManager()
        current_date = self.timetable_date_manager.current_date  # e.g. 03.04.24

        db_file_name = f"databases/db_{self.user_name}_tasks.db"
        db = Database(db_file_name)
        db.connect()

        query = "SELECT * FROM user_tasks WHERE date = ?"
        today_tasks = db.fetch_data(query=query, params=(current_date,))
        print(f'today_tasks = {today_tasks}')
        # Error handling of small kind
        today_tasks_non_doubles = self.error_handler_one_doubles_in_daily_tasks(today_tasks)  # adding error handling

        return today_tasks_non_doubles

    def error_handler_one_doubles_in_daily_tasks(self, today_tasks: list):
        """ First calls self.reduce_duplicates and then checks for matching starting times """

        today_tasks_non_doubles = self.reduce_duplicates(today_tasks)

        seen_values = set()
        result = []
        for tup in today_tasks_non_doubles:
            if tup[3] not in seen_values:
                result.append(tup)
                seen_values.add(tup[3])

        return result

    @staticmethod
    def reduce_duplicates(input_list: list) -> list:
        """ Static method to return the reduced list """
        # Create a dictionary to store element counts
        element_counts = {}

        # Count occurrences of each element in the input list
        for element in input_list:
            if element in element_counts:
                element_counts[element] += 1
            else:
                element_counts[element] = 1

        # Create the output list with elements occurring only once
        output_list = [element for element, count in element_counts.items() if count == 1]

        return output_list
