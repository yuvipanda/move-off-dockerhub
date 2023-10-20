#!/usr/bin/env python
"""
Simple script to copy files from dockerhub to quay.io of tags that match a regex
"""
import argparse
import subprocess
import time
import json
import re


def list_tags(image: str):
    resp = json.loads(
        subprocess.check_output(["skopeo", "list-tags", f"docker://{image}"]).decode()
    )
    return sorted(resp["Tags"])


def copy_image(src_image: str, dest_image: str):
    subprocess.check_call(
        [
            "skopeo",
            "copy",
            "--multi-arch",
            "all",
            f"docker://{src_image}",
            f"docker://{dest_image}",
        ]
    )


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("src_image", help="Name of image to copy from")
    argparser.add_argument("dest_image", help="Name of image to copy to")
    argparser.add_argument(
        "tag_regex", help="Copy all source image tags that match this regex"
    )
    argparser.add_argument(
        "--dry-run", action="store_true", help="Just print what would be copied"
    )

    args = argparser.parse_args()

    all_tags = list_tags(args.src_image)

    tags_to_copy = [t for t in all_tags if re.match(args.tag_regex, t)]

    print("Copying the following tags:")
    print("\n".join(tags_to_copy))

    if not args.dry_run:
        for i, tag in enumerate(tags_to_copy):
            print(f"Copying {tag} ({i + 1} of {len(tags_to_copy)})")
            start_time = time.monotonic()
            copy_image(f"{args.src_image}:{tag}", f"{args.dest_image}:{tag}")
            print(f"Done copying {tag} in {time.monotonic() - start_time}s")


if __name__ == '__main__':
    main()
