import shutil
import logging
from pathlib import Path


def get_parent(path: str) -> str:
    return str(Path(path).parent)


def get_filename(path: str) -> str:
    return Path(path).name


def get_filename_without_suffix(path: str) -> str:
    return Path(path).name.split(".")[0]


def get_suffix(path: str) -> str:
    return "".join(Path(path).suffixes)


def path_to_uri(path: str) -> str:
    return Path(path).as_uri()


def is_absolute(path: str) -> bool:
    return Path(path).is_absolute()


def is_exists(path: str) -> bool:
    return Path(path).exists()


def is_dir(path: str) -> bool:
    return Path(path).is_dir()


def is_file(path: str) -> bool:
    return Path(path).is_file()


def list_dir(path: str) -> list:
    return [str(file) for file in Path(path).iterdir()]


def resolve_path(path: str, strict=False) -> str:
    return Path(path).resolve(strict=strict)


def join_path(paths: list) -> str:
    return str(Path(paths[0]).joinpath(*paths[1:]))


def reuse_path(source: str, name_with_suffix: str) -> str:
    return str(Path(source).with_name(name_with_suffix))


def replace_name(source: str, name_without_suffix: str) -> str:
    parent = get_parent(source)
    suffix = get_suffix(source)
    return "{}{}".format(join_path([parent, name_without_suffix]), suffix)


def filter_file(path: str, pattern: str) -> list:
    return sorted([str(file) for file in Path(path).glob(pattern)])


def recursive_query_file(path: str, pattern: str) -> list:

    result = []

    def recursive(path: str, pattern: str):
        nonlocal result

        path = Path(path)

        result += filter_file(path, pattern)

        sub_folders = [folder for folder in path.iterdir() if folder.is_dir()]

        if sub_folders:
            for folder in sub_folders:
                recursive(folder, pattern)
        else:
            return result

    recursive(path, pattern)

    return result


def match_file(path: str, pattern: str) -> bool:
    return Path(path).match(pattern)


def write_text(data: str, path: str) -> str:
    path = Path(path)
    mkdir(str(path.parent))

    path.write_text(data)
    logging.info(f"Save data to: {str(path)}")

    return path


def write_bytes(data: bytes, path: str) -> str:
    path = Path(path)
    mkdir(str(path.parent))

    path.write_bytes(data)
    logging.info(f"Save data to: {str(path)}")

    return path


def read_text(path: str) -> str:
    return Path(path).read_text()


def read_bytes(path: str) -> bytes:
    return Path(path).read_bytes()


def get_cwd() -> str:
    return str(Path.cwd())


def get_home() -> str:
    return str(Path.home())


def mkdir(path: str, mode: int = 0o777, parents: bool = True, exist_ok: bool = False) -> str:
    path = Path(path)
    if not path.exists():
        Path(path).mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
    return path.resolve()


def rmdir(path: str, ignore_errors=False):
    shutil.rmtree(path, ignore_errors=ignore_errors)
