#!/usr/bin/env python3
import re
import sys

def is_likely_css(text):
    stripped = text.strip()
    # New exception: skip nodes that are just '*/'
    if stripped == "*/":
        return True
    # Heuristics to detect CSS patterns.
    if stripped.startswith("/*!") or stripped.startswith("/*"):
        return True
    if "{" in stripped and "}" in stripped and ":" in stripped:
        return True
    return False

def wrap_text_with_trans(text):
    stripped = text.strip()
    if not stripped:
        return text
    if is_likely_css(text):
        return text
    # Preserve leading/trailing whitespace.
    leading = text[:len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()):]
    return f'{leading}{{% trans "{stripped}" %}}{trailing}'

def process_template(template):
    # Split by Django template tags so they remain intact.
    parts = re.split(r'(\{%.*?%\}|{{.*?}})', template, flags=re.DOTALL)
    new_parts = []
    for part in parts:
        if part.startswith('{%') or part.startswith('{{'):
            new_parts.append(part)
        else:
            # Further split by HTML tags to avoid wrapping HTML markup.
            sub_parts = re.split(r'(<[^>]+>)', part)
            new_sub_parts = []
            for sub in sub_parts:
                if sub.startswith('<'):
                    new_sub_parts.append(sub)
                else:
                    new_sub_parts.append(wrap_text_with_trans(sub))
            new_parts.append(''.join(new_sub_parts))
    return ''.join(new_parts)

def gather_text_nodes(template):
    parts = re.split(r'(\{%.*?%\}|{{.*?}})', template, flags=re.DOTALL)
    text_nodes = []
    for part in parts:
        if part.startswith('{%') or part.startswith('{{'):
            continue
        else:
            sub_parts = re.split(r'(<[^>]+>)', part)
            for sub in sub_parts:
                if sub.startswith('<'):
                    continue
                else:
                    if sub.strip() and not is_likely_css(sub):
                        text_nodes.append(sub.strip())
    return text_nodes

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python add_trans_tags.py template_file.html")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            template = f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    # Gather and display text nodes before processing.
    text_nodes = gather_text_nodes(template)
    if text_nodes:
        print("The following text nodes were found:")
        for node in text_nodes:
            print(f"Text node found: '{node}'")
    else:
        print("No text nodes found for translation.")

    # Ask for confirmation before proceeding.
    proceed = input("Do you want to proceed with adding {% trans %} tags to these text nodes? (y/N): ")
    if proceed.lower() != 'y':
        print("Operation cancelled by user.")
        sys.exit(0)

    processed = process_template(template)
    output_filename = filename + ".i18n"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(processed)
        print(f"Processed template saved to {output_filename}")
    except Exception as e:
        print(f"Error writing to file '{output_filename}': {e}")
        sys.exit(1)
