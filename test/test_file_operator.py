from os_functions. file_operator import read_from, convert_file_dict_to_dict_metadata
import pytest


def test_read_from_flat_dir(tmp_path):
    (tmp_path / "note.md").write_text("# hello")

    result = read_from(str(tmp_path))
    if result == None:
        raise Exception("result return None")

    assert len(result) == 1
    assert result[0]["from_file"] == "note.md"
    assert result[0]["content"] == "# hello"


def test_read_from_nested_dir(tmp_path):
    (tmp_path / "note.md").write_text("# hello")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "note2.md").write_text("# nested")

    result = read_from(str(tmp_path))
    if result == None:
        raise Exception("result return None")

    assert len(result) == 2


def test_read_from_missing_dir():
    result = read_from("this_dir_does_not_exist")
    with py


def test_read_from_empty_subfolder_skipped(tmp_path):
    empty_sub = tmp_path / "empty"
    empty_sub.mkdir()

    result = read_from(str(tmp_path))

    assert result == []