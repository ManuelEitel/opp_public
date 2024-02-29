from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from drag_implementation.drag_label import DragLabel
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag



class DragButton(QPushButton):

    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)

class ViewTimetableWidgetMonday(QWidget):
    def __init__(self):

        super().__init__()

        #loadUi("view_timetable/ui_files_timetable/timetable_monday.ui", self)

        widget = QWidget(self)


        #self.setStyleSheet('background:rgb(100,100,100)')
        widget.setFixedSize(350, 200)
        widget.setStyleSheet("border: 5px solid black; background-color:yellow")
        print(self.size())
        widget.blayout = QHBoxLayout()
        widget.blayout.setContentsMargins(20, 20, 20, 20)
        for l in ['A', 'B', 'C', 'D']:
            btn = DragButton(l)
            btn.setStyleSheet("color: red;")

            widget.blayout.addWidget(btn)

        widget.setLayout(self)

    def dragEnterEvent(self, e):
        print("DragEnter")
        e.accept()

    def dragMoveEvent(self, e):
        print("DragMove")
        e.accept()

    def dropEvent(self, e):
        print("DropEvent")
        position = e.pos()
        print(position)

        self.setText(e.mimeData().text())  # +++
        e.setDropAction(Qt.MoveAction)  # +++

        e.accept()