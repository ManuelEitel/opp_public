from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QWidget, QMainWindow
from PyQt5 import QtCore as qtc


class DeleteDialogView(QDialog):

    del_dial_conf_mw = qtc.pyqtSignal(int)  # confirms pressing "delete button" in ControlMainWindow
    del_confirmed_cd = qtc.pyqtSignal(int)  # confirms pressing for the controldialogclass

    def __init__(self):
        """
        This is the Delete Dialog View of the small Window, that the Operator can call to delete elements. \n
        Deletion will end in deprecation status change from 0 to 1.
        """

        super().__init__()
        loadUi("view/ui_files/deleteDialogOperator.ui", self)
        self.setModal(True)  # make it, so you have to interact with the popup first
        self._bind()

    def _bind(self):
        self.delete_dialog_back.clicked.connect(self.go_back)
        self.delete_dialog_delete.clicked.connect(self.delete_confirmed)

    def fill_at_start(self, item_id: str, name: str, workflow: str, progress: str, marker1: str,
                      marker2: str, due_date: str, notes: str):
        """ This function has to be called from the calling class! """
        self.delete_dialog_id.setText(item_id)

        self.delete_dialog_customer.setText(name)

        self.delete_dialog_workflow.setText(workflow)
        self.delete_dialog_progress.setText(progress)

        self.delete_dialog_marker1.setText(marker1)
        self.delete_dialog_marker2.setText(marker2)

        self.delete_dialog_due_date.setText(due_date)

        self.delete_dialog_notes.setText('Notes')  # The fix is to not put "none" into the db ever


    def delete_confirmed(self):
        """
        Technically the closing of this window should be in ControlSmallDialogs, but it's one line of code.
        """
        self.close()
        self.del_dial_conf_mw.emit(1)
        self.del_confirmed_cd.emit(1)

    def go_back(self):
        """
        Technically the closing of this window should be in ControlSmallDialogs, but it's one line of code.
        """
        self.close()



