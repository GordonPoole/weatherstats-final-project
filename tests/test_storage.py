import json
from pathlib import Path
from weatherstats.storage import JSONStorage


def test_save_obj_creates_file_and_returns_path(tmp_path):
    storage = JSONStorage(indent=4)

    data = {"a": 1, "b": 2}
    file_path = tmp_path / "subdir" / "output.json"

    returned_path = storage.save_obj(data, file_path)
    assert returned_path == file_path
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded == data


def test_save_obj_creates_directories(tmp_path):
    storage = JSONStorage()

    nested_path = tmp_path / "a" / "b" / "c" / "file.json"
    storage.save_obj({"x": 10}, nested_path)

    assert nested_path.exists()


def test_indent_is_respected(tmp_path):
    storage = JSONStorage(indent=4)

    file_path = tmp_path / "file.json"
    storage.save_obj({"a": 1}, file_path)

    content = file_path.read_text()
    assert "    " in content