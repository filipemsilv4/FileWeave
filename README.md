# FileWeave: Your Bridge Between Codebase and LLMs

[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/filipemsilv4/fileweave/blob/master/README.md)
[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/filipemsilv4/fileweave/blob/master/README.pt-br.md)

Ever wished you could seamlessly share your entire codebase with an LLM? FileWeave makes it possible. This desktop application transforms the tedious process of copying multiple files from your codebase into a smooth operation. Built with Python and tkinter, FileWeave helps you create perfectly formatted code snapshots that LLMs can easily understand and analyze.

<img width="1391" alt="Screenshot 2024-12-27 at 23 48 56" src="https://github.com/user-attachments/assets/ad26dd50-29b0-45d7-a0ff-ae60dfd7a622" />

## Why FileWeave?

Modern LLMs like **Gemini** excel at understanding complex codebases - when they can see the big picture. But preparing that overview has traditionally meant tedious copy-pasting from dozens of files. FileWeave transforms this process into a simple point-and-click operation.

With FileWeave, you can:
- Navigate your project structure with ease
- Cherry-pick the files you want to include
- Automatically filter out irrelevant files using `.gitignore` rules
- Generate a perfectly formatted output ready for your LLM
- Copy everything to your clipboard with a single click

The result? You spend less time preparing code for review and more time getting valuable insights from your LLM.

## Key Features

FileWeave combines power with simplicity:

- **Smart Interface**: A clean, intuitive GUI built with tkinter
- **Intelligent Filtering**: Seamless integration with your `.gitignore` rules
- **Hidden File Control**: Toggle visibility of dot files with a single click
- **LLM-Optimized Output**: Generates markdown code blocks with language identifiers and clear file separators
- **Cross-Platform Support**: Works on macOS, Windows, and Linux
- **Keyboard Shortcuts**: Quick access with ⌘O/Ctrl+O for directory selection and ⌘C/Ctrl+C for copying

## Getting Started

FileWeave uses Poetry for dependency management. Here's how to get up and running:

1. **Install Poetry** (if you haven't already):
   Visit the [Poetry documentation](https://python-poetry.org/docs/#installation) for detailed instructions.

2. **Set up FileWeave**:
   ```bash
   git clone https://github.com/filipemsilv4/fileweave.git
   cd fileweave
   poetry install
   ```

3. **Launch the application**:
   ```bash
   poetry run python fileweave/main.py
   ```

## Using FileWeave

1. Launch FileWeave
2. Select your project's root directory
3. Adjust visibility settings if needed
4. Choose the files you want to include
5. Generate your combined output
6. Copy to clipboard and share with your LLM

## Join the Community

Your contributions can make FileWeave even better! Whether you've found a bug, have a feature request, or want to contribute code, we welcome your input through issues and pull requests.

## License

FileWeave is available under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

Special thanks to the `pathspec` library for powering our `.gitignore` parsing capabilities.
