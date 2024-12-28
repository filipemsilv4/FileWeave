# FileWeave: Simplifying Codebase Sharing for LLM Interaction

## Overview

FileWeave is a desktop application designed to simplify the process of sharing your project's codebase with Large Language Models (LLMs). Instead of manually copying and pasting code from multiple files, FileWeave allows you to selectively combine them into a single, well-structured output, making it easier to provide context to LLMs for Q\&A or initial project understanding. It's built with Python using the `tkinter` library for the GUI and integrates with your project's `.gitignore` file.

## Motivation

When interacting with LLMs about your codebase, providing them with a broad, initial view of your project can be highly beneficial. This allows the LLM to grasp the overall structure, identify key components, and answer questions more effectively without you having to constantly guide it through individual files.

However, manually preparing a comprehensive snapshot of your project for an LLM can be time-consuming. FileWeave aims to streamline this process by enabling you to:

1. **Navigate** your project's directory structure.
2. **Select** relevant files for inclusion.
3. **Filter** out irrelevant files using `.gitignore` or by hiding/showing hidden files.
4. **Generate** a single, concatenated output that you can directly paste into an LLM's input.
5. **Copy** the output to your clipboard.

By automating these steps, FileWeave reduces the initial effort required to onboard an LLM to your project, allowing for a more efficient and productive interaction.

## Features

* **Intuitive GUI:** A simple interface built with `tkinter`.
* **Directory Navigation:** Easily browse your project's files and folders.
* **File Selection:** Select files to include using checkboxes.
* **.gitignore Integration:** Respects your project's `.gitignore` to exclude unwanted files.
* **Show/Hide Hidden Files:** Toggle visibility of hidden files (files starting with a dot).
* **Formatted Output:** Generates output with:
  * Clear file separators using Markdown code blocks (e.g., ``` # project_name/path/to/file.py ... ```).
  * Language identifier within the code blocks for better LLM understanding.
* **Clipboard Integration:** Copy the output directly to your clipboard.
* **Cross-Platform:** Should work on macOS, Windows, and Linux.
* **Convenient Shortcuts:** Use ⌘O (Ctrl+O on Windows/Linux) to open a directory and ⌘C (Ctrl+C on Windows/Linux) to copy the output.

## Installation

This project uses Poetry for dependency management. To get started:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/filipemsilv4/fileweave.git
    cd fileweave
    ```

2. **Install dependencies using Poetry:**

    ```bash
    poetry install
    ```

3. **Run the application:**

    ```bash
    poetry run python fileweave/main.py
    ```

## Usage

1. Launch the application.
2. Click "Select Directory" to choose your project's root directory.
3. Select the files you want to include.
4. Optionally, toggle "Respect .gitignore" or "Show hidden files".
5. Click "Generate Output" to create the combined code output.
6. Click "Copy to Clipboard" to copy the output for use with an LLM.

## Contributing

Contributions are welcome! For suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Acknowledgments

* Uses the `pathspec` library for parsing `.gitignore` files.
