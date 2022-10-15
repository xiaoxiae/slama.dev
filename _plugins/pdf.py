#!/usr/bin/env python3

import sys
import tempfile
import os
import re
import json
import shutil
import glob
import hashlib
import yaml

from functools import partial
from subprocess import Popen, PIPE
from datetime import datetime

CACHE_FOLDER = "../.jekyll-cache/pdf"
TEMP_LATEX_PATH = "pdf.tmp"

if len(sys.argv) < 2:
    print("Script should be called with an argument.")
    quit()


def get_file_hashsum(file_name: str):
    """Generate a SHA-256 hashsum of the given file."""
    hash_sha256 = hashlib.sha256()

    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)

    return hash_sha256.hexdigest()


os.chdir(os.path.dirname(os.path.realpath(__file__)))

config = {}
if os.path.exists(CACHE_FOLDER):
    with open(CACHE_FOLDER, "r") as f:
        config = yaml.safe_load(f.read()) or {}

path = sys.argv[1]  # path to the file
name = sys.argv[2]  # name of the post

# useful paths
stripped_name = name.strip("/").split("/")[-1]
tex_name = stripped_name + ".tex"
pdf_name = stripped_name + ".pdf"
pdf_path = os.path.join("..", "assets", pdf_name)  # resulting pdf path

with open(path) as f:
    contents = f.read()

hashsum = get_file_hashsum(path)

if (
    stripped_name in config
    and config[stripped_name] == hashsum
    and os.path.exists(pdf_path)
):
    print(f"using cached {pdf_name}.", flush=True)
    quit()

# get header data
header = re.match("---((.|\n)*?)---", contents).group().strip("---").strip()
header_dictionary = {}
for line in header.splitlines():
    # there can be attributes with multiple values, like
    # redirect_from:
    # - one url
    # - another url
    parts = line.split(":")

    if len(parts) != 2:
        continue

    a, b = parts
    a = a.strip()
    b = b.strip()
    header_dictionary[a] = b

# extract date from path and put it to dictionary
match = re.search(r"\d{4}-\d{2}-\d{2}", path.split("/")[-1])
date = datetime.strptime(match.group(), "%Y-%m-%d").date()
header_dictionary["date"] = '"' + date.strftime("%-d. %-m. %Y") + '"'

category_str = ""

if "category" in header_dictionary:
    category_str = header_dictionary["category"].strip('"') + "/"
elif "category_noslug" in header_dictionary:
    category_str = header_dictionary["category_noslug"].strip('"') + "/"

header_dictionary["url"] = f"https://slama.dev/{category_str}{stripped_name}"

# create new header
new_header = (
    "---\n" + "\n".join([f"{k}: {v}" for k, v in header_dictionary.items()]) + "\n---\n"
)


def rightfloatbox(x, counter=[1]):
    text = x.group(1).strip()

    result = (
        r"\begin{wrapfigure}{r}{0.025\textwidth} \hfill \footnotemark"
        + r" \end{wrapfigure} \footnotetext"
        + f"{{{text}}}"
    )
    counter[0] += 1

    return result


def markdownDiv(x):
    markdown = x.group(1).strip()

    with open("tmp", "w") as f:
        f.write(markdown)

    _ = Popen(
        [
            "pandoc",
            "-f",
            "markdown+pipe_tables+tex_math_single_backslash ",
            "-N",
            "--pdf-engine-opt=-shell-escape",
            "-i",
            "tmp",
            "-o",
            "tmp.latex",
        ]
    ).communicate()

    with open("tmp.latex", "r") as f:
        contents = f.read()

    os.remove("tmp")
    os.remove("tmp.latex")

    return contents.strip().replace("\n\n", "\n")


def language(string_function, match):
    """Minted and Markdown have different names for different languages..."""
    mapping = {"cs": "csharp"}

    lang = match.group(1)
    if lang in mapping:
        lang = mapping[lang]

    return string_function(lang, match.group(2))


substitutions = [
    # xopp tags
    (
        r"{%\s*xopp\s*(.+?)\s*%}",
        lambda x: r"\begin{figure}[H] \center \includesvg{../_includes/"
        + stripped_name
        + r"/"
        + x.group(1).split("&")[0].strip()
        + r"}"
        + (
            ""
            if len(x.group(1).split("&")) == 1
            else r"\caption{" + x.group(1).split("&")[1].strip() + r"}"
        )
        + r"\end{figure}"
        + "\n",
    ),
    ## code with language
    (
        r"```(.+?)\n((.|\n)+?)```",
        partial(language, lambda x, y: f"\\begin{{minted}}{{{x}}}\n{y}\end{{minted}}"),
    ),
    # code without language
    (r"```\n((.|\n)+?)```", r"\\begin{minted}{text}\n\1\\end{minted}"),
    # inline code
    (r"`([^`]+?)`", r"\\mintinline{text}{\1}"),
    # csquotes
    (r"„(.+?)“", r"\\enquote{\1}"),
    # markdown
    (r"<div\s*markdown=\"1\">((.|\n)*?)<\/div>", markdownDiv),
    # float boxes\\begin{minipage}{\\textwidth} \\end{minipage}
    # (r"{:\s*.rightFloatBox\s*}\n((.|\n)+?)\n\n", r"\\begin{center}\n\\begin{framed}\n\1 \\end{framed}\n\\end{center}\n"),
    (r"{:\s*.rightFloatBox\s*}\n((.|\n)+?)\n\n", rightfloatbox),
    # TOC
    (r"- \.\n{:toc}", r"\\tableofcontents\n\\newpage"),
    # headings
    (r"^##", r""),
    # lecture notes preface
    (
        r"{%\s+lecture_notes_preface\s+(.+?)\s*\|\s*(.+?)\s*%}",
        r"# Preface\nThis website contains my lecture notes from a lecture by \1 from the academic year \2. If you find something incorrect/unclear, or would like to contribute either text or an image, feel free to submit a \\url{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull request} (or let me know via email)"
        if "language" not in header_dictionary or header_dictionary["language"] == "en"
        else r"# Úvodní informace\nTato stránka obsahuje moje poznámky z přednášky \1 z akademického roku \2. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit \\href{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull requestem} (případně mi dejte vědět na mail.",
    ),
    # Pandoc is stupid and requires space between paragraph and a list of items for it to work
    (r"(^[^-\n](.+?))\n(-|(1\.))", r"\1\n\n\3"),
    # if-else for PDF/MD-specific typesetting
    (r"<!---MARKDOWN-->((.|\n)+?)<!---PDF((.|\n)+?)-->", r"\3"),
    # relative file paths from absolute ones
    (r"^!\[(.*?)\]\((.+?)\)", r"![\1](..\2)"),
    # svg images
    (
        r"^!\[(.*?)\]\((.+?).svg\s*\)",
        r"\\begin{figure}[H]\n\\center \\includesvg{\2}\n\\end{figure}",
    ),
    # pandoc generates this when converting a standalone list; a bit of a hack but whatever
    (r"\\def\\labelenumi{\\arabic{enumi}\.}", ""),
    # remove things like \{: style=``max-width: 50\%'' :\}
    ("{:\s*style=(.+?):}", ""),
    # other images
    (r"^!\[(.*?)\]\((.+?)\s*\)", r"\\includegraphics[max width=\\textwidth]{\2}"),
]

# substitutions that only work the first time
first_substitutions = [
    # the new YAML header
    (r"^---((.|\n)*?)^---", new_header),
]

for pattern, sub in substitutions:
    contents = re.sub(pattern, sub, contents, flags=re.MULTILINE)

for pattern, sub in first_substitutions:
    contents = re.sub(pattern, sub, contents, 1, flags=re.MULTILINE)


def replace_math(contents, tag_type, argument, opening, closing):
    # TODO: this doesn't match web
    # there should be no if argument != "" else : here
    # it should just be : or not :
    tags = {
        "definition": r"**Definice"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "definition:": r"**Definice"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else "")
        + r"** \1",
        "reminder": r"**Připomenutí"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "remark": r"**Poznámka"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "notation": r"**Značení"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "lemma": r"**Lemma"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "claim": r"**Tvrzení"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "theorem": r"**Věta"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "proof": r"**Důkaz"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "algorithm": r"**Algoritmus"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "fact": r"**Fakt"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "problem": r"**Problém"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "example": r"**Příklad"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "consequence": r"**Důsledek"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "observation": r"**(👀)"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
        "question": r"**Otázka"
        + (" (" + argument.replace("\\", "\\\\") + ")" if argument != "" else ":")
        + r"** \1",
    }

    return re.sub(
        re.escape(opening) + r"((.|\n)+?)" + re.escape(closing),
        tags[tag_type],
        contents,
        1,
        flags=re.MULTILINE,
    )


# math
stack = []
for entire_tag, tag_type, _, argument in re.findall(
    r"({%\s*math\s+(.+?)\s+(\"(.+)\")*\s*%}|{%\s*endmath\s*%})", contents
):

    # closing tag
    if tag_type == "":
        opening, tag_type, argument = stack.pop()
        contents = replace_math(contents, tag_type, argument, opening, entire_tag)
    else:
        stack.append((entire_tag, tag_type, argument))

# emojis
with open("emoji.json") as f:
    emojis = json.load(f)

for char in list(contents):
    if char in emojis:
        contents = contents.replace(
            char, f"\\emoji{{{emojis[char]['name'].replace(' ', '-')}}}"
        )

with open(TEMP_LATEX_PATH, "w") as f:
    f.write(contents)

print(f"generating {pdf_name}...", flush=True, end="")
config[stripped_name] = hashsum

p = Popen(
    [
        "pandoc",
        "-f",
        "markdown+pipe_tables+tex_math_single_backslash ",
        "-N",
        "--listings",
        TEMP_LATEX_PATH,
        "-o",
        tex_name,
        "--template=pdf.latex",
        "--pdf-engine=lualatex",
    ],
    stdin=PIPE,
    stdout=PIPE,
    stderr=PIPE,
)

def cleanup():
    if os.path.exists(TEMP_LATEX_PATH):
        os.remove(TEMP_LATEX_PATH)

    for file in glob.glob(stripped_name + ".*"):
        os.remove(file)

    for file in glob.glob("_minted*"):
        shutil.rmtree(file)

    if os.path.exists("svg-inkscape"):
        shutil.rmtree("svg-inkscape")

with open(CACHE_FOLDER, "w") as f:
    f.write(yaml.dump(config))

result = p.communicate()
if p.returncode:
    print("ERROR during converting form Markdown to LaTeX:")
    for line in result[1]:
        print(f"| {line}")
    cleanup()
    quit()

p = Popen(
    ["latexmk", "-pdf", "-shell-escape", "-pdflatex=lualatex", tex_name],
    stdin=PIPE,
    stdout=PIPE,
    stderr=PIPE,
)
result = p.communicate()
if p.returncode:
    print("ERROR during generating a PDF:")
    for line in result[1].decode().splitlines():
        print(f"| {line}")
    cleanup()
    quit()

os.rename(pdf_name, pdf_path)

cleanup()

print(f" generated.", flush=True)
