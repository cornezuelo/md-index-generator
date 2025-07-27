import re
import sys
import argparse
from pathlib import Path

def github_slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r'[^\w\- ]', '', text, flags=re.UNICODE)
    text = text.replace(' ', '-')
    return text

def extract_leading_emoji(text: str) -> tuple[str, str]:    
    parts = text.strip().split(' ', 1)
    if len(parts) == 2 and is_emoji(parts[0]):
        return parts[0], parts[1]
    return '', text

def is_emoji(s: str) -> bool:    
    return bool(re.match(r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF]$', s))


def parse_headings(lines, base_level):
    pattern = re.compile(r'^(#{1,6})\s+(.*)')
    headings = []

    for line in lines:
        match = pattern.match(line)
        if match:
            raw_level = len(match.group(1))
            if raw_level < base_level:
                continue

            level = raw_level - base_level + 1
            full_title = match.group(2).strip()

            icon, title = extract_leading_emoji(full_title)
            slug = github_slugify(title)
            headings.append((level, icon, title, slug))
    return headings

def generate_index(headings, use_links=True, use_numbering=False):
    index_lines = []
    counters = []

    for level, icon, title, slug in headings:
        while len(counters) < level:
            counters.append(0)
        counters = counters[:level]
        counters[-1] += 1

        num = '.'.join(str(n) for n in counters)
        prefix = f"{num}· " if use_numbering else ''
        label = f"{prefix}{title}"

        indent = '  ' * (level - 1)
        if use_links:
            line = f"{indent}- {icon} [{label}](#{slug})" if icon else f"{indent}- [{label}](#{slug})"
        else:
            line = f"{indent}- {icon} {label}".strip()

        index_lines.append(line)

    return index_lines

def main():
    parser = argparse.ArgumentParser(description="Generate a Markdown index with links.")
    parser.add_argument("file", help="Path to the Markdown file")
    parser.add_argument("--base-level", type=int, default=1, help="Base heading level to start from (default: 1 = #)")
    parser.add_argument("--no-links", action="store_true", help="Do not generate links, just plain text")
    parser.add_argument("--numbered", action="store_true", help="Add hierarchical numbering before titles")

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {args.file}")
        sys.exit(1)

    lines = path.read_text(encoding='utf-8').splitlines()
    headings = parse_headings(lines, args.base_level)
    index = generate_index(
        headings,
        use_links=not args.no_links,
        use_numbering=args.numbered
    )

    print('\n'.join(index))

if __name__ == '__main__':
    main()