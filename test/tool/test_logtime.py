import io
import pytest
import pandas
import logging
from pathlib import Path
from WeTest.tool import logtime
from WeTest.util import provider
from pytest import TempPathFactory



@pytest.fixture(scope="module")
def testdata(tmp_path_factory: TempPathFactory):
    
    log = """
    1639362912.431	127.0.0.1	expires=Wed, 13-Dec-23 02:35:12 GMT; domain=127.0.0.1; path=/;
    1639362912.520	127.0.0.1	expires=Wed, 13-Dec-23 02:35:12 GMT; domain=127.0.0.1; path=/;
    1639362912.580	127.0.0.1	expires=Wed, 13-Dec-23 02:35:12 GMT; domain=127.0.0.1; path=/;
    """

    path = tmp_path_factory.mktemp("log") / "testlog.csv"
    df = pandas.read_csv(io.StringIO(log))
    path = provider.df_to_csv(df, path)
    
    return path


def test_gettimestamp():

    log1 = "1571731092.458	127.0.0.1"
    log2 = "1571731093	127.0.0.1"
    log3 = "15717310921571731092 1571731094 1571731093	127.0.0.1"

    print(logtime.get_timestamp(log1))
    print(logtime.get_timestamp(log2))
    print(logtime.get_timestamp(log3))

    assert logtime.get_timestamp(log1) == "1571731092"
    assert logtime.get_timestamp(log2) == "1571731093"
    assert logtime.get_timestamp(log3) == "1571731094"


def test_replace_timestamp():

    orilog = "1571731092.458	127.0.0.1"
    newlog = "1571740286.458	127.0.0.1"

    assert logtime.replace_timestamp(orilog, "2019-10-22 18:31:26") == newlog


def test_get_minutes_by_hour_span():

    result = logtime.get_minutes_by_hour_span("2019-10-24", start_hour=2, hour_span=2)
    
    assert result[0] == "2019-10-24 02:01:01"
    assert result[-1] == "2019-10-24 03:59:59"


def test_update_to_same_seconds(testdata, tmp_path: Path):

    newlog = str(tmp_path / "testlog_new_samesec.csv")
    times = ["2019-10-07 10:31:26", "2019-10-07 11:31:26"]
    
    logtime.update_to_same_seconds(testdata, newlog, times)

    logging.info(f"Export To {newlog} Success!")


def test_update_to_diffrent_seconds(testdata, tmp_path: Path):

    newlog = str(tmp_path / "testlog_new_diffsec.csv")
    times = ["2019-10-07/10", "2019-10-07/11"]
    
    logtime.update_to_diffrent_seconds(testdata, newlog, times)

    logging.info(f"Export To {newlog} Success!")
