from view.py_distribute_tasks_show_window import DistributeOverView
from databases.datatase_handler import Database
from PyQt5.QtWidgets import QPushButton
from view.py_test import TestTest


class ControlDistributeTask(object):

    def __init__(self, model, view, workflow_to_implement, item_name):

        self.model = model
        self.view = view
        self.workflow_to_implement = workflow_to_implement
        self.item_name = item_name
        self.over_view = DistributeOverView()  # loads the window with the buttons

        self.button_list_counter = 0
        self.step_list = []
        self.place_list = []
        self.time_list = []
        self.workflow_steps_button_list = []
        self._pull_wf_from_db()

        self.over_view.show()

        print(f'initiation from cdt gone well')

    def _pull_wf_from_db(self):
        db = Database("databases/db_workflows.db")
        db.connect()

        statement = f"SELECT * FROM {self.workflow_to_implement};"
        all_info = db.fetch_data(statement)

        for element in all_info:
            place = element[0]
            step = element[1]
            time = element[2]
            self.place_list.append(place)
            self.step_list.append(step)
            self.time_list.append(time)

        for i in range(len(self.step_list)):
            self.new_btn_insertion(self.step_list[i], i)

    def function_a(self):
        test = TestTest()
        test.show()

    def new_btn_insertion(self, place: str, i: int):
        button = QPushButton(text=place)
        button.setStyleSheet("background-color: rgb(244, 242, 255)")
        button.setObjectName(f'Button_{i}')
        button.clicked.connect(self.function_a)
        self.workflow_steps_button_list.append(button)
        self.over_view.horizontalLayout.insertWidget(1 + i, button)
        self.over_view.setLayout(self.over_view.horizontalLayout)
