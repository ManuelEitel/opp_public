from view.py_workflowView import WorkflowWindowView
from view.py_new_wf_step import NewWFStep
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtCore
from view.py_workflow_deletestep import DeleteWFStep
from databases.datatase_handler import Database


class ControlWorkflow(object):
    """
    Controls the behaviour of the Workflow Window of the user Person \n

    """
    def __init__(self, model):

        self.model = model

        self.wf_view = WorkflowWindowView()
        self.wf_view.show()
        self._setup_usertype()
        self.wf_new_step = None
        self.rowCount = 0
        self.wf_del_step = None
        self.wf_view.delete_step.clicked.connect(self.call_wf_delete_window)
        self.element_list = []  # a list of all the current Steps in the workflow that is about to be created
        self.wf_view.create_workflow_btn.clicked.connect(self.put_wf_in_db)
        self.wf_view.btn_new_step.clicked.connect(self.call_wf_new_step)

    def get_data_from_table_to_put_wf_in_db(self):

        rows = self.wf_view.tableWidget_Workflow.rowCount()

        row_data = []

        for row_index in range(rows):
            row_list = []
            for column_index in range(self.wf_view.tableWidget_Workflow.columnCount()):
                item = self.wf_view.tableWidget_Workflow.item(row_index, column_index)
                if item is not None:
                    row_list.append(item.text())
                else:
                    row_list.append("")
            row_data.append(row_list)
        return row_data

    def put_wf_in_db(self):
        row_data = self.get_data_from_table_to_put_wf_in_db()
        print(f'row_data = {row_data}')
        db = Database("databases/db_workflows.db")
        db.connect()
        table_name = self.wf_view.workflow_name_field.text()
        select_tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = db.fetch_data(select_tables_query)
        table_names = [table[0] for table in tables]

        if table_name not in table_names:
            statement = f"""
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    workplace VARCHAR(30),
                    name VARCHAR(30),
                    est_time VARCHAR (10),
                    linked_after VARCHAR(30), 
                    linked_before VARCHAR(30), 
                    user_empty VARCHAR(30),
                    other VARCHAR(1000)
                )
            """
            db.execute_query(statement)
            for element in row_data:
                workplace = element[0]
                name = element[1]
                est_time = element[2]
                next_step = element[3]
                previous_step = element[4]
                other = element[5]
                input_statement = f"""INSERT INTO {table_name} (
                                    workplace, name, est_time, linked_after, linked_before, other
                                    )
                                    VALUES (?,?,?,?,?,?)
                    """
                params = (workplace, name, est_time, next_step, previous_step, "Not yet")
                db.execute_query(query=input_statement, params=params)
        self.wf_view.close()
        db.close()

    def call_wf_delete_window(self):
        self.wf_del_step = DeleteWFStep(self.model, self.element_list)
        self.wf_del_step.deletion_clicked.connect(self.del_ele_from_table)
        self.wf_del_step.show()

    def del_ele_from_table(self, number: int):
        if number != 0:
            self.wf_view.tableWidget_Workflow.removeRow(number-1)

    def call_wf_new_step(self):
        """
        This window is for putting an entry into the Workflow
        """
        self.wf_new_step = NewWFStep(self.model)
        self.wf_new_step.pushed_new_step.connect(self.put_query_for_wf_in_table)
        self.wf_new_step.show()

    def put_query_for_wf_in_table(self, name_of_step: str, wf_next_step: str,
                                  wf_prev_step: str, wf_est_time: str, wf_workplace: str):
        """
        The query comes from a signal self.pushed_new_step from the wf_new_step window \n
        Four strings, which are never "" this. \n
        They are being put into the table self.wf_view.tableWidget_Workflow and not into the db yet.
        """

        self.rowCount += 1
        self.wf_view.tableWidget_Workflow.setRowCount(self.rowCount)

        element_list = [wf_workplace, name_of_step, wf_est_time, wf_next_step, wf_prev_step]
        self.element_list.append(element_list)

        i = 0
        for entry in element_list:
            item = QTableWidgetItem(entry)
            self.wf_view.tableWidget_Workflow.setItem(self.rowCount-1, i, item)
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            i += 1

    def _setup_usertype(self):
        self.wf_view.label_user_type_workflow.setText(self.model.current_rights)


