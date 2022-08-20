from pathlib import Path
from WeTest.util import config


def test_yaml(tmp_path: Path):

    # Save as yaml file
    data = {"env": ["test", "dev", "prd"]}
    path = str(tmp_path / "test.yaml")
    path = config.to_yaml(data, path)
    assert Path(path).exists()

    # Read yaml file
    content = config.read_yaml(path)
    assert content["env"] == ["test", "dev", "prd"]

    content = config.read_yaml(path, type="file")
    assert content["env"] == ["test", "dev", "prd"]

    # Ready yaml string
    text = "env: [test, dev, prd]"
    content = config.read_yaml(text, type="string")
    assert content["env"] == ["test", "dev", "prd"]


def test_ini(tmp_path: Path):

    # Save as ini file
    data = {"env": {"test": "test", "dev": "dev", "prd": "prd"}}
    path = str(tmp_path / "test.ini")
    path = config.to_ini(data, path)
    assert Path(path).exists()

    # Read ini file
    content = config.read_ini(path)
    assert content["env"]["test"] == "test"


def test_json(tmp_path: Path):

    # Save as json file
    data = {"env": {"test": "test", "dev": "dev", "prd": "prd"}}
    path = str(tmp_path / "test.json")
    path = config.to_json(data, path)
    assert Path(path).exists()

    # Read json file
    content = config.read_json(path)
    assert content["env"]["test"] == "test"
