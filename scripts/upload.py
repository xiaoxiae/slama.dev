from ftplib import FTP, error_perm
import os
from getpass import getpass


def remove_content():
    """Recursively removes all non-permanent content."""
    permanent_files = ["info.php", ".gitkeep"]
    permanent_folders = ["subdom", "domains"]

    # for all subdirectories of the current directory
    for content in ftp.nlst():
        # if it's a file
        if "." in content:
            # and the content isn't permanent
            if content not in permanent_files:
                # if it's a file, delete it
                ftp.delete(content)

                print("DELETED FILE: " + ftp.pwd() + "/" + content)
        else:
            # move down to the directory and recursively call remove_content
            ftp.cwd(content)
            remove_content()

            # move up a directory and delete the folder, if it doesn't already exist
            ftp.cwd("..")
            if content not in permanent_folders:
                ftp.rmd(content)

            print("DELETED FOLDER: " + ftp.pwd() + "/" + content)


def add_content():
    "Recursively adds the content from the _site folder to the website."
    # move to the _site
    os.chdir(os.path.join("..", "_site"))

    # get all directories
    directories = []
    for directory in [dir[0] for dir in os.walk(".")]:
        if directory[2:] != "":
            directories.append(directory[2:].replace("\\", "/"))

    # upload (create) all directories
    for directory in sorted(directories):
        if directory not in ftp.nlst():
            ftp.mkd(directory)
            print("CREATED DIRECTORY: " + directory)

    # get all files
    files = [
        os.path.join(root, name)[2:].replace("\\", "/")
        for root, dirs, files in os.walk(".")
        for name in files
    ]

    # upload all files
    for file in files:
        ftp.storbinary("STOR " + file, open(file, "rb"))
        print("CREATED FILE: " + file)


ip = input("\nIP: ")

# repeatedly attempt to connect to the server
while True:
    login = input("Login: ")
    password = getpass("Password: ")

    try:
        with FTP(ip, login, password) as ftp:
            print("Connected!")
            print(ftp.cwd("www"))

            # remove all content that isn't permanent
            remove_content()

            # add all content from _site folder
            add_content()

            # disconnect from the server and terminate the script
            print(ftp.quit())
            quit()
    except Exception as e:
        print(e)
