# Sublime Text – SQF Syntax

Sublime Text syntax highlighting for Bohemia Interactive’s SQF scripting language.

![SQF Syntax Highlighter](http://i.imgur.com/lZdwuIi.png "SQF Syntax Highlighter in action!")

## Installation

### Package Control (recommended)
1. Open Sublime Text.
2. Press `Ctrl`+`Shift`+`P` (or `Cmd`+`Shift`+`P` on macOS) → **Package Control: Install Package**.
3. Search for **SQF Language** and press **Enter**.

### Manual install
Clone into your **Packages** directory:
```bash
git clone https://github.com/JonBons/Sublime-SQF-Language.git "SQF Language"
```

Or add the repo to Package Control:
1. `Ctrl/Cmd`+`Shift`+`P` → **Package Control: Add Repository**
2. Enter `https://github.com/JonBons/Sublime-SQF-Language/`
3. Then use **Install Package** and select **SQF Language**.

## Definition Updates

This repository includes a GitHub Action that checks the upstream SQF/Arma grammar definitions and regenerates artifacts automatically.

- **Schedule:** Every **Saturday at 13:00 UTC** (`0 13 * * 6`).
- If changes are detected, it runs `generate_sqf_template.py` and commits the updated `SQF.tmLanguage` and completions. The commit message includes the upstream version (from [vlad333000/vscode-sqf](https://github.com/vlad333000/vscode-sqf)) and the short commit hash of the upstream change.

## Credits

- **Language definitions:** Generated from the excellent work in [vlad333000/vscode-sqf](https://github.com/vlad333000/vscode-sqf).
  The generator consumes:
  - `sqf.tmLanguage.json`
  - `arma-cfg.tmLanguage.json`

Huge thanks to the maintainers and contributors of that project.

## Contributing

Issues and PRs are welcome! If you’re tweaking keywords or scopes, please include example snippets so I can verify highlighting across common SQF patterns.
