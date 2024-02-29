from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QPushButton, QVBoxLayout, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('QListWidget Example')
        self.setGeometry(100, 100, 300, 200)

        # Create a QListWidget
        self.list_widget = QListWidget(self)

        # Create a QPushButton to add items to the list
        self.button_add = QPushButton('Add Item', self)
        self.button_add.clicked.connect(self.add_item)

        # Create a layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_add)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def add_item(self):
        # Get the text from the user
        text, ok = QInputDialog.getText(self, 'Add Item', 'Enter item text:')
        if ok and text:
            # Add the text as a new item to the QListWidget
            self.list_widget.addItem(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
