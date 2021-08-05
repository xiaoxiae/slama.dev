#!/usr/bin/env python3

import sys
import tempfile
import os
import re
import json
import shutil
import glob

from functools import partial
from subprocess import Popen, PIPE
from datetime import datetime

if len(sys.argv) < 2:
    print("Script should be called with an argument.")
    quit()

os.chdir(os.path.dirname(os.path.realpath(__file__)))

path = sys.argv[1]  # path to the file
name = sys.argv[2]  # name of the post

# useful paths
stripped_name = name.strip("/").split("/")[-1]
tex_name = stripped_name + ".tex"
pdf_name = stripped_name + ".pdf"
pdf_path = os.path.join("..", "assets", pdf_name)  # resulting pdf path

with open(path) as f:
    contents = f.read()

# get header data
header = re.match("---((.|\n)*?)---", contents).group().strip("---").strip()
header_dictionary = {}
for line in header.splitlines():
    a, b = line.split(":")
    a = a.strip()
    b = b.strip()
    header_dictionary[a] = b

# extract date from path and put it to dictionary
match = re.search(r'\d{4}-\d{2}-\d{2}', path.split("/")[-1])
date = datetime.strptime(match.group(), '%Y-%m-%d').date()
header_dictionary["date"] = '"' + date.strftime("%-d. %-m. %Y") + '"'
header_dictionary["url"] = f"https://slama.dev/{stripped_name}"

# create new header
new_header = "---\n" + "\n".join([f"{k}: {v}" for k, v in header_dictionary.items()]) + "\n---\n"

def floatBox(x):
    markdown = x.group(1).strip()

    with open("tmp", "w") as f:
        f.write(markdown)

    _ = Popen(["pandoc", "-f", "markdown+pipe_tables+tex_math_single_backslash ", "-N", "--pdf-engine-opt=-shell-escape", "-i", "tmp", "-o", "tmp.latex"]).communicate()

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
    ## code with language
    (r"```(.+?)\n((.|\n)+?)```", partial(language, lambda x, y: f"\\begin{{minted}}{{{x}}}\n{y}\end{{minted}}")),
    # code without language
    (r"```\n((.|\n)+?)```", r"\\begin{minted}{text}\n\1\\end{minted}"),
    # inline code
    (r"`([^`]+?)`", r"\\mintinline{text}{\1}"),
    # csquotes
    (r"„(.+?)“", r"\\enquote{\1}"),
    # markdown
    (r"<div\s*markdown=\"1\">((.|\n)*?)<\/div>", floatBox),
    # float boxes
    (r"{:\s*.rightFloatBox\s*}\n((.|\n)+?)\n\n", r"\\begin{wrapfigure}{r}{0.25\\textwidth}\n\\begin{framed}\n\1 \\end{framed}\n\\end{wrapfigure}\n"),
    # xopp tags
    (r"{%\s*xopp\s*(.+?)\s*%}", r"\\begin{figure}[H]\n\\center \\includesvg{../_includes/" + stripped_name + r"/\1}\n\\end{figure}"),
    # TOC
    (r"- \.\n{:toc}", r"\\tableofcontents\n\\newpage"),
    # headings
    (r"^##", r""),
    # lecture notes preface
    (r"{%\s+lecture_notes_preface\s+(.+?)\s*\|\s*(.+?)\s*%}", r"# Preface\nThis website contains my lecture notes from a lecture by \1 from the academic year \2. If you find something incorrect/unclear, or would like to contribute either text or an image, feel free to submit a \\url{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull request} (or let me know via email)" if "language" not in header_dictionary or header_dictionary["language"] == "en" else r"# Úvodní informace\nTato stránka obsahuje moje poznámky z přednášky \1 z akademického roku \2. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit \\href{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull requestem} (případně mi dejte vědět na mail."),
    # Pandoc is stupid and requires space between paragraph and a list of items for it to work
    (r"(^[^-\n](.+?))\n(-|(1\.))", r"\1\n\n\3"),
    # if-else for PDF/MD-specific typesetting
    (r"<!---MARKDOWN-->((.|\n)+?)<!---PDF((.|\n)+?)-->", r"\3"),
    # relative file paths from absolute ones
    (r"^!\[(.*?)\]\((.+?)\)", r"![\1](..\2)"),
    # svg images
    (r"^!\[(.*?)\]\((.+?).svg\s*\)", r"\\begin{figure}[H]\n\\center \\includesvg{\2}\n\\end{figure}"),
    # pandoc generates this when converting a standalone list; a bit of a hack but whatever
    (r"\\def\\labelenumi{\\arabic{enumi}\.}", ""),
]

# substitutions that only work first time
first_substitutions = [
    # the new YAML header
    (r"^---((.|\n)*?)^---", new_header),
]

for pattern, sub in substitutions:
    contents = re.sub(pattern, sub, contents, flags=re.MULTILINE)

for pattern, sub in first_substitutions:
    contents = re.sub(pattern, sub, contents, 1, flags=re.MULTILINE)

def replace_math(contents, tag_type, argument, opening, closing):
    tags = {
        "definition": r'**Definice' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "definition:": r'**Definice' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else "") + r"** \1",
        "reminder": r'**Připomenutí' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "remark": r'**Poznámka' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "notation": r'**Značení' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "lemma": r'**Tvrzení' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "theorem": r'**Věta' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "proof": r'**Důkaz' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "algorithm": r'**Algoritmus' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "fact": r'**Fakt' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "example": r'**Příklad' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "consequence": r'**Důsledek' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "observation": r'**(👀)' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
        "question": r'**Otázka' + (" (" + argument.replace('\\', '\\\\') + ")" if argument != '' else ":") + r"** \1",
    }

    return re.sub(re.escape(opening) + r"((.|\n)+?)" + re.escape(closing), tags[tag_type], contents, 1, flags=re.MULTILINE)

stack = []
for entire_tag, tag_type, _, argument in re.findall(r"({%\s*math\s+(.+?)\s+(\"(.+)\")*\s*%}|{%\s*endmath\s*%})", contents):

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
        contents = contents.replace(char, f"\\emoji{{{emojis[char]['name'].replace(' ', '-')}}}")

with open("pdf.tmp", "w") as f:
    f.write(contents)

print(f"generating {pdf_name}")
_ = Popen(["pandoc", "-f", "markdown+pipe_tables+tex_math_single_backslash ", "-N", "--listings", "pdf.tmp", "-o", tex_name, "--template=pdf.latex", "--pdf-engine=lualatex"], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate()
_ = Popen(["latexmk", "-pdf", "-shell-escape", "-pdflatex=lualatex", tex_name], stdin=PIPE, stdout=PIPE, sterr=PIPE).communicate()

os.rename(pdf_name, pdf_path)

# cleanup
if os.path.exists("pdf.tmp"):
    os.remove("pdf.tmp")

for file in glob.glob(stripped_name + ".*"):
    os.remove(file)

for file in glob.glob("_minted*"):
    shutil.rmtree(file)

if os.path.exists("svg-inkscape"):
    shutil.rmtree("svg-inkscape")
