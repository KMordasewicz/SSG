import os
from file_deploy import delete_dir_content, copy_dir_content
from page_generator import generate_pages_recursive



def main() -> None:
    cwd = os.getcwd()
    if os.path.basename(cwd) != "SSG":
        raise Exception("Main can be run only from project root directory.")
    public_path = cwd + "/public"
    static_path = cwd + "/static"
    delete_dir_content(public_path)
    copy_dir_content(static_path, public_path)
    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
