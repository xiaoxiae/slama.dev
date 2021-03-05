#!/usr/bin/python3

# TODO: store more information in the checksum file to make the update faster
#       - it's quite slow to recurse using FTP
# TODO: Update file, instead of remove file > add file

import argparse
import hashlib
import json
import os
from ftplib import FTP, error_perm
from getpass import getpass
from glob import glob
from subprocess import DEVNULL, PIPE, Popen
from typing import *

checksum_file_name = "checksum.json"

# files and folders not to remove
permanent_files = ["info.php", ".gitkeep", checksum_file_name, "hlenka-helenka.jpg"]
permanent_folders = ["subdom", "domains"]


parser = argparse.ArgumentParser(description="Smart-upload a folder via FTP.")

parser.add_argument("ip")
parser.add_argument("username")
parser.add_argument("password")

parser.add_argument(
    "-d",
    "--debug",
    "--dry-run",
    help="only print the actions, don't actually do them",
    action="store_true",
    dest="debug",
)

parser.add_argument(
    "-l",
    "--local-path",
    help="the folder to upload; defaults to '_site'",
    default="_site",
)

parser.add_argument(
    "-s",
    "--server-path",
    help="the folder to upload to; defaults to 'www'",
    default="www",
)

parser.add_argument(
    "-f",
    "--force",
    help="ignore the checksum file (meaning everything is removed an then uploaded)",
    action="store_true",
)

arguments = parser.parse_args()


def remove_content(old: Dict[str, str], new: Dict[str, str]):
    """Removes all relevant content on the FTP server."""
    pwd = ftp.pwd()

    # for all subdirectories of the current directory
    for content in ftp.nlst():
        # a very not-pretty way to determine if a path is a file or not
        # a little slow but probably better than anything else
        # see https://stackoverflow.com/questions/1088336/ftplib-checking-if-a-file-is-a-folder
        is_file = True
        try:
            ftp.size(content)
        except Exception:
            is_file = False

        # get the folder/file path relative to the website ftp folder
        relpath = (pwd + "/" + content)[len(arguments.server_path) + 2 :]

        # if it's a file
        if is_file:
            # and the content, if it isn't permanent
            if content not in permanent_files and not hashsums_match(old, new, relpath):
                # if it's a file, delete it
                print(f"     Removing file: {relpath}...", end="", flush=True)
                if not arguments.debug:
                    ftp.delete(content)
                print(" done.")

        elif content not in permanent_folders:
            # move down to the directory and recursively call remove_content
            ftp.cwd(content)
            remove_content(old, new)

            remaining_files = len(ftp.nlst())
            ftp.cwd("..")

            if remaining_files == 0:
                print(f"Removing directory: {relpath}...", end="", flush=True)
                if not arguments.debug:
                    ftp.rmd(content)
                print(" done.")


def add_content(old: Dict[str, str], new: Dict[str, str]):
    """Add the content of the current folder to the website."""
    # get all directories
    directories = []
    for directory, _, _ in os.walk("."):
        stripped_directory = directory[2:]

        if stripped_directory != "":
            # the replace is for windows' paths
            directories.append(stripped_directory.replace(os.sep, "/"))

    # upload (create) all directories first
    for directory in sorted(directories):
        # a hack for only creating non-existent directories
        try:
            pwd = ftp.pwd()
            ftp.cwd(directory)
            ftp.cwd(pwd)
        except Exception as e:
            print(f"Creating directory: {directory}...", end="", flush=True)
            if not arguments.debug:
                ftp.mkd(directory)
            print(" done.")

    # upload files...
    for file in new:
        # that are not ignored and didn't match hashsums
        if not hashsums_match(old, new, file):
            print(f"    Uploading file: {file}...", end="", flush=True)
            if not arguments.debug:
                ftp.storbinary("STOR " + file, open(file, "rb"))
            print(" done.")


def hashsums_match(old: Dict[str, str], new: Dict[str, str], key: str):
    """Return True if a key is in both the dictionaries and its value matches."""
    return key in old and key in new and old[key] == new[key]


def generate_hashsum(file_name):
    """Generate a SHA-256 hashsum of the given file."""
    hash_sha256 = hashlib.sha256()

    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


def get_hashsum_dictionary():
    """Return a dictionary of hashes of file contents in the current directory and all
    its subdirectories."""
    return {
        f: generate_hashsum(f)
        for f in [
            os.path.join(root, name)[2:]
            for root, dirs, files in os.walk(".")
            for name in files
        ]
    }


# change to the _site directory (if it exists)
if not os.path.exists(arguments.local_path):
    print(f"               FTP: The folder {arguments.local_path} does not exist, exiting.")
    quit()


os.chdir(arguments.local_path)

print(f"               FTP: Connecting to {arguments.ip}...", end="", flush=True)
with FTP(arguments.ip, arguments.username, arguments.password) as ftp:
    print(" connected.")

    ftp.cwd(arguments.server_path)

    new = get_hashsum_dictionary()
    json.dump(new, open(checksum_file_name, "w"), indent=4, sort_keys=True)

    # get the old hashsum
    old = {}
    if checksum_file_name in ftp.nlst() and not arguments.force:
        # get the old checksum by reading the file on the server
        lines = []
        ftp.retrlines(f"RETR {checksum_file_name}", lambda x: lines.append(x))

        old = json.loads("\n".join(lines))

    # remove all content that isn't permanent
    remove_content(old, new)

    # add all content from _site folder which is not ignored
    add_content(old, new)

    # always manually update the checksum file at the end
    if not arguments.debug:
        if checksum_file_name in ftp.nlst():
            ftp.delete(checksum_file_name)
        ftp.storbinary("STOR " + checksum_file_name, open(checksum_file_name, "rb"))

    # disconnect from the server and terminate the script
    ftp.quit()

    print(f"               FTP: Done.")
