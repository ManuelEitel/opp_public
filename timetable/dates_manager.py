from datetime import datetime, timedelta


class TimetableDateManager(object):

    def __init__(self):
        """
        self.current_week_index: Calendar Week
        self.current_week: Monday to Sunday of week
        self.weeks: Combined self.current_week_index with self.current_week
        self.current_date: Current date as string
        self.current_day: Current day as string
        """

        self.current_date = None
        self.current_year = None
        self.current_month = None
        self.current_day = None
        self.get_current_date()

        self.weeks = self.get_week_dates()

        self.current_week_index = None
        self.current_week = None
        self.get_current_week_index()

    def get_current_week_index(self):
        if self.weeks:
            self.current_date = self.current_date.strftime("%d.%m.%Y")
            for index, current_week in self.weeks:

                for date in current_week:
                    if date == self.current_date:
                        self.current_week_index = index
                        self.current_week = current_week
                    else:
                        continue
                    break

    def get_current_date(self):
        self.current_date = datetime.now()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        self.current_day = self.current_date.day

    def get_week_dates(self) -> list:
        """
        returns a list that looks like this
        week_dates = \n
        [(1,['01.01.2024', '02.01.2024', '03.01.2024', '04.01.2024','05.01.2024', '06.01.2024', '07.01.2024']), \n
         (2, ['08.01.2024', '09.01.2024', '10.01.2024', '11.01.2024','12.01.2024', '13.01.2024', '14.01.2024']), \n
         (3, [...])]
        """
        if self.current_year:
            week_dates = []
            current_date = datetime(self.current_year, 1, 1)  # Start from January 1st of the given year
            one_day = timedelta(days=1)

            # Loop through each day of the year
            while current_date.year == self.current_year:
                if current_date.weekday() == 0:  # Monday
                    week_number = current_date.isocalendar()[1]  # Get ISO week number
                    week_dates.append((week_number, []))
                    week_dates[-1][1].append(current_date.strftime("%d.%m.%Y"))
                    # Add dates for Tuesday to Sunday
                    for i in range(1, 7):
                        week_dates[-1][1].append((current_date + timedelta(days=i)).strftime("%d.%m.%Y"))
                    current_date += timedelta(days=6)  # Skip to next Monday
                else:
                    current_date += one_day
            return week_dates

