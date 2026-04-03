from textnode import TextType, TextNode, split_nodes_delimiter, text_node_to_html_node
from htmlnode import HTMLNode, LeafNode
import os
import shutil


def main() -> None:
    """
    Main entry point for the program.
    """
    copy_contents("static", "public")


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


if __name__ == "__main__":
    main()