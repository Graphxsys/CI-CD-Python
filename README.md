# PyBase

A minimal, Python repository template with .gitignore, .vscode extensions, code formatter and linter.

<p align="center">
  <img src="https://s3.dualstack.us-east-2.amazonaws.com/pythondotorg-assets/media/community/logos/python-logo-only.png" alt="Python Logo" height="100">
  &nbsp; &nbsp; &nbsp; &nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Visual_Studio_Code_1.35_icon.svg/480px-Visual_Studio_Code_1.35_icon.svg.png" alt="VS Code Logo" height="100">
</p>

## VS Code Configuration for Python Development

This repo includes a recommended set of VS Code extensions and settings to enhance Python development.

## 📦 Recommended Extensions

To ensure a smooth development experience, install the following extensions by adding them to your `.vscode/extensions.json` file:

```json
{
  "recommendations": [
    "ms-python.isort", // Sorts Python imports automatically
    "ms-python.flake8", // Linter for enforcing code quality
    "ms-python.python", // Core Python extension for VS Code
    "ms-python.pylint", // Another Python linter
    "ms-python.debugpy", // Debugging support for Python
    "yzane.markdown-pdf", // Converts Markdown to PDF
    "ms-toolsai.jupyter", // Jupyter Notebook support
    "qwtel.sqlite-viewer", // View SQLite databases
    "ritwickdey.liveserver", // Live server for web development
    "ms-python.vscode-pylance", // Python language server
    "ms-toolsai.jupyter-keymap", // Key bindings for Jupyter
    "ms-python.black-formatter", // Black code formatter
    "ms-toolsai.jupyter-renderers", // Jupyter notebook renderers
    "ms-toolsai.vscode-jupyter-slideshow", // Jupyter slideshow support
    "ms-toolsai.vscode-jupyter-cell-tags" // Jupyter cell tagging
  ]
}
```

## ⚙️ VS Code Settings

To maintain consistent formatting and linting, use the following settings in `.vscode/settings.json`:

```json
{
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter", // Use Black for formatting
    "editor.formatOnSave": true // Auto-format on save
  },
  "black-formatter.args": ["--line-length", "200"],
  "flake8.args": ["--max-line-length=200"],
  "pylint.args": ["--max-line-length=200"],
  "editor.formatOnSave": true,
  "editor.formatOnPaste": true,
  "diffEditor.codeLens": true, // Show inline code lens in diff view
  "editor.codeActionWidget.includeNearbyQuickFixes": true // Enable quick fixes
}
```

---

This setup ensures consistent formatting, efficient linting, and an improved development workflow. 🚀
