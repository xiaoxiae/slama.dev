import codecs
from os import path, listdir, makedirs

import pypandoc
from regex import compile, sub, MULTILINE


def get_files_with_extension(folder, extension):
    """Returns a list of the names of files from a folder with the said extension."""
    return [file for file in listdir(path.join(folder, '.')) if file.endswith(extension)]


def read_utf8_file(source):
    """Returns the contents of the specified utf-8 encoded file."""
    return codecs.open(source, 'r', encoding='utf8').read()


def write_utf8_file(destination_path, destination_file_name, contents):
    """Saves the contents to the specified utf-8 encoded file."""
    # ensure that the path exists
    makedirs(destination_path, exist_ok=True)

    with codecs.open(path.join(destination_path, destination_file_name), 'w', encoding='utf8') as file:
        file.write(contents)


def copy_utf8_file(source_path, destination_path, destionation_file_name):
    """Copies the specified utf-8 encoded file to the specified destination."""
    write_utf8_file(destination_path, destionation_file_name, read_utf8_file(source_path))


def substitute_str(string, substitutions):
    """Returns a string that has been substituted using all of the specified substitutions.
    :param substitutions: A list of tuples, where t[0] and t[1] are the 1st and 2nd regex.sub parameters."""

    for substitution in substitutions:
        string = sub(*substitution, string, flags=MULTILINE)

    return string


def get_config_from_jekyll(source):
    """Gets the site title and URL from the specified .yml file."""
    contents = read_utf8_file(source)

    title = compile(r'^title: *?" *(.+?) *"', flags=MULTILINE).search(contents).group(1)
    url = compile(r'^url: *?" *(.+?) *"', flags=MULTILINE).search(contents).group(1)

    return [title, url]


# SCRIPT VARIABLES
script_location = path.dirname(path.abspath(__file__))

# folders
input_folder = path.join(path.expanduser('~'), "Documents", "Wiki")
output_folder = path.join(script_location, "..", "..", "_site", "subdom", "wiki")
includes_folder = path.join(script_location, "includes")

# page settings
site_title, site_url = get_config_from_jekyll(path.join(script_location, '..', '..', '_config.yml'))
page_title = ""
page_structure = "{head}\n<body>\n{content}\n</body>"

# substitutions for Markdown
md_substitutions = [
    (r'(^[^-#\s].*?\n)-', '\g<1>\n-')
]

# substitutions for HTML
html_substitutions = [
    (r'<li><p>(.+)<\/p><\/li>', '<li>\g<1></li>'),  # fix for incorrectly formatted list items
    (r'\[\[(.+?)\]\]', '<a href="\g<1>.html">\g<1></a>'),  # wiki links to relative links
    (r'{{ *(.+?) *?}}', lambda x: site_title if x.group(1) == "site_title" \
        else page_title if x.group(1) == "page_title" \
        else site_url if x.group(1) == "page_url" \
        else "")  # liquid-like tags
]

for md_file_name in get_files_with_extension(input_folder, ".md"):
    # read the markdown file
    md_content = read_utf8_file(path.join(input_folder, md_file_name))
    md_content = substitute_str(md_content, md_substitutions)

    # convert the markdown file to pandoc
    head = read_utf8_file(path.join(includes_folder, "head.html"))
    html_content = pypandoc.convert_text(md_content, "html", format="md")

    # file + the contents
    html_file_content = page_structure.format(head=head, content=html_content)
    html_file_content = substitute_str(html_file_content, html_substitutions)

    # the name of the article
    page_title = md_file_name[:-3]

    # write the html file
    write_utf8_file(output_folder, page_title + ".html", html_file_content)

# copy the CSS style sheet to the output folder
copy_utf8_file(path.join(includes_folder, "main.css"), path.join(output_folder, "assets"), "main.css")
