import os
from shutil import ExecError
from text_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    if not markdown.strip().startswith("# "):
        raise Exception("Markdown must start with h1 header.")
    title = markdown.strip().splitlines()[0].split(" ", maxsplit=1)[1].strip() 

    return title


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    if not os.path.exists(from_path):
        raise ValueError(f"{from_path} does not exists")
    if not os.path.exists(template_path):
        raise ValueError(f"{template_path} does not exists")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    directories = os.path.dirname(dest_path)
    os.makedirs(directories, exist_ok=True)
    with open(dest_path, mode="wt") as f:
        _ = f.write(full_html)

