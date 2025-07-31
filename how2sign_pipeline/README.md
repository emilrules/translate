# How2Sign Pipeline

This package provides utilities to download a small subset of the [How2Sign](https://how2sign.github.io/) dataset, build an index, search by phrase, generate Blender animations and optionally upload results to Amazon S3.

## Installation

```bash
pip install datasets tqdm rapidfuzz boto3
```

## Download the Sample

```bash
python -m how2sign_pipeline.download_sample
```

This creates a `How2Sign_sample/` directory with clips, keypoints and translations for the first 100 samples.

## Build the Index

```bash
python -m how2sign_pipeline.indexer
```

`index.json` is written inside the sample directory.

## Searching

```python
from how2sign_pipeline.search import search_clip

result = search_clip("Welcome to the library")
print(result)
```

## Generating Blender Animations

```python
from how2sign_pipeline.animate import generate_blender_script

script = generate_blender_script('How2Sign_sample/keypoints/clip001.json', 'output.mp4')
```

Run Blender headlessly:

```bash
blender -b my_avatar.blend -P generated_script.py -o //output.mp4 -a
```

## Upload to S3 (optional)

```python
from how2sign_pipeline.s3_upload import upload_to_s3
url = upload_to_s3('output.mp4', 'my-bucket')
print(url)
```

Ensure your AWS credentials are configured via environment variables or AWS config files.
