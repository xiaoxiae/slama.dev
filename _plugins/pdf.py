#!/usr/bin/env python3

# TODO:
# - proper margins
# - TOC
# - title page

import sys
import tempfile
import os
import re
from subprocess import Popen
from datetime import datetime

os.chdir(os.path.dirname(os.path.realpath(__file__)))

path = sys.argv[1]  # path to the file
name = sys.argv[2]  # name of the post

# useful paths
stripped_name = name.strip("/").split("/")[-1]
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

substitutions = [
    # xopp tagy
    (r"{%\s*xopp\s*(.+?)\s*%}", r"\\begin{figure}[H]\n\\center \\includesvg{../_includes/" + stripped_name + r"/\1}\n\\end{figure}"),
    # TOC
    (r"- \.\n{:toc}", r"\\tableofcontents\n\\newpage"),
    # nadpisy
    (r"^##", r""),
    # lecture notes preface
    (r"{%\s+lecture_notes_preface\s+(.+?)\s*\|\s*(.+?)\s*%}", r"# Preface\nThis website contains my lecture notes from a lecture by \1 from the academic year \2. If you find something incorrect/unclear, or would like to contribute either text or an image, feel free to submit a \\url{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull request} (or let me know via email)" if "language" not in header_dictionary or header_dictionary["language"] == "en" else r"# Úvodní informace\nTato stránka obsahuje moje poznámky z přednášky \1 z akademického roku \2. Pokud by byla někde chyba/nejasnost, nebo byste rádi někam přidali obrázek/text, tak stránku můžete upravit \\href{https://github.com/xiaoxiae/slama.dev/blob/master/\_posts/}{pull requestem} (případně mi dejte vědět na mail."),
    # Pandoc is stupid and requires space between paragraph and a list of items
    (r"(^[^-\n](.+?))\n(-|(1\.))", r"\1\n\n\3"),
    # if-else for PDF typesetting
    (r"<!---MARKDOWN-->((.|\n)+?)<!---PDF((.|\n)+?)-->", r"\3"),
    # relative file paths from absolute ones
    (r"^!\[(.*?)\]\((.+?)\)", r"![\1](..\2)"),
    # svg images
    (r"^!\[(.*?)\]\((.+?).svg\s*\)", r"\\begin{figure}[H]\n\\center \\includesvg{\2}\n\\end{figure}"),
]

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

with open("pdf.tmp", "w") as f:
    f.write(contents)

print(f"generating {pdf_name}")
_ = Popen(["pandoc", "-f", "markdown+pipe_tables+tex_math_single_backslash ", "-N", "--pdf-engine-opt=-shell-escape", "-i", "pdf.tmp", "-o", pdf_path, "--template=pdf.latex", "--pdf-engine=lualatex"]).communicate()
