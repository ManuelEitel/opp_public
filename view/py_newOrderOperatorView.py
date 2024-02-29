from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QLineEdit
from PyQt5 import QtCore as qtc


class NewOrderOperatorViewView(QWidget):

    on_btn_new_ord_for_c = qtc.pyqtSignal(str, str, str, str)
    on_btn_new_ord_for_mw = qtc.pyqtSignal(str, str, str, str)

    def __init__(self):
        """
        The gui for the new order setting up from operator or admin is being done here.
        """
        super().__init__()

        loadUi("view/ui_files/newOrder_operator.ui", self)

        self.make_new_order_operator.clicked.connect(self.signal_for_new_order_from_operator)
        self._name()

    def _name(self):
        """
        renaming for easier readability
        """
        self.customer = self.customer_entrance_new_order_operator
        self.marker1 = self.marker1_entrance_new_order_operator
        self.marker2 = self.marker2_entrance_new_order_operator
        self.due_date = self.due_date_entrance_new_order_operator

    def signal_for_new_order_from_operator(self):
        """
        Emitting of signal for class ControlNewOrderOperator
        """
        if (self.customer.text() == "" or self.marker1.text() == ""
                or self.marker2.text() == "" or self.due_date.text() == ""):
            self.feedback_label.setText("Alle Felder ausfüllen!")

        else:
            self.on_btn_new_ord_for_c.emit(self.customer.text(), self.marker1.text(),
                                           self.marker2.text(), self.due_date.text())

            self.on_btn_new_ord_for_mw.emit(self.customer.text(), self.marker1.text(),
                                            self.marker2.text(), self.due_date.text())

