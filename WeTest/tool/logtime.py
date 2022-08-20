import re
import logging
from ..util import date


def get_timestamp(content: str) -> str:

    pattern = r"\b\d{10}\b"
    timestamp = re.findall(pattern, content)[0]
    return timestamp


def replace_timestamp(content: str, datetime: str) -> str:

    timestamp_ori = get_timestamp(content)
    timestamp_new = date.time_to_unixtime(datetime)
    return content.replace(str(timestamp_ori), str(timestamp_new))


def get_minutes_by_hour_span(datetime: str, start_hour: int = 1, hour_span: int = 1) -> list:

    hour = start_hour
    end_hour = start_hour + hour_span
    minute = 1
    second = 1

    result = []
    while second <= 60 and hour < end_hour and minute < 60:
        time = "{} {:0>2d}:{:0>2d}:{:0>2d}".format(datetime, hour, minute, second)
        result.append(time)
        second = second + 1
        if second == 60:
            minute = minute + 1
            second = 1
            if minute == 60:
                hour = hour + 1
                minute = 1
                second = 1

    return result


def update_to_same_seconds(source: str, target: str, times: list) -> str:

    with open(source, "r") as r:
        logs = r.readlines()

        content = []
        for time in times:
            for log in logs:
                content.append(replace_timestamp(log, time))

    with open(target, "w") as f:
        f.writelines(content)
        
    logging.info(f"Save file to: {target}")
    
    return target


def update_to_diffrent_seconds(source: str, target: str, times: list) -> str:

    with open(source, "r") as r:
        logs = r.readlines()

        content = []
        for time in times:
            time = time.split("/")
            day = time[0]
            hour = int(time[1])
            result = get_minutes_by_hour_span(day, start_hour=hour, hour_span=1)

            for log in logs:
                content.append(replace_timestamp(log, result.pop(0)))

    with open(target, "w") as f:
        f.writelines(content)

    logging.info(f"Save file to: {target}")
    
    return target