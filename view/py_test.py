from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget


class TestTest(QWidget):

    def __init__(self):

        super().__init__()
        loadUi("view/ui_files/test_widget.ui", self)

