from view_timetable.py_timetable_monday import ViewTimetableWidgetMonday
from view_timetable.py_timetable_tuesday import ViewTimetableWidgetTuesday
from view_timetable.py_timetable_overview import ViewTimetableMain

from drag_implementation.drag_label import DragLabel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton


class ControlTimetableMainWindow(object):

    def __init__(self):
        self.view_timetable_main = ViewTimetableMain()
        self.view_timetable_main.show()
        #self.view_timetable_main.setStyleSheet("background-color:rgb(11, 0, 57)")

        #self.view_timetable_monday = ViewTimetableWidgetMonday()


        # self.view_timetable_monday.setStyleSheet("background-color:rgb(11, 0, 57);")

        #self.view_timetable_tuesday = ViewTimetableWidgetTuesday()

        #self.view_timetable_main.embed_view_timetable_window(self.view_timetable_monday)
        #self.view_timetable_main.embed_view_timetable_window(self.view_timetable_tuesday)
        # Now you can access these widgets later on
        #self.view_timetable_monday.setStyleSheet("background-color:rgb(112, 20, 57)")

        #print(f'Monday widget: {self.view_timetable_monday}')
        #print(f'Tuesday widget: {self.view_timetable_tuesday}')
        ##self. = QVBoxLayout(self.centralwidget)
        #print(f'dir  ={dir(self.view_timetable_main)}')
        #print(f' dir 2 = {dir(self.view_timetable_main.layout.widget)}')
        #print(self.view_timetable_main.layout.findChildren())
        #self.view_timetable_main.view_timetable_monday.setStyleSheet("background-color:rgb(112, 20, 57)")


