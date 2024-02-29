from view.py_newOrderOperatorView import NewOrderOperatorViewView
from databases.datatase_handler import Database


class ControlNewOrderOperator:

    def __init__(self, model, view, rights):
        """
        Here we decide what happens with the Entries in the custom widget for the Operator, when he
        makes a new Order \n
        Sending out Signal database_signal to the class ControlMainWindow
        """
        self.model = model
        self.view = view
        self.rights = rights

        self.new_order_from_operator = NewOrderOperatorViewView()
        self.new_order_from_operator.show()

        self.new_order_from_operator.on_btn_new_ord_for_c.connect(self.close_dialog_and_put_query_into_db)

    def close_dialog_and_put_query_into_db(self, customer: str, marker1: str,
                                           marker2: str, due_date: str):
        """
        The Dialog of the new Order Window is being closed here. \n
        Also the
        """
        self.new_order_from_operator.close()
        db = Database("databases/db_main.db")
        db.connect()

        find_highest_id = """SELECT id FROM table_orders;"""
        highest_id = db.fetch_data(find_highest_id)

        if not highest_id:
            print(f'this case')
            next_id = 1
        else:
            next_id = self.get_next_id(highest_id=highest_id)

        statement = "INSERT INTO table_orders VALUES (?,?,?,?,?,?,?,?,?)"

        params = (next_id, customer, "Not given yet", "Not given yet",  marker1, marker2, due_date, "none", "0")

        db.execute_query(query=statement, params=params)

    @staticmethod
    def get_next_id(highest_id: list):
        """ Probably my best function so far """

        max_ele = 0
        for ele in highest_id:
            if int(ele[0]) > max_ele:
                max_ele = int(ele[0])
        max_ele = max_ele + 1

        return str(max_ele)






