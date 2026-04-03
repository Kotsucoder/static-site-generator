from markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node
import os
import shutil


def main() -> None:
    """
    Main entry point for the program.
    """

    copy_contents("static", "public")
    generate_page("content", "template.html", "public")


def copy_contents(source: str, destination: str) -> None:
    """
    Copies the contents between two given directories.

    Args:
        source: A string representing the directory to copy.
        destination: A string representing where to copy the files. WARNING: Any files that already exist here will be deleted.
    """

    print(f"Source is set to {source}, and destination is set to {destination}.")
    if os.path.exists(source) and not os.path.isfile(source) and not os.path.isfile(destination):
        if os.path.exists(destination):
            print(f"Deleting the contents of {destination}.")
            shutil.rmtree(destination)
        else:
            print(f"Creating {destination}.")
        os.mkdir(destination)
        tree = os.listdir(source)
        print(f"Files in {source} to copy:")
        print(tree)
        for file in tree:
            working_file = os.path.join(source, file)
            if os.path.isfile(working_file):
                new_file = os.path.join(destination, file)
                print(f"Copying {working_file} to {new_file}.")
                shutil.copy(working_file, new_file)
            else:
                new_dir = os.path.join(destination, file)
                print(f"Directory detected. Entering {new_dir}.")
                copy_contents(working_file, new_dir)
    else:
        raise ValueError("Invalid path")
    

def extract_title(markdown: str) -> str:
    """
    Extracts the first heading-1 line in the markdown string as the title.

    Args:
        markdown: The markdown string.

    Returns:
        str: Title extracted from the markdown.
    """

    blocks = markdown_to_blocks(markdown)
    title = None
    for block in blocks:
        blocktype = block_to_block_type(block)
        if blocktype == BlockType.HEADING:
            if block[1] != "#":
                title = block[1:]
                title = title.strip()
                return title
    raise ValueError("Markdown file must contain a header.")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Generates HTML documents from Markdown files using a HTML template.

    Args:
        from_path: The path to the directory containing the Markdown files to render as a string.
        template_path: The path to the HTML template to base the file result on as a string.
        dest_path: The path where the final rendered HTML pages go as a string.
    """

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if os.path.exists(from_path) and os.path.isdir(from_path):
        files = os.listdir(from_path)
        print(files)
        for page in files:
            full_from_path = os.path.join(from_path, page)
            full_dest_path = os.path.join(dest_path, page)
            if not os.path.isfile(full_from_path):
                os.mkdir(full_dest_path)
                generate_page(full_from_path, template_path, full_dest_path)
                continue
            with open(full_from_path, "r") as file:
                markdown_file = file.read()
            with open(template_path, "r") as file:
                template_file = file.read()
            html_page = markdown_to_html_node(markdown_file).to_html()
            title = extract_title(markdown_file)
            template_file = template_file.replace("{{ Title }}", title)
            template_file = template_file.replace("{{ Content }}", html_page)
            with open(os.path.join(dest_path, page.replace(".md", ".html")), "w") as file:
                file.write(template_file)


if __name__ == "__main__":
    main()