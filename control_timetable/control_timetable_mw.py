from view_timetable.py_timetable_overview import ViewTimetableMain
from databases.datatase_handler import Database
from timetable.dragdropwidget import DragDropWidget
from timetable.dates_manager import TimetableDateManager
from control_timetable.workhours_manager import WorkHoursManager
from datetime import datetime
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
import regex as re


class ControlTimetableMainWindow(object):

    def __init__(self, model, user):

        self.model = model
        self.user = user

        self.recommended_widget_height = None

        self.relevant_wf = []
        self.relevant_wf_data = []
        self.relevant_wf_conn = []

        self.widget_list = []
        self.workhours_manager = WorkHoursManager
        self.time_manager = TimetableDateManager()
        self.current_week = self.time_manager.current_week
        self.view_timetable_main = ViewTimetableMain(self.model, self.user)

        self.import_orders()
        self.import_relevant_wf()

        self._manage_dates()

        self.this_weeks_tasks = self.get_user_specific_data()

        self._put_data_in_wf_widgets()
        self.view_timetable_main.show()

    def prepping_times(self) -> list:
        widget_prepped_list_of_data = []
        for element in self.this_weeks_tasks:

            date = element[0][0:10]
            begin = re.findall(r', \d*,', element[0])
            time_period = re.findall(r', \d*, \d*', element[0])

            str_begin = begin[0][2:]
            time_period_str = time_period[0][1:]

            time_period_str_2 = re.findall(r', \d*', time_period_str)

            time_period_str_3 = time_period_str_2[0][2:]
            str_begin_2 = str_begin[:-1]
            start_time = self.workhours_manager.turn_int_mins_into_str_times(int(str_begin_2))

            end_time_int = int(time_period_str_3)
            self.recommended_widget_height = end_time_int
            end_time = self.workhours_manager.turn_int_mins_into_str_times(end_time_int)

            widget_prepped_list_of_data.append([date, start_time, end_time, element[1]])

        return widget_prepped_list_of_data

    def sort_tasks_by_day(self, tasks: list) -> list:
        # Define lists for each day of the week
        monday_list = []
        tuesday_list = []
        wednesday_list = []
        thursday_list = []
        friday_list = []

        # Iterate through each task
        for task in tasks:
            # Extract the date from the task
            date_str = task[0].split(',')[0].strip()
            date = datetime.strptime(date_str, '%d.%m.%Y')

            # Determine the day of the week
            day_of_week = date.weekday()

            # Assign the task to the corresponding list based on the day of the week
            if day_of_week == 0:  # Monday
                monday_list.append(task)
            elif day_of_week == 1:  # Tuesday
                tuesday_list.append(task)
            elif day_of_week == 2:  # Wednesday
                wednesday_list.append(task)
            elif day_of_week == 3:  # Thursday
                thursday_list.append(task)
            elif day_of_week == 4:  # Friday
                friday_list.append(task)

        return [monday_list, tuesday_list, wednesday_list, thursday_list, friday_list]

    def _put_data_in_wf_widgets(self):

        prelist = self.prepping_times()
        week_list = self.sort_tasks_by_day(prelist)

        for element in self.view_timetable_main.widget_list:
            element.setAcceptDrops(True)
            element.vertical_layout = QVBoxLayout()

            if element == self.view_timetable_main.monday_widget:

                if week_list[0]:
                    for task in week_list[0]:

                        text = f'{task[3]}\nBegin: {task[1]}; End: {task[2]}'
                        label_str = DragDropWidget(text)
                        label_str.setStyleSheet("border: 1px solid black; background-color: red;")

                        element.vertical_layout.addWidget(label_str)

                    element.setLayout(element.vertical_layout)

            if element == self.view_timetable_main.tuesday_widget:

                if week_list[1]:
                    for task in week_list[1]:
                        text = f'{task[3]}\nBegin: {task[1]}; End: {task[2]}'

                        label_str = DragDropWidget(text)
                        label_str.setStyleSheet("border: 1px solid black; background-color: red;")

                        element.vertical_layout.addWidget(label_str)

                    element.setLayout(element.vertical_layout)

            if element == self.view_timetable_main.wednesday_widget:

                if week_list[2]:
                    for task in week_list[2]:
                        text = f'{task[3]}\nBegin: {task[1]}; End: {task[2]}'
                        label_str = DragDropWidget(text)
                        label_str.setStyleSheet("border: 1px solid black; background-color: red;")

                        element.vertical_layout.addWidget(label_str)

                    element.setLayout(element.vertical_layout)

            if element == self.view_timetable_main.thursday_widget:

                if week_list[3]:

                    for task in week_list[3]:
                        text = f'{task[3]}\nBegin: {task[1]}; End: {task[2]}'
                        label_str = DragDropWidget(text)

                        label_str.setStyleSheet("border: 1px solid black; background-color: red;")

                        element.vertical_layout.addWidget(label_str)

                    element.setLayout(element.vertical_layout)

            if element == self.view_timetable_main.friday_widget:
                if week_list[4]:
                    for task in week_list[4]:
                        text = f'{task[3]}\nBegin: {task[1]}; End: {task[2]}'

                        label_str = DragDropWidget(text)
                        label_str.setStyleSheet("border: 1px solid black; background-color: red;")

                        element.vertical_layout.addWidget(label_str)

                    element.setLayout(element.vertical_layout)


    def get_user_specific_data(self):
        specific_data = []
        for element in self.relevant_wf_conn:
            print(f'element = {element}')
            for sub_element in element:
                workplace = sub_element[0]
                user = sub_element[1]
                date_and_time = sub_element[2]
                date = date_and_time[0:10]

                if date != "still empt" and user == self.user:
                    specific_data.append([date_and_time, workplace])

        this_weeks_tasks = self.filter_specific_data_for_week(specific_data)

        return this_weeks_tasks

    def filter_specific_data_for_week(self, prefiltered_list: list):
        this_weeks_tasks = []
        for element in prefiltered_list:
            date = element[0][0:10]
            if date in self.current_week:
                this_weeks_tasks.append(element)

        return this_weeks_tasks

    def _manage_dates(self):

        date_manager = TimetableDateManager()

        self.current_week = date_manager.current_week
        self.current_week_index = date_manager.current_week_index
        self.view_timetable_main.set_initial_date(current_week=self.current_week,
                                                  current_week_index=self.current_week_index)


    def import_orders(self):
        """Import only the non deprecated orders"""

        db = Database("databases/db_main.db")
        db.connect()

        query = "SELECT * FROM table_orders WHERE deprecated = 0"

        orders = db.fetch_data(query)

        db.close()

        db_conn = Database("databases/db_wf_usr_conn.db")
        db_conn.connect()

        for element in orders:

            table_name = f'wf_{element[3]}_ordr_{element[1]}'

            table_query = f"SELECT * FROM {table_name}"

            relevant_wf_conn = db_conn.fetch_data(table_query)



            if relevant_wf_conn:
                print(f'relevant_wf_conn = {relevant_wf_conn}')
                self.relevant_wf_conn.append(relevant_wf_conn)
                self.relevant_wf.append(element[3])

        db_conn.close()

    def import_relevant_wf(self):
        if self.relevant_wf:

            db = Database("databases/db_workflows.db")
            db.connect()

            for element in self.relevant_wf:

                query = f"SELECT * FROM {element}"

                relevant_wf_data = db.fetch_data(query)

                self.relevant_wf_data.append(relevant_wf_data)

            db.close()



