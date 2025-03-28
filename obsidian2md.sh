#!/usr/bin/env python3
"""Converts Obsidian-flavored markdown (wikilinks, image embeds, etc) into a
more standard markdown format that pandoc can convert.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

def preprocess_obsidian_md(input_path, output_path, image_dir="attachments"):
    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Convert ==highlight== to <mark>...</mark>
    text = re.sub(r'==(.+?)==', r'<mark>\1</mark>', text)

    # 2. Convert ![[image.png]] to ![](attachments/image.png)
    text = re.sub(r'!\[\[([^\]]+)\]\]', rf'![]({image_dir}/\1)', text)

    # 3. Decode %20 and other URL encodings in image paths
    text = re.sub(r'!\[]\(([^)]+)\)', lambda m: f'![]({unquote(m.group(1))})', text)

    # 4. Convert [[#heading]] to [heading](#heading)
    text = re.sub(r'\[\[#([^\]]+)\]\]', r'[\1](#\1)', text)

    # 5. Convert [[Some Page]] to [Some Page](Some-Page.md) as a fallback
    text = re.sub(r'\[\[([^\]]+?)\]\]', lambda m: f"[{m.group(1)}]({m.group(1).replace(' ', '-')}.md)", text)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"Preprocessed Markdown saved to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python obsidian_to_pandoc.py input.md output.md")
        sys.exit(1)

    input_md = Path(sys.argv[1])
    output_md = Path(sys.argv[2])
    preprocess_obsidian_md(input_md, output_md)
