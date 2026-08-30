from os_functions. file_operator import read_from, convert_file_dict_to_dict_metadata
import pytest


def test_read_from_flat_dir(tmp_path):
    (tmp_path / "note.md").write_text("# hello")

    result = read_from(str(tmp_path))
    if result == None:
        raise Exception("result return None")

    assert len(result) == 1
    assert result[0]["from_file"] == str(tmp_path / "note.md")
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
    with pytest.raises(FileNotFoundError):
        read_from("not_exist_dir")


def test_read_from_empty_subfolder_skipped(tmp_path):
    empty_sub = tmp_path / "empty"
    empty_sub.mkdir()

    result = read_from(str(tmp_path))

    assert result == []








def test_convert_file_dict_to_dict_metadata():
    test_dict = [{
        "from_file": "test_file",
        "content": """
# Title 1
This belong to title 1
""",
    }]
    expected_result = [[{
        "from_file" : "test_file",
        "from_title": "# Title 1",
        'chunk_id': 1,
        "content": ["This belong to title 1"],
    }]]
    actual_result = convert_file_dict_to_dict_metadata(test_dict)
    assert expected_result == actual_result