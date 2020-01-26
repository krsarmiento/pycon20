from datetime import datetime
from geofencing.schedule import Schedule


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def test_weekday_offset_monday():
    current_datetime = datetime.strptime('2020-01-06 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 10000


def test_weekday_offset_tuesday():
    current_datetime = datetime.strptime('2020-01-07 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 20000


def test_weekday_offset_wednesday():
    current_datetime = datetime.strptime('2020-01-08 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 30000


def test_weekday_offset_thursday():
    current_datetime = datetime.strptime('2020-01-09 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 40000


def test_weekday_offset_friday():
    current_datetime = datetime.strptime('2020-01-10 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 50000


def test_weekday_offset_saturday():
    current_datetime = datetime.strptime('2020-01-11 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 60000


def test_weekday_offset_sunday():
    current_datetime = datetime.strptime('2020-01-12 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_weekday_offset() == 70000


def test_get_minutes_passed_first_minute():
    current_datetime = datetime.strptime('2020-01-01 00:00:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_minutes_passed() == 0


def test_get_minutes_passed_six_forty_am():
    current_datetime = datetime.strptime('2020-01-01 06:40:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_minutes_passed() == 400


def test_get_minutes_passed_seven_fifteen_pm():
    current_datetime = datetime.strptime('2020-01-01 19:15:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_minutes_passed() == 1155


def test_get_minutes_passed_last_minute():
    current_datetime = datetime.strptime('2020-01-01 23:59:59', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_minutes_passed() == 1439


def test_get_numeric_representation_tuesday_at_eleven_fifty_two_am():
    current_datetime = datetime.strptime('2020-01-09 11:52:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_numeric_representation() == 40712


def test_get_numeric_representation_tuesday_at_nine_thirty_three_pm():
    current_datetime = datetime.strptime('2020-01-07 21:33:00', DATETIME_FORMAT)
    schedule = Schedule(current_datetime)
    assert schedule.get_numeric_representation() == 21293
