import os
import sys
import argparse
from pathlib import Path
from subprocess import call
from datetime import date
from datetime import datetime


DIARY_DIR = os.environ.get("DIARY_DIR")
DIARY_EDITOR = os.environ.get("DIARY_EDITOR")
if DIARY_DIR is None:
    DIARY_DIR = os.path.join(Path.home(), "diary")
if DIARY_EDITOR is None:
    DIARY_EDITOR = "vim"


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError as e:
        raise SystemExit(e)


def edit_entry(target_date = None):
    if not target_date:
        target_date = date.today()
    entry_directory = os.path.join(DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
    if not os.path.isdir(entry_directory):
        os.makedirs(entry_directory)
    date_str = target_date.strftime("%Y-%m-%d")
    file_name = date_str + ".md"
    entry_path = os.path.join(os.path.join(entry_directory, file_name))
    entry_exist = False
    if os.path.isfile(entry_path):
        entry_exist = True
    with open(entry_path, "a") as entry:
        if not entry_exist:
            entry.write(datetime.strftime(target_date, "## %Y-%m-%d, %A"))
        entry.flush()
        call([DIARY_EDITOR, entry_path])


def cat_entry():
    target_date = date.today()
    entry_directory = os.path.join(DIARY_DIR, str(target_date.year), "{:02}".format(target_date.month))
    file_name = target_date.strftime("%Y-%m-%d") + ".md"
    entry_path = os.path.join(os.path.join(entry_directory, file_name))
    if os.path.isfile(entry_path):
        with open(entry_path, "r") as entry:
            print(entry.read())
    else:
        print("Diary for today not created yet")


# def main():
#     args = sys.argv[1:]
#     if not args:
#         edit_entry()
#     elif args[0] == "cat":
#         cat_entry()
#     else:
#        edit_entry(parse_date(args[0]))

# Add new function to search
def find_entry(search_str):
    # Create a list to collect matched entries
    matched_entries = []

    # Go through each year directory in the diary directory
    for year_dir in Path(DIARY_DIR).iterdir():
        if year_dir.is_dir():  # Add this check to ensure it's a directory
            for month_dir in year_dir.iterdir():
                if month_dir.is_dir():  # Likewise, add this check here too
                    for entry_file in month_dir.iterdir():
                        if entry_file.is_file() and entry_file.suffix == '.md':  # To be extra cautious, ensure this is a file before opening and the file type is md.
                            # To see which file has encoding problem
                            try:
                                with open(entry_file, 'r', encoding='utf-8') as f:
                                    lines = f.readlines()
                                    for line_no, line in enumerate(lines, start=1):
                                        if search_str in line:
                                            # If the string is found, add the file name and line number to the list
                                            matched_entries.append((entry_file, line_no, line.strip()))
                            except UnicodeDecodeError:
                                print(f"Encoding issue detected in file: {entry_file}")

                        # if entry_file.is_file():  # To be extra cautious, ensure this is a file before opening
                        #     # rest of your code...
                        #     # Open the diary file and search for the given string
                        #     with open(entry_file, "r") as f:
                        #         lines = f.readlines()
                        #         for line_no, line in enumerate(lines, start=1):
                        #             if search_str in line:
                        #                 # If the string is found, add the file name and line number to the list
                        #                 matched_entries.append((entry_file, line_no, line.strip()))

    # Display the matched entries
    if not matched_entries:
        print(f"No entries found for '{search_str}'")
        return

    for entry_file, line_no, line in matched_entries:
        print(f"{entry_file.name} (Line {line_no}): {line}")


def main():
    args = sys.argv[1:]
    if not args:
        edit_entry()
    elif args[0] == "cat":
        cat_entry()
    elif args[0] == "find" and len(args) > 1:  # Check if "find" command is used and a string is given to search
        find_entry(args[1])
    else:
       edit_entry(parse_date(args[0]))


if __name__ == "__main__":
    main()
