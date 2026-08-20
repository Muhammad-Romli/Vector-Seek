from converter_functions.markdown_converter import markdown_to_dict_metadata
import pytest

def test_markdown_conventer_regular():
    
    actual_result = markdown_to_dict_metadata("Diary", """
# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it
""")

    expected_result = [{
        "from_file":  "Diary",
        "title": "# Dear diary",
        "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
    }]

    assert actual_result == expected_result
    

def test_markdown_conventer_multiple_titles():
    
    actual_result = markdown_to_dict_metadata("Diary", """
# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it

# REASON WHY I HATE ULCER

- Painful
- Attack me for no reason
- Painful
- Happen too often
""")

    expected_result = [{
        "from_file":  "Diary",
        "title": "# Dear diary",
        "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
    },
    {
        "from_file": "Diary",
        "title": "# REASON WHY I HATE ULCER",
        "content": ["""- Painful
- Attack me for no reason
- Painful
- Happen too often"""]
    }]

    assert actual_result == expected_result



def test_markdown_conventer_no_title():
    
    actual_result = markdown_to_dict_metadata("Diary", """
For the last 3 days i got painful ulcer and right now is the peak of it. uhhh, i forgot to add title
""")

    expected_result = [{
        "from_file":  "Diary",
        "title": None,
        "content": ["For the last 3 days i got painful ulcer and right now is the peak of it. uhhh, i forgot to add title"]
    }]

    assert actual_result == expected_result




def test_markdown_conventer_multiple_contents():
    
    actual_result = markdown_to_dict_metadata("Diary", """
# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it

And i still code this day
""")

    expected_result = [{
        "from_file":  "Diary",
        "title": "# Dear diary",
        "content": ["For the last 3 days i got painful ulcer and right now is the peak of it", "And i still code this day"]
    }]

    assert actual_result == expected_result



def test_markdown_conventer_text_before_title():
    
    actual_result = markdown_to_dict_metadata("Diary", """
this diary wrote in August 20 2026
# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it
""")

    expected_result = [
        {
            "from_file":  "Diary",
            "title": None,
            "content": ["this diary wrote in August 20 2026"]
        },
        {
            "from_file":  "Diary",
            "title": "# Dear diary",
            "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
        }
    ]

    assert actual_result == expected_result