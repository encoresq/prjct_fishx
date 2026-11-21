from pathlib import Path


def resource_path(filename):
    return str(Path(__file__).resolve().parent / "ui" / filename)


def base_path(filename):
    return str(Path(__file__).resolve().parent / "db" / filename)

