"""Download a small How2Sign subset with videos, keypoints and translations."""

from pathlib import Path
import json
from typing import Union

from datasets import load_dataset
from tqdm import tqdm

DATASET_NAME = "how2sign/how2sign"
SPLIT = "train"
DEFAULT_OUTPUT_DIR = Path("How2Sign_sample")


def download_samples(num_samples: int = 100, output_dir: Union[str, Path] = DEFAULT_OUTPUT_DIR) -> None:
    """Download ``num_samples`` samples of How2Sign to ``output_dir``."""
    output_dir = Path(output_dir)
    clips_dir = output_dir / "clips"
    keypoints_dir = output_dir / "keypoints"
    translations_dir = output_dir / "translations"
    for d in (clips_dir, keypoints_dir, translations_dir):
        d.mkdir(parents=True, exist_ok=True)

    dataset = load_dataset(DATASET_NAME, split=f"{SPLIT}[:{num_samples}]")

    for sample in tqdm(dataset, desc="Downloading samples"):
        sample_id = str(sample.get("id") or sample.get("video_id") or sample.get("name"))
        if not sample_id:
            raise ValueError("Sample is missing an identifier")

        # Video
        video = sample.get("video")
        video_dst = clips_dir / f"{sample_id}.mp4"
        if isinstance(video, dict) and "path" in video:
            Path(video["path"]).rename(video_dst)
        elif hasattr(video, "export"):
            video.export(str(video_dst))
        else:
            raise ValueError("Unexpected video representation")

        # Keypoints
        keypoints = sample.get("keypoints") or sample.get("pose")
        if keypoints is not None:
            with open(keypoints_dir / f"{sample_id}.json", "w") as f:
                json.dump(keypoints, f)

        # Translation
        phrase = sample.get("translation") or sample.get("text")
        if phrase is not None:
            with open(translations_dir / f"{sample_id}.txt", "w") as f:
                f.write(phrase.strip())


if __name__ == "__main__":
    download_samples()
