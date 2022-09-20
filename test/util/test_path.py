import logging
from WeTest.util import path


def test_mkdir():
    report = path.mkdir("tmp")
    assert path.is_exists(report)


def test_get_parent():
    assert path.get_parent("/a/b/c") == "/a/b"


def test_get_filename():
    assert path.get_filename("/a/b/c/d.txt") == "d.txt"
    assert path.get_filename("/a/b/c/d.tar.gz") == "d.tar.gz"


def test_get_filename_without_suffix():
    assert path.get_filename_without_suffix("/a/b/c/d.txt") == "d"
    assert path.get_filename_without_suffix("/a/b/c/d.tar.gz") == "d"


def test_get_suffix():
    assert path.get_suffix("/a/b/c/d.txt") == ".txt"
    assert path.get_suffix("/a/b/c/d.tar.gz") == ".tar.gz"


def test_path_to_uri():
    assert path.path_to_uri("/a/b/c/d.txt") == "file:///a/b/c/d.txt"


def test_is_absolute():
    assert path.is_absolute("/a/b/c/d.txt") == True
    assert path.is_absolute("a/b/c/d.txt") == False


def test_is_exists():
    assert path.is_exists("test/util/test_path.py") == True
    assert path.is_exists("/a/b/c/d.txt") == False


def test_is_dir():
    assert path.is_dir("test/util") == True
    assert path.is_dir("/a/b/c/d.txt") == False


def test_is_file():
    assert path.is_file("test/util") == False
    assert path.is_file("test/util/test_path.py") == True


def test_list_dir():
    logging.info(path.list_dir("test"))


def test_resolve_path():
    logging.info(path.resolve_path("test"))


def test_join_path():
    assert path.join_path(["a", "b", "c", "d"]) == "a/b/c/d"


def test_reuse_path():
    assert path.reuse_path("/a/b/c/d.txt", "d.zip") == "/a/b/c/d.zip"


def test_replace_name():
    assert path.replace_name("/a/b/c/d.txt", "e") == "/a/b/c/e.txt"


def test_filter_file():
    logging.info(path.filter_file("test", "*.py"))


def test_recursive_query_file():
    logging.info(path.recursive_query_file("test", "*.py"))
    logging.info(path.recursive_query_file("test", "test_path.py"))

    assert path.recursive_query_file("test", "test_path.py") == ["test/util/test_path.py"]


def test_match_file():
    assert path.match_file("/a/b/c/d.txt", "*.txt") == True
    assert path.match_file("/a/b/c/d.txt", "d.txt") == True
    assert path.match_file("/a/b/c/d.txt", "c/*.txt") == True
    assert path.match_file("/a/b/c/d.txt", "*/*.txt") == True


def test_rw_text(tmp_path):
    file = tmp_path / "write_text.txt"
    file = path.write_text("hello world!", str(file))
    assert path.is_exists(file)
    assert path.read_text(file) == "hello world!"


def test_rw_bytes(tmp_path):
    file = tmp_path / "write_bytes"
    file = path.write_bytes(b"hello world!", str(file))
    assert path.is_exists(file)
    assert path.read_bytes(file) == b"hello world!"


def test_get_cwd():
    logging.info(path.get_cwd())


def test_get_home():
    logging.info(path.get_home())


def test_rmdir():
    assert path.is_exists("tmp") == True
    path.rmdir("tmp")
    assert path.is_exists("tmp") == False
