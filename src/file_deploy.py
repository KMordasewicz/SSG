import os
import shutil


def delete_dir_content(path: str):
    print(f"Deleting content of {path} directory...")
    shutil.rmtree(path, False)
    print("Content succesfully deleted.")


def copy_dir_content(path: str, destination: str):
    if not os.path.exists(path):
        raise ValueError(f"Given path does not exists: {path}")
    if (not os.path.isdir(destination)) or (not os.path.exists(destination)):
        print(f"Destianation: {destination} is not a file or doesn't exists, creating one...")
        os.mkdir(destination)
    print(f"coping file from {path} to {destination}")
    dir_content = os.listdir(path)
    print(f"Content of {path}: {dir_content}")
    for content in dir_content:
        content_path = os.path.join(path, content)
        print(content_path)
        if os.path.isfile(content_path):
            print(f"Coping file: {content_path}")
            shutil.copy(content_path, destination)
        else:
            print(f"Encounter dir {content}")
            copy_dir_content(
                content_path,
                os.path.join(destination, content)
            )

