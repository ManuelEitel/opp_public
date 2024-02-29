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

class ViewTimetableWidgetTuesday(QWidget):
    def __init__(self):

        super().__init__()

        loadUi("view_timetable/ui_files_timetable/timetable_tuesday.ui", self)

        self.setAcceptDrops(True)
        self.setStyleSheet("background-color:yellow")
        self.blayout = QHBoxLayout()
        for l in ['E', 'F', 'G', 'H']:
            btn = DragButton(l)
            btn.setStyleSheet("color: red;")

            self.blayout.addWidget(btn)
        btn2 = QPushButton(self, text="Hallo")
        self.blayout.addWidget(btn2)
        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.pos()
        widget = e.source()

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if pos.x() < w.x() + w.size().width() // 2:
                # We didn't drag past this widget.
                # insert to the left of it.
                self.blayout.insertWidget(n - 1, widget)
                break

        e.accept()
