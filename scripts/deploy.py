"""Runs all of the scripts and commands necessary to build the website from
scratch and to deploy it via FTP."""

import os

# clean and build website
os.chdir("..")
os.system("bundle exec jekyll clean")
os.system("bundle exec jekyll build")
os.chdir("scripts")

# upload the website
import upload
