#!/usr/bin/env python3

from bs4 import BeautifulSoup
import re

# Read your HTML file
with open('input.html', 'r', encoding='utf-8') as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all headings h1-h6
headings = soup.find_all(re.compile('^h[1-6]$'))
toc_entries = []
id_counts = {}

for heading in headings:
    level = int(heading.name[1])
    text = heading.get_text().strip()

    # Create a safe id by lowercasing, removing non-alphanumerics, and replacing spaces
    base_id = re.sub(r'\s+', '-', re.sub(r'[^a-zA-Z0-9\s]', '', text.lower()))
    # Ensure unique id
    count = id_counts.get(base_id, 0)
    if count:
        unique_id = f"{base_id}-{count}"
    else:
        unique_id = base_id
    id_counts[base_id] = count + 1

    # Add the id attribute to the heading
    heading['id'] = unique_id

    # Append to TOC list with level, text, and id
    toc_entries.append({'level': level, 'text': text, 'id': unique_id})

# Build nested unordered list for TOC
toc_html = ""
prev_level = 0

for entry in toc_entries:
    level = entry['level']
    if level > prev_level:
        toc_html += "<ul>" * (level - prev_level)
    elif level < prev_level:
        toc_html += "</li>" + ("</ul></li>" * (prev_level - level))
    else:
        toc_html += "</li>"
    toc_html += f'<li><a href="#{entry["id"]}">{entry["text"]}</a>'
    prev_level = level

# Close any open tags
toc_html += "</li>" + ("</ul></li>" * (prev_level - 1)) + "</ul>"

# Optionally, insert TOC at a specific location, e.g. before the first heading:
first_heading = soup.find(re.compile('^h[1-6]$'))
toc_soup = BeautifulSoup(toc_html, 'html.parser')
if first_heading:
    first_heading.insert_before(toc_soup)

# Write the modified HTML back to file
with open('output.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
