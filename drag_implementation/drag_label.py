from PyQt5.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class DragLabel(QLabel):

    def mouseEvent(self, e):

        if e.buttons() == Qt.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)
            drag.exec_(Qt.MoveAction)
