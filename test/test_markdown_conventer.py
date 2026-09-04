from converter_functions.markdown_converter import markdown_to_dict_metadata
import pytest

def test_markdown_conventer_regular():
    
    actual_result = markdown_to_dict_metadata("Diary", """
# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it
""")

    expected_result = [{
        "from_file":  "Diary",
        "from_title": "# Dear diary",
        "sub_title": None,
        "chunk_id": 1,
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
        "from_title": "# Dear diary",
        "sub_title": None,
        "chunk_id": 1,
        "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
    },
    {
        "from_file": "Diary",
        "from_title": "# REASON WHY I HATE ULCER",
        "sub_title": None,
        "chunk_id": 2,
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
        "from_title": None,
        "sub_title": None,
        "chunk_id": 0,
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
        "from_title": "# Dear diary",
        "sub_title": None,
        "chunk_id": 1,
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
            "from_title": None,
            "sub_title": None,
            "chunk_id": 0,
            "content": ["this diary wrote in August 20 2026"]
        },
        {
            "from_file":  "Diary",
            "from_title": "# Dear diary",
            "sub_title": None,
            "chunk_id": 1,
            "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
        }
    ]

    assert actual_result == expected_result

def test_title_with_no_contents_at_the_end():
    
    actual_result = markdown_to_dict_metadata("Diary", """
this diary wrote in August 20 2026

# Dear diary

For the last 3 days i got painful ulcer and right now is the peak of it

# END
""")

    expected_result = [
        {
            "from_file":  "Diary",
            "from_title": None,
            "sub_title": None,
            "chunk_id": 0,
            "content": ["this diary wrote in August 20 2026"]
        },
        {
            "from_file":  "Diary",
            "from_title": "# Dear diary",
            "sub_title": None,
            "chunk_id": 1,
            "content": ["For the last 3 days i got painful ulcer and right now is the peak of it"]
        }
    ]

    assert actual_result == expected_result


def test_title_with_sub_title_at_the_end():
    
    actual_result = markdown_to_dict_metadata("Diary", """
this diary wrote in March 04 2026

# Dear diary

Just recently, i learnt that is okay to be yourself,
maybe not for me and my school environment, but she somehow did it. 
i wish i was that brave...

She was smart, nice, unique, beautiful and most importantly,
she can enjoy her life without being afraid.
she just wear earphone in class and be herself,
she doesn't care her backpacks have many stickers,
she doesn't scared to make whatsapp statuses,
she don't care if anyone see her badly by her personalities by how she sit,
unlike me....
is small things, but is might be my top 10 most feared things,
she really inspired me to just, let go...

# END
## I promise if i become success and if ONLY i become success
""")

    expected_result = [
        {
            "from_file":  "Diary",
            "from_title": None,
            "sub_title": None,
            "chunk_id": 0,
            "content": ["this diary wrote in March 04 2026"]
        },
        {
            "from_file":  "Diary",
            "from_title": "# Dear diary",
            "sub_title": None,
            "chunk_id": 1,
            "content": ["""Just recently, i learnt that is okay to be yourself,
maybe not for me and my school environment, but she somehow did it. 
i wish i was that brave...""", """She was smart, nice, unique, beautiful and most importantly,
she can enjoy her life without being afraid.
she just wear earphone in class and be herself,
she doesn't care her backpacks have many stickers,
she doesn't scared to make whatsapp statuses,
she don't care if anyone see her badly by her personalities by how she sit,
unlike me....
is small things, but is might be my top 10 most feared things,
she really inspired me to just, let go..."""]
        }
    ]

    assert actual_result == expected_result



def test_sub_title_with_content_at_end():
    
    actual_result = markdown_to_dict_metadata("Diary", """
this diary wrote in March 04 2026

# Dear diary

Just recently, i learnt that is okay to be yourself,
maybe not for me and my school environment, but she somehow did it. 
i wish i was that brave...

She was smart, nice, unique, beautiful and most importantly,
she can enjoy her life without being afraid.
she just wear earphone in class and be herself,
she doesn't care her backpacks have many stickers,
she doesn't scared to make whatsapp statuses,
she don't care if anyone see her badly by her personalities by how she sit,
unlike me....
is small things, but is might be my top 10 most feared things,
she really inspired me to just, let go...

# From The Future
## I promise if i become success and if ONLY i become success
Message from me in the future after getting job:

""")

    expected_result = [
        {
            "from_file":  "Diary",
            "from_title": None,
            "sub_title": None,
            "chunk_id": 0,
            "content": ["this diary wrote in March 04 2026"]
        },
        {
            "from_file":  "Diary",
            "from_title": "# Dear diary",
            "sub_title": None,
            "chunk_id": 1,
            "content": ["""Just recently, i learnt that is okay to be yourself,
maybe not for me and my school environment, but she somehow did it. 
i wish i was that brave...""", """She was smart, nice, unique, beautiful and most importantly,
she can enjoy her life without being afraid.
she just wear earphone in class and be herself,
she doesn't care her backpacks have many stickers,
she doesn't scared to make whatsapp statuses,
she don't care if anyone see her badly by her personalities by how she sit,
unlike me....
is small things, but is might be my top 10 most feared things,
she really inspired me to just, let go..."""]
        },
        {
            "from_file":  "Diary",
            "from_title": "# From The Future",
            "sub_title": "## I promise if i become success and if ONLY i become success",
            "chunk_id": 3,
            "content": ["Message from me in the future after getting job:"]
        },
    ]

    assert actual_result == expected_result