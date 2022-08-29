import logging
from WeTest.util import date


def test_get_unixtime():

    logging.info(date.get_unixtime(10))
    logging.info(date.get_unixtime(13))


def test_get_time():

    logging.info(date.get_time())
    logging.info(date.get_time("YYYY/MM/DD HH_mm_ss"))
    logging.info(date.get_time("YYYY-MM-DD HH:mm:ss"))


def test_get_timedelta():

    assert (date.get_timedelta("2019-10-22 18:31:26", "2019-10-22 18:32:26")).days == 0
    assert (date.get_timedelta("2019-10-22 18:31:26", "2019-10-22 18:32:26")).seconds == 60


def test_unixtime_to_time():

    assert date.unixtime_to_time(1571740286) == "2019-10-22 18:31:26"
    assert date.unixtime_to_time(1571740286, "YYYY-MM-DD HH:mm:ss") == "2019-10-22 18:31:26"
    assert date.unixtime_to_time(1571740286, "YYYY/MM/DD HH:mm:ss") == "2019/10/22 18:31:26"


def test_time_to_unixtime():

    assert date.time_to_unixtime("2019-10-22 18:31:26") == 1571740286
    assert date.time_to_unixtime("2019/10/22 18:31:26") == 1571740286


def test_format_date():

    logging.info(date.format_date("2020-01-03"))
    logging.info(date.format_date("2020-01-03", "YYYY-MM-DD"))
    logging.info(date.format_date("2020/01/03", "YYYY-MM-DD"))
    logging.info(date.format_date("2020/01/03", "YYYYMMDD"))
    logging.info(date.format_date("2021-03-26T10:57:01.000+0800", "YYYY-MM-DD HH:mm:ss ZZ"))
    logging.info(date.format_date("2021-03-26T10:57:01.000+0800", "YYYY-MM-DD HH:mm:ss"))

    assert date.format_date("2020-01-03") > date.format_date("2020-01-02")


def test_get_day_delta():

    assert date.get_day_delta("2020-10-15", "2020-10-10") == 5
    assert date.get_day_delta("20201015", "20201010") == 5
    assert date.get_day_delta("2020/10/15", "2020/10/10") == 5

    logging.info(date.get_current_hour())

    logging.info(date.get_today())

    logging.info(date.get_yesterday())
    logging.info(date.get_yesterday(fmt="YYYY-MM-DD"))
    logging.info(date.get_yesterday(fmt="YYYYMMDD"))

    logging.info(date.get_monday())
    logging.info(date.get_monday(fmt="YYYY-MM-DD"))
    logging.info(date.get_monday(fmt="YYYYMMDD"))
    logging.info(date.get_monday(datetime="20210709", fmt="YYYYMMDD")) == "20210629"

    logging.info(date.get_lastmonth_firstday())
    logging.info(date.get_lastmonth_firstday(fmt="YYYY-MM-DD"))
    logging.info(date.get_lastmonth_firstday(fmt="YYYYMMDD"))


def test_get_day_by_range():

    start_date = "2020-07-27"
    end_date = "2020-08-02"
    daterange = date.get_day_by_range(start_date, end_date)

    assert daterange == [
        "2020-07-27",
        "2020-07-28",
        "2020-07-29",
        "2020-07-30",
        "2020-07-31",
        "2020-08-01",
        "2020-08-02",
    ]


def test_get_timestamp_by_range():

    start_date = "2020-07-28 23:59:00"
    end_date = "2020-07-28 23:59:59"

    daterange = date.get_timestamp_by_range(start_date, end_date)
    logging.info(daterange)

    daterange = date.get_timestamp_by_range(start_date, end_date, frame="hour")
    logging.info(daterange)

    daterange = date.get_timestamp_by_range(start_date, end_date, frame="day")
    logging.info(daterange)


def test_get_monday_by_range():

    start_date = "2020-07-27"
    end_date = "2020-08-24"
    daterange = date.get_monday_by_range(start_date, end_date)

    assert daterange == ["2020-07-27", "2020-08-03", "2020-08-10", "2020-08-17", "2020-08-24"]


def test_get_date_by_timedelta():

    logging.info("Current Time: " + date.get_time())
    logging.info("30 Minutes Ago: " + date.get_date_by_timedelta(date.get_time(), minutes=-30, fmt="YYYY-MM-DD HH:mm:ss"))
    logging.info("Torrow: " + date.get_date_by_timedelta(date.get_time(), days=1))
    logging.info("Yesterday: " + date.get_date_by_timedelta(date.get_time(), days=-1))
    logging.info("1 Week Ago: " + date.get_date_by_timedelta(date.get_time(), weeks=-1))
    logging.info("1 Month Ago: " + date.get_date_by_timedelta(date.get_time(), months=-1))
    logging.info("1 Year Ago :" + date.get_date_by_timedelta(date.get_time(), years=-1))
    logging.info("1 Hour Ago: " + date.get_date_by_timedelta(date.get_time(), hours=-1))
    logging.info("1 Hour Ago For Specific Date: " + date.get_date_by_timedelta("2021-03-04 00:00:00", hours=-1))


def test_get_day_by_timedelta():

    logging.info(date.get_day_by_timedelta(date.get_monday(), days=5))
    logging.info(date.get_day_by_timedelta(date.get_monday(), fmt="YYYY/M/D", days=5))
