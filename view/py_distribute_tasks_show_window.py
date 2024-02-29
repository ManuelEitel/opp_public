from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class DistributeOverView(QWidget):
    def __init__(self):
        """ bunch of buttons """
        super(DistributeOverView, self).__init__()
        loadUi("view/ui_files/workflow_distribute_step_btn_window.ui", self)

        self.btn_close.clicked.connect(self.close_fct)

    def close_fct(self):
        self.close()
