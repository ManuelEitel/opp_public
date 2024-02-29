from view.py_deleteDialog import DeleteDialogView
from databases.datatase_handler import Database


class ControlDeleteOrder(object):

    def __init__(self, item_id: str, name: str, workflow: str, progress: str,
                 marker1: str, marker2: str, due_date: str, note: str):
        """ An order is deleted here """
        self.delete_dialog_view = DeleteDialogView()

        self.delete_dialog_view.show()
        self.wf_new_step = None

        self.item_id = item_id
        self.name = name
        self.workflow = workflow
        self.progress = progress
        self.marker1 = marker1
        self.marker2 = marker2
        self.due_date = due_date
        self.notes = note
        self.delete_dialog_view.fill_at_start(item_id=self.item_id, name=self.name, workflow=self.workflow,
                                              progress=self.progress, marker1=self.marker1, marker2=self.marker2,
                                              due_date=self.due_date, notes=self.notes)
        self.delete_dialog_view.del_confirmed_cd.connect(self.delete_from_db)

    def delete_from_db(self, integer_for_signal_slot: int):

        db = Database("databases/db_main.db")
        db.connect()
        statement = """UPDATE table_orders
                        SET deprecated = '1'
                        WHERE id = ? AND name = ? AND marker1 = ? AND marker2 = ? AND due_date = ?"""
        params = (self.item_id, self.name, self.marker1, self.marker2, self.due_date)

        db.execute_query(query=statement, params=params)
        db.close()

