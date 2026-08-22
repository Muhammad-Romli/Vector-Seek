from search_function import search_top_similarities
import json
import argparse
from format import format_top_similarity


parser = argparse.ArgumentParser(description="Search embeddings for the most similar text to a query")
parser.add_argument("query", type=str, help='Type text that you want to search(query) inside string, like this ("YOUR QUERY")')
parser.add_argument("-n", "--num-of-similarities", type=int, default=5, help="Number of top matching results to return (default: 5)")
args = parser.parse_args()


with open("embeddings.json", "r", encoding="utf-8") as json_file:
    metadata = json.load(json_file)
top_similarities = search_top_similarities(args.query, metadata, args.num_of_similarities)
format_top_similarity(top_similarities)