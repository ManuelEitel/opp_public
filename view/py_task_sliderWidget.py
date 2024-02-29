from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5 import QtCore as qtc
from databases.datatase_handler import Database


class TaskSliderWidgetView(QWidget):

    def __init__(self, model, saved_workflow):

        """
        The selected and saved stored workflow self.saved_workflow is by pressing on a cell now in a final widget,
        where the user can see and compare the assignment before finally assigning or not assigning it.\n
        It would be cool, if the workflow would be distributed via drag-and-drop, but there is no tim.
        """

        super().__init__()
        self.model = model

        self.saved_workflow = saved_workflow
        loadUi("view/ui_files/task_sliderWidget.ui", self)

        self._rename_usertype()
        self._load_up_workflow_elements()

    def _rename_usertype(self):
        self.give_wf_usertype.setText(self.model.current_rights)

    def _load_up_workflow_elements(self):
        """ Display the Workflows Steps """

        self.name_label.setText(self.saved_workflow)
        db = Database("databases/database_workflows.db")
        db.connect()

        statement = """SELECT * FROM {}""".format(self.saved_workflow)

        rows = db.fetch_data(statement)

        for element in rows:
            self.lw_give_task.addItem(element[1])

