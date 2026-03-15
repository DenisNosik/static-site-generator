import os
import shutil
from blocks_markdown import markdown_to_html_node

def generate_destination(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination) # delete destination dir
    os.mkdir(destination)

def copy_all_content_to(source, destination):
    if not os.path.exists(source):
        raise Exception("source doesn't exist")
    for item in os.listdir(source):
        path = os.path.join(source, item)
        if os.path.isfile(path):
            shutil.copy(path, destination)
        else:
            destination_path = os.path.join(destination, item)
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            copy_all_content_to(path, destination_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line.replace("# ", "")
    raise Exception("title was not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f_m:
        md_content = f_m.read()
    with open(template_path, "r") as f_t:
        template = f_t.read()
    node = markdown_to_html_node(md_content)
    html_content = node.to_html()
    title = extract_title(md_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w") as f_d:
        f_d.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(item_path, template_path, dest_path)
        else:
            generate_pages_recursive(item_path, template_path, dest_path)
 
def main():
    generate_destination("public")
    copy_all_content_to("static", "public")

    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()
