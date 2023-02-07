# coding: UTF-8

# Library by default
import os
# Library by local
from config import get_config
from manipulate import manipulate_bookmeter_html
# Library by third party
import pyperclip as pc
import glob2

BEFORE_HTML = get_config("general_path", "htmls_before")
AFTER_HTML = get_config("general_path", "htmls_after")

def export_file(content : str, file_name_without_ext : str, extension : str, target_dir : str) -> bool:
    is_exported = False
    file_name = f"{file_name_without_ext}.{extension}"
    file_name_abs_path = f"{target_dir}/{file_name}"
    with open(file_name_abs_path, 'x') as f:
        f.write(content)
    is_exported = True
    return is_exported

def get_files(dir : str, is_only_filename : bool = True, is_reversed : bool = False) -> list:
    files = glob2.glob(dir)
    cleansed_files = []
    if is_only_filename:
        for f in files:
            cleansed_files.append(os.path.split(f)[-1])
    else:
        cleansed_files = files
    cleansed_files.sort(key=None, reverse=is_reversed)
    return cleansed_files

def read_file(file : str) -> str:
    content = open(file, 'r')
    return content

def main():
    bookmeter_html = ""

    files_before = get_files(f"./{BEFORE_HTML}/*", True, False)
    files_after = get_files(f"./{AFTER_HTML}/*", True, False)
    yet_files = list(set(files_before) - set(files_after))
    yet_files.sort(key=None, reverse=False)
    for f in yet_files:
        print("======================= File name ===========================")
        print(f"f\n")
        bookmeter_html = read_file(f"./{BEFORE_HTML}/{f}")
        soup = manipulate_bookmeter_html(bookmeter_html)
        print("======================= prettify start ===========================")
        blog_article = soup.prettify()
        print(blog_article)
        export_file(blog_article, f.split(".")[0], "html", AFTER_HTML)

        # pc.copy(blog_article)
        # print("copied to your clipboard!")
        print("======================= prettify end ===========================")


if __name__ == "__main__":
    main()
