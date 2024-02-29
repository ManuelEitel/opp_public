from PyQt5.uic import loadUi
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class NewWFStep(QWidget):

    pushed_new_step = qtc.pyqtSignal(str, str, str, str, str)

    def __init__(self, model):
        """
        The gui for the workflow windows' new step popup window is being done here.
        """

        super().__init__()
        self.model = model
        loadUi("view/ui_files/workflow_newstep.ui", self)

        self.setWindowModality(Qt.ApplicationModal)  # make it, so you have to interact with the widget first

        self._name()
        self.make_new_wf_step.clicked.connect(self.push_create_new_step)

    def _name(self):
        self.workflow_usertype.setText(self.model.current_rights)
        self.workplace_list = [self.computer_btn, self.supply_btn, self.workstation_btn, self.packaging_btn]

    def push_create_new_step(self):
        """
        Emits name_of_step, wf_next_step, wf_next_step, wf_est_time
        """
        name_of_step = self.wf_step_name.text()
        wf_next_step = self.wf_next_step.text()
        wf_prev_step = self.wf_prev_step.text()
        wf_est_time = self.wf_est_time.text()
        if (name_of_step == "" or wf_next_step == "" or wf_prev_step == ""
                or wf_est_time == "" or not self.check_for_one_button_checked()):
            self.wf_feedback_label.setText("Missing entry.")
        else:
            rb_workplace = self.get_text_from_ratio_button_true()
            self.pushed_new_step.emit(name_of_step, wf_next_step, wf_prev_step, wf_est_time, rb_workplace)
            self.close()

    def check_for_one_button_checked(self):
        """ Returns True, if one button is pressed, False otherwise """

        for element in self.workplace_list:
            if element.isChecked():
                return True
        return False

    def get_text_from_ratio_button_true(self):
        """ Returns the string of the button in self.workplace_list, that is true."""

        for element in self.workplace_list:
            if element.isChecked():
                return element.text()
