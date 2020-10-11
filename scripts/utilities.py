import hashlib
from typing import *
from subprocess import Popen, PIPE


def get_file_hashsum(file_name: str):
    """Generate a SHA-256 hashsum of the given file."""
    hash_sha256 = hashlib.sha256()

    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


def get_string_hashsum(string: str):
    """Generate a SHA-256 hashsum of the given string."""
    return hashlib.sha256(string.encode()).hexdigest()


def print_formatted_message(sub, obj):
    """Print Jekyll-like status string with a given subject."""
    print(f"{sub.rjust(18)}: {obj}")
