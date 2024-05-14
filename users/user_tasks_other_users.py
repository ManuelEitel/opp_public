from databases.datatase_handler import Database
import regex as re

class CheckOtherUserTasks(object):

    def __init__(self, user_name: str, task: str, workflow: str, date, order: str):
        """
        Object is only there to erase possible doubles if they are deprecated = 0
        This class explicitly checks, if other users have the selected task already and then erases that task
        from their databases.

        Input params:
        :user_name: The string of the user_name
        :task: The string of the task
        :workflow: The string of the workflow name
        :date: If given, when to place the task
        """

        self.user_name = user_name
        self.task = task
        self.workflow = workflow
        self.date = date
        self.order = order

        user_name_list = self.call_all_user_names()
        filenames = self.translate_username_list_into_filenames(user_name_list)
        self.check_each_file_for_doubling_and_erase_if_so(filenames, user_name_list)

    def check_each_file_for_doubling_and_erase_if_so(self, filenames: list, user_name_list: list):
        for i in range(len(filenames)):
            all_tasks_from_user_x, user_name = self.check_individual_file(filenames[i], user_name_list[i])
            self.search_for_doubling(all_tasks_from_user=all_tasks_from_user_x, user_name=user_name)

    def search_for_doubling(self, all_tasks_from_user: list, user_name: str):
        """
        Erases cases, that are the same order, task and workflow.
        params: all_tasks_from_user: list
        params: user_name: str
        """

        for element in all_tasks_from_user:
            step = element[1]
            workflow = element[2]
            order = element[5]

            if self.task == step and self.workflow == workflow:  # case doubling; the task was given to someone before
                self.erase_overwritten_user_task(user_name, self.task, self.workflow, order)

    def erase_overwritten_user_task(self, user_name: str, task: str, workflow: str, order: str):
        """ Erases from the three databases the hints of the old given task """
        self.erase_from_db_user_tasks_db(user_name=user_name, task=task, workflow=workflow, order=order)
        self.update_progress_in_table_orders_in_db_main_db(user_name=user_name, task=task,
                                                           workflow=workflow, order=order)
        self.erase_from_db_wf_usr_conn_db(user_name=user_name, task=task, workflow=workflow, order=order)

    def erase_from_db_wf_usr_conn_db(self, user_name: str, task: str, workflow: str, order: str):
        db = Database("databases/db_wf_usr_conn.db")
        db.connect()

        table_name = f"wf_{workflow}_ordr_{order}"

        query = f"UPDATE {table_name} SET user_name = ?, user_time = ? WHERE user_name = ? AND step_name = ? AND deprecated = 0"
        params = ("Removed", "Removed", user_name, task)

    def update_progress_in_table_orders_in_db_main_db(self, user_name: str, task: str, workflow: str, order: str):
        """ Progress Updating required 3/4 -> 2/4 """

        db = Database("databases/db_main.db")
        db.connect()

        query = """SELECT progress FROM table_orders WHERE workflow = ? AND name = ? """
        params = (workflow, order)

        progress_list = db.fetch_data(query=query, params=params)

        progress = progress_list[0][0]

        print(f'Successfully pulled progress "{progress}" through self.erase_from_table_orders_on_main_db')

        new_progress = self.downgrade_progress_by_one(progress=progress)

        query_1 = f"UPDATE table_orders set progress = ? WHERE name = ? AND workflow = ? AND deprecated = 0"

        params_1 = (new_progress, order, workflow)

        db.execute_query(query=query_1, params=params_1)

        db.close()



    def downgrade_progress_by_one(self, progress: str):

        match = re.findall(r'\d*/', progress)
        match = match[0][:-1]
        match2 = re.findall(r'/\d*', progress)
        match2 = match2[0][1:]
        int_got = int(match)
        int_from = int(match2)
        if int_got != 0:
            int_got_new = int_got - 1
            return str(f'{int_got_new}/{int_from}')
        else:
            return str(f'0/{int_from}')

    @staticmethod
    def erase_from_db_user_tasks_db(user_name: str, task: str, workflow: str, order: str):
        db = Database(f'databases/db_{user_name}_tasks.db')
        db.connect()

        query = f"""DELETE FROM user_tasks WHERE task = ? AND workflow = ? AND order_name = ? AND deprecated = 0"""
        parameter = (task, workflow, order, )

        db.execute_query(query=query, params=parameter)
        db.close()

    @staticmethod
    def check_individual_file(filename: str, user_name: str):
        db = Database(f'databases/{filename}')
        db.connect()

        checking_query_for_table_user_tasks = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        checking_params = ("user_tasks",)

        table_exists = db.fetch_data(query=checking_query_for_table_user_tasks, params=checking_params)

        if table_exists:
            query = "SELECT * from user_tasks WHERE deprecated = 0"
            all_tasks = db.fetch_data(query)

            db.close()

            return all_tasks, user_name[0]

        else:
            db.close()
            return [], user_name[0]

    @staticmethod
    def call_all_user_names() -> list:
        db = Database("databases/db_main.db")
        db.connect()

        query = """SELECT name FROM table_users WHERE rights = 'User'"""

        user_name_list = db.fetch_data(query)

        db.close()

        return user_name_list

    @staticmethod
    def translate_username_list_into_filenames(user_name_list: list) -> list:

        filenames = []

        for element in user_name_list:
            filename = f'db_{element[0]}_tasks.db'
            filenames.append(filename)

        return filenames
