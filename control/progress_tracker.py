from databases.datatase_handler import Database

class ProgressTracking:

    def __init__(self, order_name: str, curr_progress: str, wf: str):
        """
        Asks the current progress in the wf data sheet and gives back info about that """
        self.order_name = order_name
        self.curr_progress = curr_progress
        self.wf = wf
        self.collect_wf_data()

    def collect_wf_data(self):
        data = self.orders()
        if not data:
            return "Not given yet"
        deprecated_have = 0
        deprecated_from_total = len(data)
        for element in data:
            if element[3] != 0:
                deprecated_have += 1
        self.curr_progress = f"{deprecated_have}/{deprecated_from_total}"
        return self.curr_progress

    def orders(self):

        db = Database('databases/db_wf_usr_conn.db')
        db.connect()
        table_name = f"wf_{self.wf}_ordr_{self.order_name}"
        query = f"SELECT * FROM {table_name}"

        data = db.fetch_data(query)
        print(f'special data = {data}')  # None
        db.close()

        return data
