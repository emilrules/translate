"""Utility to upload files to Amazon S3."""

import os
from pathlib import Path
from typing import Optional

import boto3


def upload_to_s3(file_path: Path, bucket: str, key: Optional[str] = None) -> str:
    """Upload ``file_path`` to ``bucket`` and return the public URL."""
    file_path = Path(file_path)
    key = key or file_path.name
    s3 = boto3.client("s3")
    s3.upload_file(str(file_path), bucket, key, ExtraArgs={"ACL": "public-read"})
    return f"https://{bucket}.s3.amazonaws.com/{key}"


__all__ = ["upload_to_s3"]
