import sys
import os
from file_deploy import delete_dir_content, copy_dir_content
from page_generator import generate_pages_recursive



def main() -> None:
    input = sys.argv
    if len(input) != 2:
        basepath = "/"
    else:
        basepath = input[1]
    cwd = os.getcwd()
    public_path = cwd + "/docs"
    static_path = cwd + "/static"
    delete_dir_content(public_path)
    copy_dir_content(static_path, public_path)
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
