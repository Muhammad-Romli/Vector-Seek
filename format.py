import shutil
import textwrap


BOLD = "\033[1m"
RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
BRIGHT_GREEN = "\033[92m"

def format_top_similarity(embed_metadatas: list[dict], num_shown: int):
    width = shutil.get_terminal_size().columns

    print("\n" * 3)
    print("=" * width)
    print(f"                    {CYAN}{BOLD}Result of similarities search from most similar to least:{RESET}                    ")
    print("=" * width)
    count = 0
    for embed_metadata in embed_metadatas[:num_shown]:
        wrapped_text = textwrap.fill(embed_metadata["content"], 
                                    width=100,
                                    initial_indent="\t",
                                    subsequent_indent="\t",)
        count += 1
        print(f"""

        {BOLD}{GREEN}RESULT {count}{RESET}:
{wrapped_text}

{BRIGHT_GREEN}{BOLD}{'FROM_FILE':<12}:{RESET} {embed_metadata["metadata"]["from_file"]}
{BRIGHT_GREEN}{BOLD}{'FROM_TITLE':<12}:{RESET} {embed_metadata["metadata"]["from_title"]}
{BRIGHT_GREEN}{BOLD}{'CHUNK ID':12}:{RESET} {embed_metadata["metadata"]["chunk_id"]}


{"_" * width}
""")
    print("\n" * 3)

# embed_metadatas variable data, should look like wmbed_metadata like dataflow number 3 in README.md