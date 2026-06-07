#!/usr/bin/env python3
"""Generate an interactive index.html for Rep*.png images in this directory."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


def make_id(filename: str) -> str:
    """Create a stable anchor id from a filename."""
    slug = re.sub(r"[^a-z0-9]+", "-", filename.lower()).strip("-")
    return slug or "image"


def display_label(filename: str) -> str:
    """Return a short display label from Repository_<repo_id>_... filenames."""
    parts = filename.split("_")
    if len(parts) > 1 and parts[1]:
        return parts[1]
    return filename


def build_html(image_names: list[str], page_title: str) -> str:
    options = []
    toc_items = []
    sections = []

    for name in image_names:
        safe_name = html.escape(name)
        anchor = make_id(name)
        short_label = html.escape(display_label(name))

        options.append(
            f'          <option value="{anchor}" title="{safe_name}">{short_label}</option>'
        )
        toc_items.append(
            f'        <li><a href="#{anchor}" title="{safe_name}">{short_label}</a></li>'
        )

        sections.append(
            "\n".join(
                [
                    f'    <section id="{anchor}">',
                    f'      <h3><a href="{safe_name}" title="{safe_name}">{short_label}</a></h3>',
                    f'      <img src="{safe_name}" alt="{safe_name}">',
                    '      <a class="top-link" href="#page-top">Back to top</a>',
                    "    </section>",
                ]
            )
        )

    return "\n".join(
        [
            "<!DOCTYPE html>",
            '<html lang="en">',
            "<head>",
            '  <meta charset="UTF-8">',
            '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            f"  <title>{html.escape(page_title)}</title>",
            "  <style>",
            "    :root {",
            "      color-scheme: light;",
            "      --bg: #f5f7fa;",
            "      --panel: #ffffff;",
            "      --text: #1f2933;",
            "      --muted: #52606d;",
            "      --border: #d9e2ec;",
            "      --accent: #1f4e79;",
            "    }",
            "",
            "    html {",
            "      scroll-behavior: smooth;",
            "    }",
            "",
            "    body {",
            "      margin: 0;",
            "      font-family: Georgia, \"Times New Roman\", serif;",
            "      background: var(--bg);",
            "      color: var(--text);",
            "    }",
            "",
            "    header {",
            "      position: sticky;",
            "      top: 0;",
            "      z-index: 10;",
            "      padding: 20px 24px;",
            "      background: rgba(245, 247, 250, 0.96);",
            "      border-bottom: 1px solid var(--border);",
            "      backdrop-filter: blur(8px);",
            "    }",
            "",
            "    h1 {",
            "      margin: 0 0 8px;",
            "      font-size: 28px;",
            "      color: var(--accent);",
            "    }",
            "",
            "    p {",
            "      margin: 0;",
            "      color: var(--muted);",
            "      font-size: 15px;",
            "    }",
            "",
            "    main {",
            "      max-width: 1200px;",
            "      margin: 0 auto;",
            "      padding: 24px;",
            "    }",
            "",
            "    nav,",
            "    .selector {",
            "      margin-bottom: 28px;",
            "      padding: 18px;",
            "      background: var(--panel);",
            "      border: 1px solid var(--border);",
            "      border-radius: 12px;",
            "      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);",
            "    }",
            "",
            "    nav h2,",
            "    .selector h2 {",
            "      margin: 0 0 12px;",
            "      font-size: 20px;",
            "      color: var(--accent);",
            "    }",
            "",
            "    nav ul {",
            "      margin: 0;",
            "      padding-left: 18px;",
            "      column-width: 320px;",
            "      column-gap: 24px;",
            "    }",
            "",
            "    nav li {",
            "      margin-bottom: 6px;",
            "      break-inside: avoid;",
            "      word-break: break-word;",
            "    }",
            "",
            "    .selector-controls {",
            "      display: flex;",
            "      flex-wrap: wrap;",
            "      gap: 10px;",
            "      align-items: center;",
            "    }",
            "",
            "    select,",
            "    button {",
            "      font: inherit;",
            "      font-size: 15px;",
            "      padding: 8px 10px;",
            "      border: 1px solid var(--border);",
            "      border-radius: 8px;",
            "      background: #fff;",
            "      color: var(--text);",
            "    }",
            "",
            "    button {",
            "      cursor: pointer;",
            "      color: #fff;",
            "      background: var(--accent);",
            "      border-color: var(--accent);",
            "    }",
            "",
            "    button:hover {",
            "      filter: brightness(1.05);",
            "    }",
            "",
            "    section {",
            "      margin-bottom: 28px;",
            "      padding: 16px;",
            "      background: var(--panel);",
            "      border: 1px solid var(--border);",
            "      border-radius: 12px;",
            "      box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);",
            "      scroll-margin-top: 160px;",
            "    }",
            "",
            "    h3 {",
            "      margin: 0 0 12px;",
            "      font-size: 20px;",
            "      word-break: break-word;",
            "    }",
            "",
            "    a {",
            "      color: var(--accent);",
            "      text-decoration: none;",
            "    }",
            "",
            "    a:hover {",
            "      text-decoration: underline;",
            "    }",
            "",
            "    .top-link {",
            "      display: inline-block;",
            "      margin-top: 12px;",
            "      font-size: 14px;",
            "      color: var(--muted);",
            "    }",
            "",
            "    img {",
            "      display: block;",
            "      width: 100%;",
            "      height: auto;",
            "      border: 1px solid var(--border);",
            "      border-radius: 8px;",
            "      background: #fff;",
            "    }",
            "",
            "    @media (max-width: 720px) {",
            "      header {",
            "        position: static;",
            "      }",
            "",
            "      section {",
            "        scroll-margin-top: 24px;",
            "      }",
            "",
            "      nav ul {",
            "        column-width: auto;",
            "      }",
            "    }",
            "  </style>",
            "</head>",
            "<body>",
            '  <div id="page-top"></div>',
            "  <header>",
            f"    <h1>{html.escape(page_title)}</h1>",
            "    <p>Interactive index for repository FAIRness history plots generated from files matching Rep*.png.</p>",
            "  </header>",
            "",
            "  <main>",
            '    <div class="selector" aria-label="Image selector">',
            "      <h2>Quick Select</h2>",
            '      <div class="selector-controls">',
            '        <label for="image-picker">Choose an image:</label>',
            '        <select id="image-picker">',
            *options,
            "        </select>",
            '        <button id="jump-button" type="button">Go to image</button>',
            "      </div>",
            "    </div>",
            "",
            "    <nav>",
            "      <h2>Contents</h2>",
            "      <ul>",
            *toc_items,
            "      </ul>",
            "    </nav>",
            "",
            *sections,
            "  </main>",
            "",
            "  <script>",
            '    const picker = document.getElementById("image-picker");',
            '    const jumpButton = document.getElementById("jump-button");',
            "",
            "    function jumpToSelectedImage() {",
            "      const targetId = picker.value;",
            "      const target = document.getElementById(targetId);",
            "      if (target) {",
            '        target.scrollIntoView({ behavior: "smooth", block: "start" });',
            "      }",
            "    }",
            "",
            '    jumpButton.addEventListener("click", jumpToSelectedImage);',
            '    picker.addEventListener("change", jumpToSelectedImage);',
            "  </script>",
            "</body>",
            "</html>",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate index.html from Rep*.png images in a directory"
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing Rep*.png files (default: script directory)",
    )
    parser.add_argument(
        "--title",
        default="Repository FAIRness Time Histories",
        help="Page title and heading",
    )
    args = parser.parse_args()

    image_dir = args.dir.resolve()
    image_names = sorted([p.name for p in image_dir.glob("Repository*.png")], key=str.lower)   # make list of all Repository*.png files in the directory, sorted case-insensitively
    
    timeStamp = '-07T10'
    for i, name in enumerate(image_names):
        if timeStamp not in name:
            continue  # skip files that don't include the timestamp pattern
        new_name = name.replace(timeStamp, '')  # remove the timestamp from the filename
        (image_dir / name).rename(image_dir / new_name)
        image_names[i] = new_name

    if not image_names:
        raise SystemExit(f"No files matching Repository*.png in {image_dir}")

    html_text = build_html(image_names, args.title)
    out_path = image_dir / "index.html"
    out_path.write_text(html_text, encoding="utf-8")

    print(f"Wrote {out_path} with {len(image_names)} images")


if __name__ == "__main__":
    main()
