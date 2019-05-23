import codecs
from os import path, listdir, makedirs

import pypandoc
from regex import compile, sub, MULTILINE


def get_files_with_extension(source, extension):
    """Returns a list of the names of files from the source folder with the said extension."""
    return [file for file in listdir(path.join(source, '.')) if file.endswith(extension)]


def read_utf8_file(source):
    """Returns the contents of the specified utf-8 encoded file."""
    return codecs.open(source, 'r', encoding='utf8').read()


def write_utf8_file(destination_path, destination_file_name, contents):
    """Saves the contents to the specified utf-8 encoded file."""
    # ensure that the path exists
    makedirs(destination_path, exist_ok=True)

    # write the file
    with codecs.open(path.join(destination_path, destination_file_name), 'w', encoding='utf8') as file:
        file.write(contents)


def copy_utf8_file(source_path, destination_path, destination_file_name):
    """Copies the specified utf-8 encoded file to the specified destination."""
    write_utf8_file(destination_path, destination_file_name, read_utf8_file(source_path))


def perform_regex_substitutions(string, substitutions):
    """Returns a string that has been substituted using a list of regex substitutions.
    :param string: The string to be substituted.
    :param substitutions: A list of tuples, where t[0] and t[1] are the 1st and 2nd regex.sub() parameters."""

    for substitution in substitutions:
        string = sub(*substitution, string, flags=MULTILINE)

    return string


def get_config_from_jekyll(source, variable):
    """Gets a Jekyll variable from an .yml file."""
    contents = read_utf8_file(source)

    return compile(r'^' + variable + r': *?" *(.*?) *"', flags=MULTILINE).search(contents).group(1)


def substitute_liquid_variables(content, file_name, variables):
    """Substitute the liquid-like variables."""
    # add the special section title variable to the mix
    all_variables = {**variables, **{"section_title": file_name}}
    
    for variable, substitution in all_variables.items():
        content = sub(r"\{\{ *" + variable + r" *\}\}", substitution, content, flags=MULTILINE)

    return content


# SCRIPT VARIABLES
# path to this script
script_location = path.dirname(path.abspath(__file__))

# generation-related folders
includes_folder = path.join(script_location, "includes")
site_folder = path.join(script_location, "..", "..")

wiki_folder = path.join(path.expanduser('~'), "Documents", "Wiki")
output_folder = path.join(site_folder, "_site", "subdom", "wiki")

# files used in the conversion
site_config_file = path.join(site_folder, '_config.yml')

# liquid-like variables used in the conversion
site_variables = {
    "description": "Tom's personal wiki.",
    "website_title": get_config_from_jekyll(site_config_file, "title"),
    "url": get_config_from_jekyll(site_config_file, "wiki-url")
}

page_structure = "{head}\n<body>\n{content}\n</body>"

# substitutions for Markdown
md_substitutions = [
    (r'(^[^-#\s].*?\n)-', r'\g<1>\n-')  # prevent incorrect Pandoc formatting of lists after text
]

# substitutions for HTML
html_substitutions = [
    (r'<li><p>(.+)<\/p><\/li>', r'<li>\g<1></li>'),  # fix for incorrectly formatted list items
    (r'\[\[(.+?)\]\]', r'<a href="\g<1>.html">\g<1></a>'),  # wiki links to relative links
]

# CONVERSION
for md_file_name in get_files_with_extension(wiki_folder, ".md"):
    # read the markdown file and perform regex substitutions
    md_content = read_utf8_file(path.join(wiki_folder, md_file_name))
    md_content = perform_regex_substitutions(md_content, md_substitutions)

    # convert the file to HTML using Pandoc
    html_content = pypandoc.convert_text(md_content, "html", format="md")

    # add additional content (head,...) and perform regex substitutions
    head = read_utf8_file(path.join(includes_folder, "head.html"))
    html_file_content = page_structure.format(head=head, content=html_content)
    html_file_content = perform_regex_substitutions(html_file_content, html_substitutions)

    #  swap for liquid-like variables
    html_file_content = substitute_liquid_variables(html_file_content, md_file_name[:-3].lower(), site_variables)

    # write the html file
    write_utf8_file(output_folder, md_file_name[:-3] + ".html", html_file_content)

# copy the CSS style sheet to the output folder
copy_utf8_file(path.join(includes_folder, "main.css"), path.join(output_folder, "assets"), "main.css")
