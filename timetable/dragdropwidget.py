from PyQt5.QtWidgets import QLabel, QPushButton
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class DragDropWidget(QLabel):

    def __init__(self, *args, **kwargs):
        super(DragDropWidget, self).__init__(*args, **kwargs)

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return
        mimeData = QMimeData()
        mimeData.setText(self.text())
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.exec(Qt.CopyAction)

