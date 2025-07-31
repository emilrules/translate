"""Search indexed How2Sign phrases."""

import json
from pathlib import Path
from typing import Optional, Dict
from rapidfuzz import fuzz

DEFAULT_INDEX_PATH = Path("How2Sign_sample/index.json")


def load_index(index_path: Path = DEFAULT_INDEX_PATH):
    with open(index_path) as f:
        return json.load(f)


def search_clip(query: str, index_path: Path = DEFAULT_INDEX_PATH) -> Optional[Dict[str, str]]:
    index = load_index(index_path)
    best = None
    best_score = -1
    for entry in index:
        score = fuzz.partial_ratio(query.lower(), entry["phrase"].lower())
        if score > best_score:
            best = entry
            best_score = score
    return best


if __name__ == "__main__":
    import sys
    query = " ".join(sys.argv[1:])
    result = search_clip(query)
    print(json.dumps(result, indent=2))
