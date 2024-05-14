from PyQt5.QtWidgets import QTableWidgetItem, QPushButton
from PyQt5 import QtCore

# import app classes
from view.py_mainWindowView import MainWindowView
from model.model_operator import OperatorAndAdminRights
from control.control_workflow import ControlWorkflow
from control.control_newOrderOperator import ControlNewOrderOperator
from control.control_dialog import ControlDeleteOrder
from control.control_putWorkflowOnOrder import PutWorkflowOnOrder
from control.control_admin import ControlAdmin
from control.control_distribute_task import ControlDistributeTask
from control_timetable.control_user_overview_slector import ControlUserOverviewSelector
from control.progress_tracker import ProgressTracking

# databases stuff
from databases.datatase_handler import Database


class ControlMainwindow:
    """
    Controls the behaviour of the MainWindow of the Operator Person \n
    """
    def __init__(self, model, view, rights):

        super().__init__()
        """
        self.model_main.current_rights  =  Operator, Viewer, Developer, Admin, etc.
        This is the main window from the perspective of the operator. 
        Only god and I know the whole code in here now. I will clean this, even though most subtasks stem from here.
        As the central window of the app, this is prolly the longest bit of code in one file - 
        it will get bigger though.
        """
        self.model = model
        self.view = view
        self.rights = rights

        self.mainWindowView = MainWindowView()
        self.mainWindowView.show()

        self._bind()
        self._init_additional_privileges()
        self.current_mode = None
        self.row = None
        self.delete_dialog = None
        self.new_order_operator = None
        self.workflow_window = None
        self.item_id = None
        self.customer = None
        self.progress = None
        self.workflow = None
        self.marker1 = None
        self.marker2 = None
        self.due_date = None
        self.saved_workflow = None
        self.task_slider_view = None
        self.table_list = None
        self.admin_control = None
        self._set_up_rowcount()

        self._input_data_at_start()

        self.wf_choosingView = None
        self.control_put_workflow_on_order = None
        self.control_distribute_task_overview = None
        self.control_distribute_task_tasks = None
        self.control_time_table_mw = None
        self.mainWindowView.feedback_mw.setReadOnly(True)

        self.mainWindowView.distribute_wf_btn.clicked.connect(self.distribute_wf_btn_fct)
        self.mainWindowView.btn_week_view.clicked.connect(self.open_week_window)
        self.mainWindowView.cell_clicked.connect(self.on_cell_clicked)
        self._setup_usertype()
        self.mainWindowView.mode_btn_clicked_del_wf.connect(self.update_wf)
        self._admin_menu_element_pressed()

    def open_week_window(self):
        self.control_time_table_mw = ControlUserOverviewSelector(self.model)

    def _admin_menu_element_pressed(self):
        self.mainWindowView.actionAdministration.triggered.connect(self.call_admin_window)

    def call_admin_window(self):
        """ From Signal self.mainWindowView.actionAdministration """
        if self.model.current_rights == "admin":
            self.admin_control = ControlAdmin(self.model)

    def update_wf(self, signal_int: int):
        """ After closing Workflow Window the feedback widget is cleared and the saved_workflow is set to None """
        self.saved_workflow = None
        self.mainWindowView.feedback_mw.setText("")

    def _setup_usertype(self):
        """ At initializing the Window the label for the user type is being set """
        self.mainWindowView.usertype_label.setText(self.model.current_rights)

    def distribute_wf_btn_fct(self):
        """ From Signal self.mainWindowView.distribute_wf_btn """
        self.control_put_workflow_on_order = PutWorkflowOnOrder(self.model)
        self.control_put_workflow_on_order.wf_choosingView.cell_clicked_wf_choosing.connect(self.safe_chosen_wf)
        self.mainWindowView.update_btns_all()

    def _init_additional_privileges(self):
        """
        Depending on the usertype some can have certain privileges, that are bein initialized here \n
        self.current_mode is "viewingMode", "deleteMode", "reworkOrderMode", "distributeTasksMode",
            "distributeWorkflowMode"
        """
        if self.model.current_rights == "operator" or self.model.current_rights == "admin":

            self.additional_rights = OperatorAndAdminRights()
            self.current_mode = self.additional_rights.current_mode

        elif self.model.current_rights == "develop":
            self.mainWindowView.mode_widget_3.close()  # dev is not supposed to see this mode
            self.mainWindowView.newOrder.hide()  # dev is not supposed to make a new order

        # ToDo: Design and decide the other modes such as User (=Bearbeiter/Produktionsmitarbeiter)

    def safe_chosen_wf(self, str_signal: str):
        """ The user is distributing workflows and for that the workflow needs to be stored in a parameter
        self.saved_workflow         """
        self.saved_workflow = str_signal  # store parameter
        self.mainWindowView.feedback_mw.setPlainText(f"Now set workflow: {self.saved_workflow}")
        self.current_mode = "distributeWorkflowMode"  # ToDo: Use this for distributing Workflows
        self.control_put_workflow_on_order.wf_choosingView.close()

    def on_cell_clicked(self, row: int, column: int, mouse_button: QtCore.Qt.MouseButton):
        """
        Slot receiving function
            Checks self.current_mode for state and opens the possible cases
                case 1: "viewingMode -> do nothing
                case 2: "deleteMode" -> open the deletion window dialog
        """
        if self.current_mode == "viewingMode":
            pass
        elif self.current_mode == "deleteMode":
            try:
                self.row = row
                order_id = self.mainWindowView.tableWidget.item(self.row, 0).text()
                name = self.mainWindowView.tableWidget.item(self.row, 1).text()
                workflow = self.mainWindowView.tableWidget.item(self.row, 2).text()
                progress = self.mainWindowView.tableWidget.item(self.row, 3).text()
                marker1 = self.mainWindowView.tableWidget.item(self.row, 4).text()
                marker2 = self.mainWindowView.tableWidget.item(self.row, 5).text()
                due_date = self.mainWindowView.tableWidget.item(self.row, 6).text()
                notes = self.mainWindowView.tableWidget.item(self.row, 7).text

                self.delete_dialog = ControlDeleteOrder(item_id=order_id, name=name,
                                                        workflow=workflow, progress=progress, marker1=marker1,
                                                        marker2=marker2, due_date=due_date, note=notes)

                self.delete_dialog.delete_dialog_view.del_dial_conf_mw.connect(self.delete_entry_from_table)

            except AttributeError as e:
                print(f'e = {e}')
        elif self.current_mode == "distributeWorkflowMode":
            workflow_item = QTableWidgetItem(self.saved_workflow)
            self.mainWindowView.tableWidget.setItem(row, 3, workflow_item)
            workflow_item.setFlags(QtCore.Qt.ItemIsEnabled)

            id_item = self.mainWindowView.tableWidget.item(row, 0).text()
            name = self.mainWindowView.tableWidget.item(row, 1).text()

            db = Database("databases/db_main.db")
            db.connect()
            statement = f"""UPDATE table_orders 
                            SET workflow = ?
                            WHERE id = ? AND name = ?"""
            params = (self.saved_workflow, id_item, name)
            db.execute_query(query=statement, params=params)
            db.close()

            wf_length = self.get_workflow_length(self.saved_workflow)

            db = Database("databases/db_main.db")
            db.connect()
            query = f"UPDATE table_orders SET progress = ? WHERE name = ? AND id = ?"
            params = (f"0/{wf_length}", name, id_item)

            db.execute_query(query=query, params=params)

            db.close()
            wf_length_item = QTableWidgetItem(f"0/{wf_length}")
            self.mainWindowView.tableWidget.setItem(row, 2, wf_length_item)
            wf_length_item.setFlags(QtCore.Qt.ItemIsEnabled)

        elif self.current_mode == "distributeTasksMode":
            workflow_to_implement = self.mainWindowView.tableWidget.item(row, 3).text()
            item_name = self.mainWindowView.tableWidget.item(row, 1).text()
            self.control_distribute_task_tasks = ControlDistributeTask(self.model, self.view,
                                                                       workflow_to_implement, item_name)

    @staticmethod
    def get_workflow_length(saved_workflow: str):

        db = Database("databases/db_workflows.db")
        db.connect()

        query = f"SELECT COUNT(*) FROM {saved_workflow}"

        wf_data = db.fetch_data(query)
        db.close()
        wf_length = wf_data[0][0]

        return wf_length


    def delete_entry_from_table(self, integer_for: int):
        """ UI Handling of the deletion of an order """
        self.mainWindowView.tableWidget.removeRow(self.row)

    def put_delete_dialog_back_to_none(self, integer: int):
        """ self.delete_dialog is supposed to be None, unless it's open. """

        self.delete_dialog = None

    def _input_data_at_start(self):
        """ MainWindow needs its entrances read from db and put into table. """
        ## hier dann noch das feld rein, dass es das richtig in die table rein schiebt
        db = Database("databases/db_main.db")
        db.connect()
        statement = "SELECT * FROM table_orders WHERE deprecated = 0;"
        data = db.fetch_data(statement)
        db.close()
        if data is not None:
            for element in data:
                print(f'element from data = {element}')
                old_progress = element[2]
                new_progress = self.change_orders_acc_to_progress(element[1], element[2], element[3])
                print(f'new_progress = {new_progress}')
                new_element = (element[0], element[1], new_progress, element[3], element[4], element[5], element[6],
                               element[7])
                self._orders_from_db_in_tabular(new_element)

                if new_progress != old_progress:
                    db = Database("databases/db_main.db")
                    db.connect()

                    query = f"""UPDATE table_orders SET progress = ? WHERE name = ? AND workflow = ? AND deprecated = 0"""

                    params = (new_progress, element[1], element[3])

                    db.execute_query(query=query, params=params)

                    db.close()



    def change_orders_acc_to_progress(self, order_name: str, curr_progress: str, wf: str):
        progress_tracker = ProgressTracking(order_name=order_name, curr_progress=curr_progress, wf=wf)
        print(f'got here again')
        return progress_tracker.curr_progress

    def _orders_from_db_in_tabular(self, element: tuple):
        """
        Set row count one up (it's 0 at initiation), since we add new element (this might change later) \n
        Change the dictionary into two nice lists \n
        Iterate through the columns and make the table read only.
        |name|progress|marker1|marker2|due_date|notes|deprecated|
        """
        self.rowCount += 1
        self.mainWindowView.tableWidget.setRowCount(self.rowCount)
        element_list = [element[0], element[1], element[2], element[3], element[4], element[5], element[6], element[7]]
        print(f'element_list = {element_list}')
        i = 0
        for entry in element_list:
            item = QTableWidgetItem(str(entry))
            self.mainWindowView.tableWidget.setItem(self.rowCount-1, i, item)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            i += 1

    def _bind(self):
        """
        Binds the signal "change_style" from the class MainWindowView() to this
        """
        self.mainWindowView.change_style.connect(self.update_mode)  # done
        self.mainWindowView.createWorkflow.clicked.connect(self.open_workflow_window)
        self.mainWindowView.newOrder.clicked.connect(self.open_new_order_widget)  # done

    def open_workflow_window(self):
        """
        opens control Workflow and gives usertype through
        """
        self.workflow_window = ControlWorkflow(self.model)

    def open_new_order_widget(self):
        """
        opens control New Order Operator and gives usertype through
        """
        self.new_order_operator = ControlNewOrderOperator(self.model, self.view, self.rights)
        self.new_order_operator.new_order_from_operator.on_btn_new_ord_for_mw.connect(
            self.insert_new_operator_order_in_tabular)

    def insert_new_operator_order_in_tabular(self, customer: str, marker1: str, marker2: str,
                                             due_date: str):
        """
        Note: I know how this can be coded much prettier, but there is just now no time. \n
        After receiving signal "second_signal_order_button_clicked" in func self.open_new_order_widget, when there is
        the button clicked the stuff already is in database and now the new query is being put into the ui for
        further usage.
        """
        db = Database("databases/db_main.db")
        db.connect()

        statement = """SELECT * FROM table_orders WHERE deprecated = '0'; """
        rows = db.fetch_data(statement)

        new_entry = rows[-1]
        new_entry_list = [new_entry[0], new_entry[1], new_entry[2], new_entry[3], new_entry[4],
                          new_entry[5], new_entry[6], new_entry[7]]  # deprecated is entry8 and doesnt matter

        self.mainWindowView.tableWidget.insertRow(0)

        for index, element in enumerate(new_entry_list):
            item = QTableWidgetItem(element)
            self.mainWindowView.tableWidget.setItem(0, index, item)
            item.setFlags(QtCore.Qt.ItemIsEnabled)

        self.new_order_operator = None

    def update_mode(self, button_delete: QPushButton, button_change: QPushButton, button_distribute: QPushButton,
                    button_string: str):
        """
        Three modes: delete_mode, change_mode, distributeTask_mode - visually done
        ToDo: Create in class Operator a way to keep track of his modes of operations
        Currently all this does is paint the buttons yellow
        """
        if button_string == "delete":
            if button_delete.isChecked():
                self.current_mode = "deleteMode"
            else:
                self.current_mode = "viewingMode"
        if button_string == "change":
            if button_change.isChecked():
                self.current_mode = "reworkOrderMode"
            else:
                self.current_mode = "viewingMode"

        if button_string == "distribute":
            if button_distribute.isChecked():
                self.current_mode = "distributeTasksMode"
            else:
                self.current_mode = "viewingMode"

    def _set_up_rowcount(self):
        """
        self.rowCount is the number of the rows and at the beginning of the empty app there is nothing inside
        unless it's being filled
        """
        self.rowCount = 0
        self.mainWindowView.tableWidget.setRowCount(self.rowCount)
