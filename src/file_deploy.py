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
    for content in os.path.join(path, *dir_content):
        if os.path.isfile(content):
            print(f"Coping file: {content}")
            shutil.copy(content, destination)
        else:
            print(f"Encounter dir {content}")
            copy_dir_content(
                os.path.join(path, content),
                os.path.join(destination, content)
            )

