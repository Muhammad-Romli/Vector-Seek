BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BRIGHT_GREEN = "\033[92m"

def format_top_similarity(embed_metadatas: list[dict], num_shown: int):


    print("\n" * 10)
    print("=" * 110)
    print(f"                    {CYAN}{BOLD}Result of similarities search from most similar to least:{RESET}                    ")
    print("=" * 110)
    count = 0
    for embed_metadata in embed_metadatas[:num_shown]:
        count += 1
        print(f"""

        {BOLD}{GREEN}RESULT {count}{RESET}:
{embed_metadata["content"]}

{BRIGHT_GREEN}{BOLD}FROM_FILE:{RESET} {embed_metadata["metadata"]["from_file"]}
{BRIGHT_GREEN}{BOLD}FROM_TITLE:{RESET} {embed_metadata["metadata"]["from_title"]}
{BRIGHT_GREEN}{BOLD}CHUNK ID:{RESET} {embed_metadata["metadata"]["chunk_id"]}


{"_" * 110}
""")

# embed_metadatas variable data, should look like wmbed_metadata like dataflow number 3 in README.md