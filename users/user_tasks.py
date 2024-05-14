import datetime
import os
import sqlite3
from databases.datatase_handler import Database
from control_timetable.workhours_manager import WorkHoursManager


class ManageUserTasks(object):

    def __init__(self, user_name: str, task: str, workflow: str, date, order: str):
        """
        This class manages the database of the user called "db_{user_name}_tasks.db".
        Input params:
        :user_name: The string of the user_name
        :task: The string of the task
        :workflow: The string of the workflow name
        :date: If given, when to place the task

        This class calls the class WorkHoursManager to get shift slots
        """
        self.user_name = user_name
        self.task = task
        self.workflow = workflow

        self.date = date  # type not clear perhaps make it *args or even *kwargs

        self.order = order

        self.time_now_in_hours_mins = None

        self.task_time = self.pull_task_time_from_workflow()

        self.workhours_manager = WorkHoursManager(user=self.user_name, task_time=self.task_time)
        self.current_date = datetime.datetime.now().strftime("%d.%m.%Y")
        self.db_name = f'db_{self.user_name}_tasks.db'  # for each user this name is the same

        self._setup_user_db()
        self._create_table_if_not_exists()

    def _setup_user_db(self):
        """ Creates Database file for user, if not already existing """

        self.curr_dir = os.path.dirname(os.path.abspath(__file__))
        self.main_dir = os.path.dirname(self.curr_dir)  # hops one directory above (where we wanna be)

        self.database_dir = os.path.join(self.main_dir, "databases", self.db_name)

        if not os.path.exists(self.database_dir):
            conn = sqlite3.connect(self.database_dir)
            conn.close()

    def _create_table_if_not_exists(self):
        """ Creates the table user_tasks inside the user, where all his data is being stored """
        db = Database(self.database_dir)
        db.connect()
        query = """CREATE TABLE IF NOT EXISTS user_tasks (
                        date CHAR(30),
                        task CHAR(30),
                        workflow CHAR(30),
                        task_begin INT,
                        task_end INT,
                        order_name CHAR(30),
                        deprecated INT
                        )"""

        db.execute_query(query)
        db.close()

    def get_all_non_deprecated_user_tasks(self) -> list:
        """ Calls db table user_tasks und returns list of all the tasks, the user has, that are non deprecated """

        db = Database(self.database_dir)
        db.connect()

        query = """ SELECT * FROM user_tasks WHERE deprecated = 0"""
        non_deprecated_tasks_list = db.fetch_data(query)

        db.close()
        return non_deprecated_tasks_list

    def get_relevant_dates(self) -> tuple:
        """
        weeks: [(0, (01.01.24)), (1, (02.01.24)), ...]
        this_week: [01.01.24, 02.01.24, 03.01.24, ..., 07.01.24] for this current week
        next_week: same as this week, except next week
        today: current date format: 01.01.24
        next_monday: for weekend cases date of next monday format 01.01.24
        """
        self.workhours_manager.get_current_date_and_week()

        workday = None

        for index, date in enumerate(self.workhours_manager.current_week):
            if date == self.workhours_manager.current_date:
                workday = index

        weeks = self.workhours_manager.timetable_dates_manager.weeks
        this_week = weeks[self.workhours_manager.current_week_index-1][1]
        next_week = weeks[self.workhours_manager.current_week_index][1]
        today = self.workhours_manager.current_date
        next_monday = next_week[0]

        return weeks, this_week, next_week, today, next_monday, workday  # workday is an index! [0:5]

    def deprecate_date(self, date: str, step_name: str, wf_name: str):
        """ Given Entry gets put into the deprecated = 1 state """

        db = Database(self.database_dir)
        db.connect()

        params = (date, step_name, wf_name)

        query = """ UPDATE user_tasks
                    SET deprecated = 1
                    WHERE date = ?
                        AND task = ?
                        AND workflow = ?;"""

        db.execute_query(query=query, params=params)

        db.close()

    def deprecate_past_user_tasks(self, all_non_deprecated_user_tasks: list):
        """
        Given a User Task List, where all his tasks, that are not deprecated (state deprecated=0) are listed,
        this function puts the dates, that are in the past (at least yesterday) into the state deprecated=1.

        """
        for element in all_non_deprecated_user_tasks:
            date = element[0]
            step_name = element[1]
            wf_name = element[2]

            if self.date_in_the_past(date):  # case: date in the past
                self.deprecate_date(date=date, step_name=step_name, wf_name=wf_name)

    @staticmethod
    def date_in_the_past(date_str: str):
        """
        Checks, if given date is (in the past) or (today and future) in day steps
        Function returns True, if given date is in the past.
        """

        date_format = "%d.%m.%Y"
        input_date = datetime.datetime.strptime(date_str, date_format)

        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        if input_date <= today:
            return True
        else:
            return False

    @staticmethod
    def erase_tasks_that_are_after_now(time_delta_list: list, now_in_mins: int) -> list:
        """
        Filter the time_delta_list (e.g. [(480, 490), (490, 500), (520, 620), (780, 880)]) in such a way, that all
        tasks, that already happened today are being ignored. A list with all the tasks, that need to be considered
        is being produced
        """
        delta_list_for_today_with_now_time_considered = []

        for element in time_delta_list:
            start_time = element[0]

            if start_time >= now_in_mins:
                delta_list_for_today_with_now_time_considered.append(element)

        return delta_list_for_today_with_now_time_considered

    @staticmethod
    def find_time_slot_today(time_delta_shorted: list, time_slot: int, date: str, now_in_int: int):
        """
        The same as find_time_slot_not_today, but with the difference, that elements should not be integrated into
        those times, that are already passed.
        """

        # Case: Go through shorted list.
        for i in range(len(time_delta_shorted)):

            if i == 0:
                # Check if we can put the new task before the first element
                # Starting time of first element in today's tasks
                time_start_0 = time_delta_shorted[i][3]
                time_end_0 = time_delta_shorted[i][4]

                # First current task is after 8 o'Clock, but before the lunch break
                # Bingo! We might fit the task before, though?
                if time_start_0 > 480 and 720 > time_end_0 > now_in_int:
                    # Check, if we can fit the task before. If so, make entry.
                    if 480 + time_slot <= time_start_0 and time_end_0 < now_in_int:

                        """Case put something into a slot and returned that slot data"""
                        # print(f'result_{i} = {[date, 480, 480+time_slot]}')
                        return [date, 480, 480 + time_slot]

                # Check, if the task 0 is in the second half of the day (afternoon)
                elif time_start_0 >= 780 and 1020 >= time_end_0 > now_in_int:

                    """Case put it at 8 o'Clock """
                    # print(f'result_{i} = {[date, 480, 480 + time_slot]}')
                    return [date, 480, 480 + time_slot]

                # First current task is already happening at 8 o'Clock
                elif time_start_0 == 480 and time_end_0 > now_in_int:

                    # Case: There is no other task, other than task 0 in the time_delta_list
                    # We can check, if we want to put the task before or directly after the lunch break
                    if len(time_delta_shorted) == 1:

                        # Make sure it fits before the lunch break
                        if time_end_0 + time_slot <= 720:
                            return [date, time_end_0, time_end_0 + time_slot]

                        # It does not fit before the lunch break, but also does not go over the 17 o'clock line
                        elif 720 < time_end_0 + time_slot < 1020:
                            return [date, 780, 780 + time_slot]

                        # Case the first task goes from 480 to 720
                        elif time_end_0 == 720:
                            return [date, 780, 780 + time_slot]


                    # Since we are iterating over the elements and connect them with the next element,
                    # we have to check the case where the task 0 has a task 1 following and check the cases
                    # where the new task fits
                    elif len(time_delta_shorted) > 1:

                        time_start_0 = time_delta_shorted[i][3]
                        time_end_0 = time_delta_shorted[i][4]
                        time_start_1 = time_delta_shorted[i + 1][3]
                        time_end_1 = time_delta_shorted[i + 1][4]

                        # case only one other element. fits before the break
                        if time_end_0 < 720 and time_end_0 + time_slot <= time_start_1 and time_end_0 + time_slot < 780:
                            return [date, time_end_0, time_end_0 + time_slot]

                        if time_end_0 == 720 and 780 + time_slot < time_start_1:
                            return [date, 780, 780 + time_slot]

            # i != 0: And it's currently still before 8 o'Clock
            if i != 0:
                # At this point, the time_delta_list will be longer than 1, because this is case at least i = 1.
                # all, but the last task case are being checked here:
                if i < len(time_delta_shorted) - 1:
                    """ 
                    i starts from 0 to len(time_delta_list)-1, so to not meet the last element we only go to
                    the second last element, which is i = len(time_delta_list) - 2
                    """
                    time_start_0 = time_delta_shorted[i][3]
                    time_end_0 = time_delta_shorted[i][4]
                    time_start_1 = time_delta_shorted[i + 1][3]
                    time_end_1 = time_delta_shorted[i + 1][4]

                    # Case we are before lunch break and the task fits between current and next order
                    if (now_in_int < time_end_0 < 720 and time_end_0 + time_slot <= 720
                            and time_end_0 + time_slot <= time_start_1):
                        return [date, time_end_0, time_end_0 + time_slot]

                    # Case the new task does not fit behind the task 0 before the lunch break, but right after the
                    # lunch break before task 1
                    elif (time_end_0 + time_slot >= 720 >= time_end_0 > now_in_int and 780 + time_slot <= time_start_1
                          and time_end_0 > now_in_int):
                        return [date, time_end_0, time_end_0 + time_slot]

                    # Case the task 0 is already in the afternoon and we fit him between him and the next element
                    elif time_end_0 >= 780 and time_end_0 + time_slot <= time_start_1 and time_end_0 > now_in_int:
                        return [date, time_end_0, time_end_0 + time_slot]

                # We are at the last element and haven't returned anything yet.
                # It is still before 8 o'Clock
                # The element can be before or after the lunch break
                elif i == len(time_delta_shorted) - 1:

                    time_start_0 = time_delta_shorted[i][3]
                    time_end_0 = time_delta_shorted[i][4]

                    # case the new element fits before lunch break
                    if now_in_int < time_end_0 < 720 and time_end_0 + time_slot <= 780:
                        return [date, time_end_0, time_end_0 + time_slot]

                    # case the new element cannot be fittet between task 0 and lunch break
                    elif now_in_int < time_end_0 < 720 and time_end_0 + time_slot > 780:
                        return [date, 780, 780 + time_slot]

                    # the last task ends right before the lunch break
                    elif time_end_0 == 720 and time_end_0 > now_in_int:
                        return [date, 780, 780 + time_slot]

                    # case regular fits after task_end into this day
                    elif now_in_int < time_end_0 < 1020 and time_end_0 + time_slot <= 1020:
                        return [date, time_end_0, time_end_0 + time_slot]

                    # case the last task of the day ends a 17 o'Clock
                    elif time_end_0 == 1020 and now_in_int < time_end_0:
                        return []

        # print(f'result_NONE = []')
        return []

    def find_time_slot_not_today(self, time_delta_list: list, time_slot: int, date: str):
        """
        This is a function that only tries to fit a number as a slot, a delta, into a space between to deltas.
        returns data list [date- string, time in int where the task starts, time in int where the task ends]
        or [], if it doesn't fit into the day at all.
        """
        # Case: Go through whole day

        for i in range(len(time_delta_list)):

            if i == 0:
                # Check if we can put the new task before the first element
                # Starting time of first element in today's tasks
                time_start_0 = time_delta_list[i][3]
                time_end_0 = time_delta_list[i][4]

                # First current task is after 8 o'Clock, but before the lunch break
                # Bingo! We might fit the task before, though?
                if time_start_0 > 480 and time_end_0 < 720:

                    # Check, if we can fit the task before. If so, make entry.
                    if 480 + time_slot <= time_start_0:

                        """Case put something into a slot and returned that slot data"""
                        # print(f'result_{i} = {[date, 480, 480+time_slot]}')
                        return [date, 480, 480 + time_slot]

                # Check, if the task 0 is in the second half of the day (afternoon)
                elif time_start_0 >= 780 and time_end_0 <= 1020:

                    """Case put it at 8 o'Clock """
                    # print(f'result_{i} = {[date, 480, 480 + time_slot]}')
                    return [date, 480, 480 + time_slot]

                # First current task is already happening at 8 o'Clock
                elif time_start_0 == 480:

                    # Case: There is no other task, other than task 0 in the time_delta_list
                    # We can check, if we want to put the task before or directly after the lunch break
                    if len(time_delta_list) == 1:

                        # Make sure it fits before the lunch break
                        if time_end_0 + time_slot <= 720:

                            return [date, time_end_0, time_end_0 + time_slot]

                        # It does not fit before the lunch break, but also does not go over the 17 o'clock line
                        elif 720 < time_end_0 + time_slot < 1020:

                            return [date, 780, 780 + time_slot]

                        # Case the first task goes from 480 to 720
                        elif time_end_0 == 720:

                            return [date, 780, 780 + time_slot]


                    # Since we are iterating over the elements and connect them with the next element,
                    # we have to check the case where the task 0 has a task 1 following and check the cases
                    # where the new task fits
                    elif len(time_delta_list) > 1:

                        time_start_0 = time_delta_list[i][3]
                        time_end_0 = time_delta_list[i][4]
                        time_start_1 = time_delta_list[i + 1][3]
                        time_end_1 = time_delta_list[i + 1][4]

                        # case only one other element. fits before the break
                        if time_end_0 < 720 and time_end_0 + time_slot <= time_start_1 and time_end_0 + time_slot < 780:

                            return [date, time_end_0, time_end_0 + time_slot]

                        if time_end_0 == 720 and 780 + time_slot < time_start_1:
                            return [date, 780, 780 + time_slot]

            # i != 0: And it's currently still before 8 o'Clock
            if i != 0:
                # At this point, the time_delta_list will be longer than 1, because this is case at least i = 1.
                # all, but the last task case are being checked here:
                if i < len(time_delta_list) - 1:
                    """ 
                    i starts from 0 to len(time_delta_list)-1, so to not meet the last element we only go to
                    the second last element, which is i = len(time_delta_list) - 2
                    """
                    time_start_0 = time_delta_list[i][3]
                    time_end_0 = time_delta_list[i][4]
                    time_start_1 = time_delta_list[i + 1][3]
                    time_end_1 = time_delta_list[i + 1][4]

                    # Case we are before lunch break and the task fits between current and next order
                    if time_end_0 < 720 and time_end_0 + time_slot <= 720 and time_end_0 + time_slot <= time_start_1:

                        return [date, time_end_0, time_end_0 + time_slot]

                    # Case the new task does not fit behind the task 0 before the lunch break, but right after the
                    # lunch break before task 1
                    elif time_end_0 <= 720 <= time_end_0 + time_slot and 780 + time_slot <= time_start_1:
                        return [date, time_end_0, time_end_0 + time_slot]

                    # Case the task 0 is already in the afternoon and we fit him between him and the next element
                    elif time_end_0 >= 780 and time_end_0 + time_slot <= time_start_1:

                        return [date, time_end_0, time_end_0 + time_slot]

                # We are at the last element and haven't returned anything yet.
                # It is still before 8 o'Clock
                # The element can be before or after the lunch break
                elif i == len(time_delta_list) - 1:

                    time_start_0 = time_delta_list[i][3]
                    time_end_0 = time_delta_list[i][4]

                    # case the new element fits before lunch break
                    if time_end_0 < 720 and time_end_0 + time_slot <= 780:

                        return [date, time_end_0, time_end_0 + time_slot]

                    # case the new element cannot be fittet between task 0 and lunch break
                    elif time_end_0 < 720 and time_end_0 + time_slot > 780:
                        return [date, 780, 780 + time_slot]

                    # the last task ends right before the lunch break
                    elif time_end_0 == 720:
                        return [date, 780, 780 + time_slot]

                    # case regular fits after task_end into this day
                    elif time_end_0 < 1020 and time_end_0 + time_slot <= 1020:
                        # print(f'time_end_0 = {time_end_0}')
                        return [date, time_end_0, time_end_0 + time_slot]

                    # case the last task of the day ends a 17 o'Clock
                    elif time_end_0 == 1020:

                        return []

        return []

    def put_into_next_timeslot_when_data_there_alrdy(self):
        """
        Returns: int(time_of_entry), int(time_of_entry+int_task_time), date_of_entry, "string"
        See into the testfile honestly. this one is a big function (algorithm), that finds the sweet spot of any
        task and any given time constellation of already existing tasks.

        The main functions are:
         * self.find_time_slot_today(element, int_task_time)
           The user wants to give tasks today and depending on how late it is you can't put tasks into the past
           This function finds the spot in accordance to the current time
           If you want to understand this function first check the next function, then return to this.

         * self.find_time_slot_not_today(element, int_task_time)
           If a task does not need to be put into today, that means, we can neglect the hour:min-time and just
           iterate through the whole day if the task can fit there. Difficulties are break times. But that's doable.
        """

        all_non_deprecated_user_tasks = self.get_all_non_deprecated_user_tasks()

        self.deprecate_past_user_tasks(all_non_deprecated_user_tasks=all_non_deprecated_user_tasks)  # error handling 1

        ordered_current_steps = self.order_current_steps(all_non_deprecated_user_tasks)

        #get workflow - length
        task_time = self.get_task_length(self.workflow)
        int_task_time = self.workhours_manager.time_str_into_int_minutes(task_time[0])

        time_of_entry = None
        date_of_entry = None
        timeplace = None
        placing_date = None

        for element in ordered_current_steps:

            # Divide between elements, that have date of today (where we might have to change our approach of
            # distributing the tasks depending on how much o'Clock it is right now

            element_date = element[0][0]
            user_time_manager = WorkHoursManager(user=self.user_name, task_time=task_time)
            current_correct_date = user_time_manager.current_date
            current_now = datetime.datetime.now()
            hours = current_now.hour
            minutes = current_now.minute

            placing_list = None

            now_in_int = 60 * int(hours) + int(minutes)

            if element_date == current_correct_date:
                time_delta_shorted = self.erase_tasks_that_are_after_now(time_delta_list=element,
                                                                         now_in_mins=now_in_int)

                placing_list = self.find_time_slot_today(time_delta_shorted=time_delta_shorted, time_slot=int_task_time,
                                                         date=element_date, now_in_int=now_in_int)


            if element_date != current_correct_date:

                placing_list = self.find_time_slot_not_today(time_delta_list=element, time_slot=int_task_time,
                                                             date=element_date)

            placing_date = placing_list[0]
            timeplace = placing_list[1]
            timeplace_end = placing_list[2]

            self.make_entry_user_task(date=placing_date, time_begin=timeplace, time_end=timeplace_end)
            self.update_wf_usr_conn_db(time=f"{placing_date}, {timeplace}, {timeplace_end}")

            if timeplace is not None:
                time_of_entry = timeplace
                date_of_entry = placing_date
                break

        db2 = Database(self.database_dir)
        db2.connect()

        query_2 = f"""  INSERT INTO user_tasks (date, task, workflow, task_begin, task_end, order_name, deprecated) 
                        VALUES ('{date_of_entry}', '{self.task}', '{self.workflow}', '{time_of_entry}', 
                        '{time_of_entry + int_task_time}', '{self.order}', 0)"""

        db2.execute_query(query_2)
        db2.close()

        table_name_conn = f'wf_{self.workflow}_ordr_{self.order}'

        db3 = Database('databases/db_wf_usr_conn.db')
        db3.connect()

        user_time = f'{date_of_entry}, {time_of_entry}, {time_of_entry + int_task_time}'

        query_3 = f"""  UPDATE '{table_name_conn}'
                        SET user_time = '{user_time}',
                            user_name = '{self.user_name}'
                        WHERE step_name = '{self.task}';
                    """
        db3.execute_query(query_3)
        db3.close()

        return int(time_of_entry), int(time_of_entry+int_task_time), date_of_entry, "string"

    def get_task_length(self, wf: str):
        db = Database("databases/db_workflows.db")
        db.connect()

        query = f"""SELECT est_time FROM {wf} WHERE name = '{self.task}'"""
        task_time = db.fetch_data(query)
        db.close()
        return task_time[0]

    @staticmethod
    def order_current_steps(all_non_deprecated_user_tasks: list) -> list:
        """
        [('27.03.2024',..., 150,...), ('27.03.2024',..., 480,...), ('27.03.2024',..., 300,...),...]
        gets sorted by date and then fourth column into
        [('27.03.2024',..., 150,...), ('27.03.2024',..., 300,...), ('27.03.2024',..., 480,...),...]
        """
        if len(all_non_deprecated_user_tasks) == 1:
            return [all_non_deprecated_user_tasks]

        else:
            sorted_tasks = sorted(all_non_deprecated_user_tasks)
            grouped_tasks = {}
            for task in sorted_tasks:
                key = task[0]
                if key not in grouped_tasks:
                    grouped_tasks[key] = []
                grouped_tasks[key].append(task)
            return_list = [sorted(group, key=lambda x: x[3]) for group in grouped_tasks.values()]

            return return_list

    def find_next_timeslot_if_tables_empty_and_put_task_there(self):
        """
        Now there is not a table of timeslots, that are not deprecated:
        The user-task will be given the next slot.
        """
        weeks, this_week, next_week, today, next_monday, workday = self.get_relevant_dates()

        if workday > 4:  # case: It's saturday or sunday
            """Case, we have saturday or Sunday => day > 4"""

            task_time_in_minutes = self.calculate_time_in_minutes(self.task_time)

            end_time = 480 + task_time_in_minutes

            self.make_entry_user_task(date=next_monday, time_begin=480, time_end=end_time)
            self.update_wf_usr_conn_db(time=f"{next_monday}, 480, {end_time}")
            return next_monday, 480, end_time, f"{next_monday}, 480, {end_time}"

        elif workday <= 4:

            task_time_in_mins = self.workhours_manager.time_str_into_int_minutes(self.task_time)  # because of elif

            self.time_now_in_hours_mins = datetime.datetime.now().strftime("%H:%M")
            now_in_int = self.workhours_manager.time_str_into_int_minutes(self.time_now_in_hours_mins)

            # Case: It is 7 o'Clock in the morning and the task_time does not take 4 hours (which by default it cant be)
            if now_in_int < 480:
                self.make_entry_user_task(date=today, time_begin=480, time_end=480+task_time_in_mins)
                self.update_wf_usr_conn_db(time=f"{today}, 480, {480+task_time_in_mins}")
                return today, 480, 480+task_time_in_mins, f"{today}, 480, {480+task_time_in_mins}"

            # Case: It is after (or just) 8 o'Clock in the morning
            else:

                # Case: It is between 8 o'Clock and 12 o'Clock in the morning
                if 480 <= now_in_int <= 720:

                    # Case: The task can still be done before 12 o'Clock
                    if now_in_int + task_time_in_mins <= 720:

                        self.make_entry_user_task(date=today, time_begin=now_in_int,
                                                  time_end=now_in_int+task_time_in_mins)
                        self.update_wf_usr_conn_db(time=f"{today}, {now_in_int}, {now_in_int+task_time_in_mins}")
                        return (today, now_in_int,
                                now_in_int+task_time_in_mins,
                                f"{now_in_int}, {now_in_int}, {now_in_int+task_time_in_mins}")

                    # Case: The task cannot be done before 12 o'Clock
                    if now_in_int + task_time_in_mins > 720:
                        self.make_entry_user_task(date=today, time_begin=780, time_end=780+task_time_in_mins)
                        self.update_wf_usr_conn_db(time=f"{today}, {780}, {780+task_time_in_mins}")
                        return today, 780, 780 + task_time_in_mins, f"{today}, 780, {780 + task_time_in_mins}"

                # Case: It is between 12 o'Clock and 13 o'Clock (fuck the brits "oNe O'cLoCk")
                elif 720 < now_in_int < 780:

                    # Case: The task can be done at any case right after the break:
                    self.make_entry_user_task(date=today, time_begin=780, time_end=780+task_time_in_mins)
                    self.update_wf_usr_conn_db(time=f"{today}, {780}, {780 + task_time_in_mins}")
                    return today, 780, 780 + task_time_in_mins, f"{today}, 780, {780 + task_time_in_mins}"

                # Case: It is between 13 o'Clock and 17 o'Clock
                elif 780 <= now_in_int <= 1020:

                    # Case: The task still fits into today's time
                    if now_in_int + task_time_in_mins <= 1020:
                        self.make_entry_user_task(date=today, time_begin=now_in_int,
                                                  time_end=now_in_int+task_time_in_mins)
                        self.update_wf_usr_conn_db(time=f"{today}, {now_in_int}, {now_in_int+task_time_in_mins}")
                        return (today, now_in_int, now_in_int + task_time_in_mins,
                                f"{today}, now_in_int, {now_in_int + task_time_in_mins}")

                    # Case: The task does not fit into today's time:
                    elif now_in_int + task_time_in_mins > 1020:

                        if workday < 4:  # Case: It's not friday => Tomorrow is allowed

                            tomorrow = self.workhours_manager.current_week[workday + 1]  # we need tomorrow here

                            self.make_entry_user_task(date=tomorrow, time_begin=480,
                                                      time_end=480+task_time_in_mins)
                            self.update_wf_usr_conn_db(time=f"{tomorrow}, {480}, {480+task_time_in_mins}")
                            return tomorrow, 480, 480+task_time_in_mins, f"{tomorrow}, {480}, {480+task_time_in_mins}"

                        elif workday == 4:  # Case: It is friday => Next monday needed

                            self.make_entry_user_task(date=next_monday, time_begin=480,
                                                      time_end=480+task_time_in_mins)
                            self.update_wf_usr_conn_db(time=f"{next_monday}, {480}, {480+task_time_in_mins}")
                            return next_monday, 480, 480+task_time_in_mins, f"{next_monday}, {480}, {480+task_time_in_mins}"

                # Case it is after 17 o'clock
                elif now_in_int > 1020:

                    if workday < 4:  # Case: It's not friday => Tomorrow is allowed

                        tomorrow = self.workhours_manager.current_week[workday + 1]  # we need tomorrow here

                        self.make_entry_user_task(date=tomorrow, time_begin=480,
                                                  time_end=480 + task_time_in_mins)
                        self.update_wf_usr_conn_db(time=f"{tomorrow}, {480}, {480 + task_time_in_mins}")
                        return tomorrow, 480, 480+task_time_in_mins, f"{tomorrow}, {480}, {480 + task_time_in_mins}"

                    elif workday == 4:  # Case: It is friday => Next monday needed

                        self.make_entry_user_task(date=next_monday, time_begin=480,
                                                  time_end=480 + task_time_in_mins)
                        self.update_wf_usr_conn_db(time=f"{next_monday}, {480}, {480 + task_time_in_mins}")
                        return next_monday, 480, 480+task_time_in_mins, f"{next_monday}, {480}, {480 + task_time_in_mins}"

    def update_wf_usr_conn_db(self, time):
        db = Database("databases/db_wf_usr_conn.db")
        db.connect()
        table_name = f"wf_{self.workflow}_ordr_{self.order}"
        query = f"UPDATE {table_name} SET user_name = ?, user_time = ? WHERE deprecated = 0 and step_name = ?"
        params = (self.user_name, time, self.task)
        db.execute_query(query=query, params=params)
        db.close()

    @staticmethod
    def calculate_time_in_minutes(time):
        elements = time.split(":")
        hours = int(elements[0])
        minutes = int(elements[1])
        task_time_in_minutes = 60 * hours + minutes
        return task_time_in_minutes

    def make_entry_user_task(self, date: str, time_begin: int, time_end: int):
        db = Database(self.database_dir)
        db.connect()

        query = """INSERT INTO user_tasks (date, task, workflow, task_begin, task_end, order_name, deprecated)
                   VALUES (?, ?, ?, ?, ?, ?, ?)"""

        values = (date, self.task, self.workflow, time_begin, time_end, self.order,  0)

        db.execute_query(query, values)

        db.close()

    def pull_non_deprecated_user_tasks(self) -> list:
        """ Sub-function from self.find_all_user_tasks_from_now_on()"""
        db = Database(self.database_dir)
        db.connect()

        query = "SELECT * FROM {} WHERE deprecated = 0".format("user_tasks")

        user_tasks_from_now_on = db.fetch_data(query)
        db.close()

        return user_tasks_from_now_on

    def pull_task_time_from_workflow(self):
        """ Need the task_time -> pull it here """

        db = Database("databases/db_workflows.db")
        db.connect()

        query = "SELECT * FROM {}".format(self.workflow)

        workflow_data = db.fetch_data(query)
        db.close()

        for element in workflow_data:
            if element[1] == self.task:
                task_time = element[2]
                return task_time



