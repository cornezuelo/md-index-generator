# md-index-generator

A simple script to generate a hierarchical, indented Markdown table of contents with GitHub-style anchor links.

---

## 🔧 Requirements

- Python 3.7+
- No external dependencies

---

## 🚀 Usage

```bash
python generate.py path/to/your_file.md
```

This will print a Markdown index like:

- 🧠 [Introduction](#introduction)
  - 🧪 [Basics](#basics)
    - 💡 [Example](#example)

---

## ⚙️ Options

| Option          | Description                                               |
|-----------------|-----------------------------------------------------------|
| `--base-level`  | Set the heading level to start indexing from (`#` = 1)    |
| `--numbered`    | Add hierarchical numbers before the title (`1.1.`, etc.)  |
| `--no-links`    | Output plain text (no `[link](#anchor)`)                  |

---

## ℹ️ About slugs and links

- Slugs mimic GitHub behavior.
- Accents and special characters are preserved:  
  `"Introducción"` → `#introducción` (not `#introduccion`)
- Spaces are replaced with hyphens.
- No punctuation is stripped unless invalid for anchors.

---

## 💡 Automatic emoji handling

If a heading starts with an emoji (e.g. `🧠 Introduction`), it is automatically moved **outside the link** to avoid rendering glitches on GitHub.

### ❌ Problematic:

```markdown
- [🧠 Introduction](#introduction)
```

### ✅ Handled automatically as:

```markdown
- 🧠 [Introduction](#introduction)
```

---

## 📄 Example

### Markdown input:

```markdown
# Project Title

## Getting Started

### Installation

### Usage
```

### Command:

```bash
python generate.py doc.md --base-level 2 --numbered
```

### Output:

- 1· 📦 [Getting Started](#getting-started)
  - 1.1· 🔧 [Installation](#installation)
  - 1.2· 🚀 [Usage](#usage)

---

## 🧠 What it does

- Parses headings from `#` to `######`
- Builds an indented list using `-` with proper nesting
- Slugs are compatible with GitHub (preserve accents)
- Detects and moves emojis outside of links for safe rendering
- Adds hierarchical numbers with `--numbered`
- Disables links with `--no-links`
- Skips headings above the `--base-level`
- Output is printed to the terminal
- Does **not** modify the original file

---

## 📌 Notes

- Output can be copy-pasted into any Markdown document
- Fully compatible with GitHub-flavored Markdown (GFM)

---

## 📝 License

MIT License