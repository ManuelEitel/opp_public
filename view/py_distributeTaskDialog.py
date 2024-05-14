from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.uic import loadUi


class DistributeView(QDialog):
    def __init__(self, view):

        self.view = view
        super(DistributeView, self).__init__()
        loadUi("view/ui_files/distributeTaskDialog.ui", self)


