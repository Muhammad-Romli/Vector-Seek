def format_top_similarity(similarities: list[dict]):
    print("=" * 50)
    print("                    Result of similarities search from most similar to least:                    ")
    print("=" * 50)
    for similarity in similarities:
        from_file = similarity["chunk"]["from_file"]
        from_title = similarity["chunk"]["from_title"]
        chunk_id = similarity["chunk"]["chunk_id"]
        content = similarity["chunk"]["content"]


        print(f"""


    from_file: {from_file}
    from_title(H1): {from_title}
    chunk_id: {chunk_id}
    content: {content}

{print("-" *  50)}
""")

# similarities variable data, should look like wmbed_metadata like dataflow number 3 in README.md