#!/usr/bin/env python3
"""Generate an interactive index.html for Rep*.png images in this directory."""

from __future__ import annotations

import argparse
import html
import re
import pandas as pd
from tabulate import tabulate
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

def makeRepositoryRangeTable(rangeLimit=0.15):

    rangeFile = 'longTermRepositoryFairUseCasesByYearRange.csv'
    range_df = pd.read_csv(rangeFile)
    range_df = range_df[['Repository Name', 'Total']]
    range_df = range_df.rename(columns={'Total': 'Range'})

    for i in range(len(range_df)):
        m = re.search(r"\(([^()]*)\)$", range_df['Repository Name'].iloc[i])
        if m:
            rep_id = m.group(1)
            range_df.at[i, 'Repository Name'] = range_df.at[i, 'Repository Name'].replace(rep_id,f'<a href="#repository-{rep_id.replace(".","-")}-time-history-2026-06-png" title="Repository_{rep_id}_Time_History_2026-06.png">{rep_id}</a>')

    table_df = makeSquishedTable(range_df[range_df['Range'] >= rangeLimit], 3, False)
    return table_df

def makeSquishedTable(df, numberOfSets=2, transpose=True):
    '''
        This function takes a dataframe and returns a dataframe with long rows 
        compressed into columns. This is used to convert a spiral results table
        with 25 columns in two rows intof a table with seven rows and eight columns
        (numberOfSets = 4). The squishing makes it possible to include the table 
        in a report with portrait orientation
        
        Args:
            df (dataframe): The dataframe to be squished
            numberOfSets (int, default = 2): The number of sets of columns

        Attributes:

        Returns:
            table_df (dataframe): The squished dataframe

        Notes:
    '''
    if transpose:
        df_t    = df.transpose()                                       # transpose the dataframe so that concepts are rows instead of columns
    else:
        df_t    = df

    for i in range(len(df_t)):                                     # convert floats to % in Scores
        if isinstance(df_t.iloc[i,1], float):
                df_t.iloc[i,1] = f'{df_t.iloc[i,1]:.0%}'

    if transpose == True:
        if len(df.columns) / numberOfSets == int(len(df.columns) / numberOfSets):   # calculate the number of rows per set, rounding up if necessary
            rowsPerSet = int(len(df.columns) / numberOfSets)
        else:
            rowsPerSet = int(len(df.columns) / numberOfSets) + 1
    else:
        rowsPerSet = int(len(df) / numberOfSets) + 1

    table_df = pd.DataFrame()
    i = 0
    col = []

    while i < len(df_t):
        j = i + rowsPerSet
        df_i = df_t.iloc[i:j]
        df_i.reset_index(inplace=True, drop=True)
        table_df = pd.concat([table_df, df_i], axis=1, ignore_index=True)
        if transpose == True:
            col.extend(['Concept', 'Score'])
        else:
            col.extend(df.columns)
        i += rowsPerSet

    table_df.columns = col
    return table_df.fillna('')

def build_html(image_names: list[str], page_title: str, range_html: str) -> str:
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
            "      font-family: 'Century Gothic', CenturyGothic, AppleGothic, gothic, Arial, Helvetica, sans-serif;",
            "      font-size: medium;",
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
            f"    <h1>{page_title}</h1>",
            f"    <p>{page_description}</p>",
            '    <p>&nbsp;</p>',
            f"    <p>{page_additional_info}</p>",
            '    <p>&nbsp;</p>',
            f"    <p>{page_fairness_info}</p>",
            '    <p>&nbsp;</p>',
            f"    <p>{page_gallery_info}</p>",
            "  </header>",
            "",
            
            "  <main>",
            "<h2>Check the <a href=\"https://bit.ly/FAIRUseCasesForDataCite\">Radar Plot Key</a> for more information about the use cases and how to interpret the plots.</h2>",
            '    <div class="selector" aria-label="Image selector">',
            "      <h2>Use Quick Select if you know the repository id.</h2>",
            '      <div class="selector-controls">',
            '        <label for="image-picker">Choose an image:</label>',
            '        <select id="image-picker">',
            *options,
            "        </select>",
            '        <button id="jump-button" type="button">Go to image</button>',
            "      </div>",
            "    </div>",
            "",
                    "<nav>"
                    "<h2>Repository FAIRness Ranges</h2>",
                    "<p>Repositories with FAIRness range of 15% or more over ten years are shown in the table below. Click on a repository identifier to jump to its time history.</p>",
                    "<p>&nbsp;</p>",
                    f"{range_html}",
                    "</nav>",

    
            "    <nav>",
            "      <h2>Contents</h2>",
            "      <p>Click on a repository identifier to jump to its time history.</p>",
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

page_description = """The FAIR Principles were proposed a decade ago to guide the management and stewardship of scientific data. Version 4.0 of the DataCite metadata schema was released during the same year.
    The schema continues to evolve to support the FAIR principles and <a href="https://doi.org/10.59350/wgret-2kd02">other emergent metadata needs</a>."""
page_additional_info = """Almost 600 DataCite repositories have been creating DOIs since 2017. We determined yearly FAIRness of those repositories using the same 
    tools used for recognizing <a href="https://doi.org/10.59350/v2may-69s52">several kinds of bright spots</a>.
    We measured the range of completeness (max-min) over ten years to find repositories that had become more FAIR. This page shows yearly time histories for these 
    repositories as radar plots for each of four use cases (Text, Identifiers, Connections, and Contacts). Each use case is a row with yearly columns. Yearly Total FAIRness is shown in parentheses
    in the column titles and yearly scores for each use case are shown below the radar plots. Metadata completeness is visually represented by the radar plot areas. Increases in completeness 
    are reflected by radar plots filling up. Check the <a href="https://bit.ly/FAIRUseCasesForDataCite">Radar Plot Key</a> for more information about the use cases and how to interpret the plots."""
page_fairness_info = """ These data show that FAIRness can be achieved in many ways and that improvements occur in different patterns. In some cases they happen simultaneously over several use cases, 
    in others they happen in distinct steps, reflecting different strategies and priorities. FAIRness is not a destination but a journey. We hope these data will inspire and guide 
    others on their own FAIRness journeys. We also hope they will encourage repository managers to share their own strategies and successes."""
page_gallery_info = """This gallery includes repositories that have been <i>active in DataCite since at least 2017 and have changed overall FAIRness by 15% or more.</i> 
    The data can be browsed by scrolling through the images or repositories can be selected using the quick select dropdown, the Table organized by Range, or the alphabetical list. The complete data are available at <a href="https://doi.org/10.5281/zenodo.20617483">https://doi.org/10.5281/zenodo.20617483</a> and a notebook that reproduces the analysis and figures is available at <a href="https://bit.ly/DataCiteBecomingBright">https://bit.ly/DataCiteBecomingBright</a>. 
    <br><br>We hope this gallery will inspire and guide repository managers on their own FAIRness journeys and encourage them to share their own strategies and successes.
    <hr style="height:2px;color:gray;background-color:gray">
    <p>Repository FAIRness Time Histories created June 2026 &copy; by <a href="https://metadatagamechangers.com">Metadata Game Changers</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">CC BY-NC-SA 4.0</a></p>"""

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

    range_df    = makeRepositoryRangeTable()
    range_html  = tabulate(range_df, headers=list(range_df.columns), tablefmt="html", showindex=False)
    range_html = range_html.replace("<table>", '<table style="border-collapse: collapse; border: 1px solid black; width: 100%;">')  # add inline styles for better table appearance
    range_html = range_html.replace("<th>", '<th style="border: 1px solid black; padding: 8px;">')
    range_html = range_html.replace("<td>", '<td style="border: 1px solid black; padding: 8px;">')
    range_html = range_html.replace('<td style="text-align: right;">', '<td style="border: 1px solid black; padding: 8px;">')
    range_html = range_html.replace("&lt;", "<").replace("&gt;", ">").replace("&quot;", '"')  # unescape <, >, and " in the table

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

    html_text = build_html(image_names, args.title, range_html)
    out_path = image_dir / "index.html"
    out_path.write_text(html_text, encoding="utf-8")

    print(f"Wrote {out_path} with {len(image_names)} images")


if __name__ == "__main__":
    main()
