import arrow
from .. import const
from datetime import timedelta


def get_unixtime(length: int = 10) -> int:

    if length == 10:
        return int(arrow.now(tz=const.TZINFO).timestamp())

    elif length == 13:
        return int(arrow.now(tz=const.TZINFO).timestamp() * 1000)


def get_time(fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:

    return arrow.now(tz=const.TZINFO).format(fmt)


def get_timedelta(start: str, end: str) -> timedelta:

    return arrow.get(end) - arrow.get(start)


def unixtime_to_time(unixtime: int, fmt: str = "YYYY-MM-DD HH:mm:ss") -> str:

    return arrow.get(unixtime, tzinfo=const.TZINFO).format(fmt)


def time_to_unixtime(datetime: str) -> int:

    return int(arrow.get(datetime, tzinfo=const.TZINFO).timestamp())


def get_current_hour() -> int:

    return arrow.now(tz=const.TZINFO).hour


def format_date(datetime: str, fmt: str = "YYYY-MM-DD") -> str:

    return arrow.get(datetime, tzinfo=const.TZINFO).format(fmt)


def get_day_delta(start_date: str, end_date: str) -> int:

    return (arrow.get(start_date, tzinfo=const.TZINFO) - arrow.get(end_date, tzinfo=const.TZINFO)).days


def get_today(fmt: str = "YYYY-MM-DD") -> str:

    return arrow.now(tz=const.TZINFO).format(fmt)


def get_yesterday(fmt: str = "YYYY-MM-DD") -> str:

    return arrow.now(tz=const.TZINFO).shift(days=-1).format(fmt)


def get_monday(datetime: str = get_today(), fmt: str = "YYYY-MM-DD") -> str:

    return arrow.get(datetime, tzinfo=const.TZINFO).shift(weekday=0).shift(days=-7).format(fmt)


def get_lastmonday(fmt: str = "YYYY-MM-DD") -> str:

    return arrow.now(tz=const.TZINFO).shift(weekday=0).shift(days=-7).shift(weeks=-1).format(fmt)


def get_lastmonth_firstday(fmt: str = "YYYY-MM-DD") -> str:

    return arrow.now(tz=const.TZINFO).shift(days=1 - arrow.now(tz=const.TZINFO).day, months=-1).format(fmt)


def get_day_by_range(start_date: str, end_date: str, fmt: str = "YYYY-MM-DD") -> list:

    start_date = arrow.get(start_date, tzinfo=const.TZINFO)
    end_date = arrow.get(end_date, tzinfo=const.TZINFO)

    days = []
    while start_date <= end_date:
        days.append(start_date.format(fmt))
        start_date = start_date.shift(days=1)

    return days


def get_timestamp_by_range(start_date: str, end_date: str, frame: str = "second") -> list:

    start_date = arrow.get(start_date, tzinfo=const.TZINFO)
    end_date = arrow.get(end_date, tzinfo=const.TZINFO)

    timestamps = [int(timestamp.timestamp()) for timestamp in arrow.Arrow.range(frame, start_date, end_date, tz=const.TZINFO)]

    return timestamps


def get_monday_by_range(start_date: str, end_date: str, fmt="YYYY-MM-DD") -> list:

    daterange = get_day_by_range(start_date, end_date, fmt="YYYY-MM-DD")

    mondays = []
    for date in daterange:
        date = arrow.get(date, tzinfo=const.TZINFO)
        if date.weekday() == 0:
            mondays.append(date.format(fmt))

    return mondays


def get_date_by_timedelta(datetime: str, fmt: str = "YYYY-MM-DD", **timedelta) -> str:

    return arrow.get(datetime, tzinfo=const.TZINFO).shift(**timedelta).format(fmt)


def get_day_by_timedelta(start_date: str, fmt: str = "YYYY-MM-DD", **timedelta) -> list:

    end_date = get_date_by_timedelta(start_date, fmt, **timedelta)
    days = get_day_by_range(start_date, end_date, fmt)

    return days
