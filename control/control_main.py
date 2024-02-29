from model.model_main import ModelMain
from view.view_main import ViewMain
from PyQt5.QtWidgets import QApplication
from control.control_loginview import ControlLoginView
import sys

class ControlMain(object):
    """
    Control regulates the apps behaviour
    Initializes the Login Window at start as well as the app itself
    Coordinates Control_loginView, Control_signUpView, Control_mainWindowView"
    """

    def __init__(self):

        # Start the App
        app = QApplication(sys.argv)

        self.model_main = ModelMain()
        self.view_main = ViewMain()

        self.ui_start_up = ControlLoginView(self.model_main, self.view_main)
        # control_timetable_main_window = ControlTimetableMainWindow()  #ToDo: Integrate Widget after Users
        sys.exit(app.exec())
