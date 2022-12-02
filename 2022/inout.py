import io
from pathlib import Path


def read(path: Path, method: str = "raw", mode: str = "r") -> str | list | set:
    """Read data from file_path and return lines as raw string or list of strings."""
    if not path.exists():
        raise FileNotFoundError(f"File {path.resolve()} not found.")
    with open(path, mode) as file:
        match method:
            case "raw":
                content = _raw(file)
            case "lines":
                content = _lines(file)
            case "set":
                content = set(_lines(file))
            case _:
                raise NotImplementedError(f"Method {method} not implemented.")
    return content

def _raw(file: io.TextIOWrapper) -> str:
    """Return raw string."""
    return file.read()

def _lines(file: io.TextIOWrapper) -> list:
    """Return lines as a list."""
    return [entry.replace("\n", "") for entry in file.readlines()]
