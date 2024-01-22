#!/usr/bin/env python3

import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse
from collections import defaultdict
import glob
from concurrent.futures import ThreadPoolExecutor
import requests


def find_html_files(directory):
    """Recursively get all HTML files in a given directory."""
    html_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def parse_links(html_file):
    """Parse all links in an HTML file."""
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        return links

def strip_link(url):
    """Remove parameters/queries/fragments from a URL."""
    parsed_url = urlparse(url)
    stripped_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return stripped_url

def get_status_code(url, timeout=5):
    """Check the status code of a given website."""
    try:
        return requests.head(url, timeout=timeout).status_code
    except requests.exceptions.Timeout as e:
        return -1
    except requests.exceptions.ConnectionError as e:
        print(url, e)
        return -2


DIRECTORY_PATH = '../_site/'
LOCAL_SERVER_ADDRESS = "http://localhost:4000"

is_local_running = get_status_code(LOCAL_SERVER_ADDRESS)
assert is_local_running == 200, "Local instance not running?"

weird_link_set = set()
link_dict = defaultdict(set)

print("Gathering links...")
files = find_html_files(DIRECTORY_PATH)
for i, html_file in enumerate(files):
    links = parse_links(html_file)

    for link in links:
        link = strip_link(link)

        if link.startswith("/"):
            link = LOCAL_SERVER_ADDRESS + link

        if len(link) == 0:
            continue
        elif not link.startswith("http") and link not in weird_link_set:
            print(f"{html_file}: Relative or non-HTTP link '{link}'")
            weird_link_set.add(link)
        else:
            link_dict[link].add(html_file)

    print(f"[{i+1}/{len(files)}]: got {len(link_dict)} links (after {html_file}).")


print()
print("Visiting...")

with ThreadPoolExecutor(max_workers=8) as executor:
    for i, (url, files, status) in enumerate(
        executor.map(lambda x: (x[0], x[1], get_status_code(x[0])), link_dict.items())
    ):
        if 400 <= status < 600 or status == -1:  # -1 for timeout
            print(f"[{i+1}/{len(link_dict)}] {status if status != -1 else 'TIMEOUT'} on '{url}', found in {files}")
