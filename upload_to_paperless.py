from __future__ import annotations

import argparse
import dataclasses as dc
import mimetypes
import os
import sys
import urllib
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import final


@final
@dc.dataclass
class APIConfig:
    endpoint: str
    key: str
    version: int


def guess_mime_type(path: Path) -> str:
    if sys.version_info >= (3, 13):
        type_, _encoding = mimetypes.guess_file_type(path, strict=True)
    else:
        type_, _encoding = mimetypes.guess_type(path, strict=True)

    return type_ or "application/octet-stream"


def upload(api: APIConfig, path: Path, encoding: str = "utf-8") -> None:
    boundary = uuid.uuid4().hex
    url = f"{api.endpoint}/api/documents/post_document/"

    if not url.startswith(("http:", "https:")):
        raise ValueError("URL must start with 'http:' or 'https:'.")

    # Prepare the content
    with path.open("rb") as file:
        body = [
            f"--{boundary}".encode(encoding),
            (
                f"Content-Disposition: form-data; "
                f'name="document"; '
                f'filename="{path.name}"'
            ).encode(encoding),
            f"Content-Type: {guess_mime_type(path)}".encode(encoding),
            b"",
            file.read(),
            b"",
            f"--{boundary}--".encode(encoding),
            b"",
        ]
        content = b"\r\n".join(body)

    # Prepare the headers
    headers = {
        "Accept": f"application/json; version={api.version}",
        "Authorization": f"Token {api.key}",
        "Connection": "keep-alive",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(content)),
    }

    # Request
    request = urllib.request.Request(url, data=content, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(request) as response:
            print(f"OK : {response.read().decode(encoding)}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Response: {e.read().decode(encoding)}")

        raise
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

        raise


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a document to Paperless.")

    parser.add_argument(
        "--endpoint",
        type=str,
        required=False,
        help="The API endpoint URL (e.g., http://localhost:8000).",
        default="http://localhost:8000",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        required=False,
        help=(
            "The API key for authentication. "
            "Can also be set via the PAPERLESS_API_KEY environment variable."
        ),
    )
    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove the file after successful upload.",
    )
    parser.add_argument(
        "file_paths",
        metavar="file_path",
        nargs="+",
        type=str,
        help="The path to the file to upload.",
    )

    args = parser.parse_args()

    if not args.api_key:
        args.api_key = os.getenv("PAPERLESS_API_KEY")

    if not args.api_key:
        print("Error: API key must be provided via --api-key or PAPERLESS_API_KEY.")
        sys.exit(1)

    api_config = APIConfig(
        endpoint=args.endpoint.removesuffix("/"),
        key=args.api_key,
        version=9,
    )

    for p in args.file_paths:
        path = Path(p)

        upload(api_config, path)

        if args.remove:
            path.unlink()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        sys.exit(1)
