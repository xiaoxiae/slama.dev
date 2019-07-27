"""Runs all of the scripts and commands necessary to build the website from
scratch and to deploy it via FTP."""

import os

# move to the directory of this script, so it can execute system commands in appropriate
# directories
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# clean and build website
os.chdir("..")
os.system("bundle exec jekyll clean")
os.system("bundle exec jekyll build")
os.chdir("scripts")

# convert the wiki to a page
import wiki_to_html.__main__

# upload the website
import upload
