# Static Site Generator

A Python-based static site generator built from scratch, converting Markdown to static HTML. Created while completing Boot.dev's guided project covering Object-Oriented Programming (OOP), recursion, and content rendering pipelines.

## Features

- **Markdown to HTML Conversion**: Parses Markdown files and converts them to HTML using custom parsing logic
- **Template System**: Uses HTML templates with placeholders for title and content
- **Recursive Directory Processing**: Handles nested directory structures for organizing content
- **Static Asset Copying**: Automatically copies CSS, images, and other static files
- **Base Path Support**: Configurable base paths for deployment in subdirectories
- **Custom HTML Node System**: Implements a tree-based HTML generation system with classes like `HTMLNode` and `TextNode`

## Project Structure

```
static-site-generator/
├── src/                    # Source code
│   ├── main.py            # Main generator script
│   ├── htmlnode.py        # HTML node classes
│   ├── textnode.py        # Text node classes
│   ├── markdown.py        # Markdown parsing logic
│   └── test_*.py          # Unit tests
├── content/               # Markdown source files
├── static/                # Static assets (CSS, images)
├── docs/                  # Generated HTML output
├── template.html          # HTML template
├── build.sh              # Build script
├── main.sh               # Run script with local server
├── test.sh               # Test runner
└── README.md             # This file
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kotsucoder/static-site-generator.git
   cd static-site-generator
   ```

2. Ensure Python 3.13+ is installed

## Usage

### Building the Site

Run the build script to generate the static site:

```bash
./build.sh
```

This will:
- Copy static assets from `static/` to `docs/`
- Convert all Markdown files in `content/` to HTML
- Generate the complete site in the `docs/` directory

### Running Locally

To build and serve the site locally:

```bash
./main.sh
```

This starts a local HTTP server on port 8888.

### Manual Execution

You can also run the generator directly:

```bash
python3.13 src/main.py [basepath]
```

Where `basepath` is optional and defaults to `/`. Use a basepath like `/my-site/` when deploying to a subdirectory.

## Testing

Run the test suite:

```bash
./test.sh
```

Or manually:

```bash
python3.13 -m unittest discover -s src
```

## Key Components

### HTML Node System (`htmlnode.py`, `textnode.py`)
- `HTMLNode`: Represents HTML elements with tags, attributes, and children
- `TextNode`: Represents text content within HTML elements
- Tree-based structure for building and rendering HTML

### Markdown Parser (`markdown.py`)
- Converts Markdown to HTML nodes
- Supports headings, paragraphs, lists, links, images, and code blocks
- Block-level and inline element parsing

### Main Generator (`main.py`)
- Orchestrates the site generation process
- Recursively processes directories
- Extracts titles from Markdown headers
- Applies templates and handles base paths

## Learning Outcomes

This project demonstrates:
- Object-oriented design principles
- Recursive algorithms for directory traversal
- String parsing and manipulation
- File system operations in Python
- Unit testing with Python's `unittest` framework
- Command-line argument handling

## Contributing

This is a learning project from Boot.dev. Feel free to fork and experiment, but it's primarily for educational purposes.
