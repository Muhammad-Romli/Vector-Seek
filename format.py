def format_top_similarity(similarities: list[dict]):
    print("\n" * 10)
    print("=" * 110)
    print("                    Result of similarities search from most similar to least:                    ")
    print("=" * 110)
    for similarity in similarities:
        print(similarity["chunk"])
        from_file = similarity["chunk"]["from_file"]
        from_title = similarity["chunk"]["from_title"]
        chunk_id = similarity["chunk"]["chunk_id"]
        content = similarity["chunk"]["content"]


        print(f"""


    from_file: {from_file}
    from_title(H1): {from_title}
    chunk_id: {chunk_id}
    content: {content}


{print("\n" * 3)}
{print("-" *  50)}
{print("\n" * 3)}
""")

# similarities variable data, should look like wmbed_metadata like dataflow number 3 in README.md