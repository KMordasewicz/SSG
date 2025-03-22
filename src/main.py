import os
from signal import raise_signal
from file_deploy import delete_dir_content, copy_dir_content



def main() -> None:
    cwd = os.getcwd()
    if os.path.basename(cwd) != "SSG":
        raise Exception("Main can be run only from project root directory.")
    public_path = cwd + "/public"
    static_path = cwd + "/static"
    delete_dir_content(public_path)
    copy_dir_content(static_path, public_path)

if __name__ == "__main__":
    main()
