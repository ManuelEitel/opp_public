import datetime
from databases.datatase_handler import Database
from timetable.dates_manager import TimetableDateManager


class WorkHoursManager(object):

    def __init__(self, user: str, task_time: str):
        """
        In versions more that V1.0 the User shifts need to be adjustable, to not just be 8-17.
        This setup makes that later change easier. In V1.0 it's enough to have every User 8-17 shifts.
        The corresponding function for the shifts is self._set_workhours().

        # ToDo: task_time is not used here. Get rid of it.
        """

        self.user = user
        self.task_time = task_time
        self._set_workhours()
        self.timetable_dates_manager = None

        self.current_date = None
        self.current_week = None
        self.sorted_dates = None
        self.current_week_index = None

    def get_current_date_and_week(self):
        """ Rename dates stuff for read ability """

        self.timetable_dates_manager = TimetableDateManager()
        self.current_date = self.timetable_dates_manager.current_date
        self.current_week = self.timetable_dates_manager.current_week
        self.current_week_index = self.timetable_dates_manager.current_week_index

    def _set_workhours(self):
        """ This function eventually needs to be adjusted, so that the user themselves can adjust his shifts. """

        self.morning_start = 480  # "08:00"
        self.morning_end = 720  # "12:00"

        self.afternoon_start = 780  # "13:00"
        self.afternoon_end = 1020  # "17:00"

        self.shift = [self.morning_start, self.morning_end, self.afternoon_start, self.afternoon_end]

    @staticmethod
    def time_str_into_int_minutes(task_time: str) -> int:
        """ hours: "08:15" -> mins = 60 * hours + minutes """

        elements = task_time.split(":")
        task_time = int(elements[0])
        minutes = int(elements[1])

        time_in_minutes = 60 * task_time + minutes
        return time_in_minutes

    @staticmethod
    def turn_int_mins_into_str_times(task_time: int) -> str:

        hours = task_time // 60
        minutes = task_time % 60
        if minutes == 0:
            minutes = "00"
        task_end_time = f'{hours}:{minutes}'
        return task_end_time




