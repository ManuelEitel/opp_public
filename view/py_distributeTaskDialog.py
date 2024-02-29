from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class DistributeView(QWidget):
    def __init__(self, view):

        self.view = view
        super(DistributeView, self).__init__()
        loadUi("view/ui_files/distributeTaskWidget.ui", self)


