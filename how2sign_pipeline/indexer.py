"""Build an index.json aligning videos, keypoints and translations."""

import json
from pathlib import Path
from typing import List, Dict

DEFAULT_BASE_DIR = Path("How2Sign_sample")


def build_index(base_dir: Path = DEFAULT_BASE_DIR) -> List[Dict[str, str]]:
    base_dir = Path(base_dir)
    clips_dir = base_dir / "clips"
    keypoints_dir = base_dir / "keypoints"
    translations_dir = base_dir / "translations"
    index = []

    for txt_file in sorted(translations_dir.glob("*.txt")):
        sample_id = txt_file.stem
        phrase = txt_file.read_text().strip()
        entry = {
            "id": sample_id,
            "phrase": phrase,
            "video_path": str(clips_dir / f"{sample_id}.mp4"),
            "keypoints_path": str(keypoints_dir / f"{sample_id}.json"),
        }
        index.append(entry)

    with open(base_dir / "index.json", "w") as f:
        json.dump(index, f, indent=2)

    return index


if __name__ == "__main__":
    build_index()
