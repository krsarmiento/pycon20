"""
Schedule module

We use the number of minutes in a day (1440) plus an offset to know which day we're using.

Monday: +10,000
Tuesday: +20,000
Wednesday: +30,000
Thursday: +40,000
Friday: +50,000
Saturday: +60,000
Sunday: +70,000

Examples:
    Thursday at 11:52 am -> 40,712
    Tuesday at 9:33 pm -> 21,293
"""


WEEK_MAPPING = {
    '1': 10000,
    '2': 20000,
    '3': 30000,
    '4': 40000,
    '5': 50000,
    '6': 60000,
    '0': 70000,
}


class Schedule:

    def __init__(self, datetime):
        self.datetime = datetime

    def get_weekday_offset(self):
        raw_weekday = self.datetime.strftime('%w')
        return WEEK_MAPPING[raw_weekday]

    def get_minutes_passed(self):
        raw_hours = self.datetime.strftime('%H')
        raw_minutes = self.datetime.strftime('%M')
        return int(raw_hours) * 60 + int(raw_minutes)

    def get_numeric_representation(self):
        return self.get_weekday_offset() + self.get_minutes_passed()

