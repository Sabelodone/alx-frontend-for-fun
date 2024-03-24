#!/usr/bin/python3
"""
This is a script to convert a Markdown file to HTML.

Usage:
    ./markdown2html.py [input_file] [output_file]

Arguments:
    input_file: the name of the Markdown file to be converted
    output_file: the name of the output HTML file

Example:
    ./markdown2html.py README.md README.html
"""


import sys
import os
import re
import hashlib

def generate_heading_html(match):
    level = len(match.group(1))
    return f"<h{level}>{match.group(2)}</h{level}>\n"

def generate_unordered_list_html(match):
    items = match.group(1).strip().split('\n')
    html = "<ul>\n"
    for item in items:
        html += f"    <li>{item.strip()}</li>\n"
    html += "</ul>\n"
    return html

def generate_ordered_list_html(match):
    items = match.group(1).strip().split('\n')
    html = "<ol>\n"
    for item in items:
        html += f"    <li>{item.strip()}</li>\n"
    html += "</ol>\n"
    return html

def generate_paragraph_html(match):
    return f"<p>\n    {match.group(1)}\n</p>\n"

def generate_bold_html(match):
    return f"<b>{match.group(1)}</b>"

def generate_emphasis_html(match):
    return f"<em>{match.group(1)}</em>"

def generate_md5_html(match):
    content = match.group(1)
    md5_hash = hashlib.md5(content.encode()).hexdigest()
    return f"{md5_hash}\n"

def remove_c_html(match):
    content = match.group(1)
    return content.replace('c', '')

def main():
    if len(sys.argv) < 3:
        sys.stderr.write("Usage: ./markdown2html.py <input_file> <output_file>\n")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        sys.stderr.write(f"Missing {input_file}\n")
        sys.exit(1)

    with open(input_file, 'r') as f:
        markdown_content = f.read()

    html_content = markdown_content

    # Parse markdown and generate HTML
    html_content = re.sub(r'^#(\#+)\s*(.+)', generate_heading_html, html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^-\s+(.+)', generate_unordered_list_html, html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\*\s+(.+)', generate_ordered_list_html, html_content, flags=re.MULTILINE)
    html_content = re.sub(r'^\n(.+?)\n', generate_paragraph_html, html_content, flags=re.MULTILINE|re.DOTALL)
    html_content = re.sub(r'\*\*(.*?)\*\*', generate_bold_html, html_content)
    html_content = re.sub(r'__(.*?)__', generate_emphasis_html, html_content)
    html_content = re.sub(r'\[\[(.*?)\]\]', generate_md5_html, html_content)
    html_content = re.sub(r'\(\((.*?)\)\)', remove_c_html, html_content)

    with open(output_file, 'w') as f:
        f.write(html_content)

if __name__ == "__main__":
    main()
