from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QWidget, QMainWindow
from PyQt5 import QtCore as qtc


class DeleteUserDialog(QDialog):

    deletion_pressed_signal = qtc.pyqtSignal(str)

    def __init__(self):
        """
        This is the Delete Dialog View of the small Window, that the Operator can call to delete elements. \n
        Deletion will end in deprecation status change from 0 to 1.
        """

        super().__init__()
        loadUi("view/ui_files/deleteUserDialog.ui", self)
        self.setModal(True)  # make it, so you have to interact with the popup first

        self.username = None

        self.delete_dialog_back.clicked.connect(self.close_window)
        self.delete_dialog_delete.clicked.connect(self.deletion_pressed_fct)

    def fill_table_with_entry(self, username: str):
        self.delete_user_name.setText(f'Username = {username}')
        self.username = username

    def close_window(self):
        self.close()

    def deletion_pressed_fct(self):
        print(f'got to deletion_pressed_fct')
        self.deletion_pressed_signal.emit(self.username)


