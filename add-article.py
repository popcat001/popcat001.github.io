#!/usr/bin/env python3
"""
add-article.py — Add a new tutorial card to index.html

Usage:
  python3 add-article.py <filename.html>

The script reads the HTML file, extracts metadata automatically,
prompts for anything it can't find, inserts a card at the top of
the homepage (newest first), then optionally commits and pushes.
"""

import re
import sys
import os
import subprocess


# ── Metadata extraction ────────────────────────────────────────────────────

def extract_title(html):
    m = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
    if not m:
        return None
    title = m.group(1)
    title = re.sub(r'\s*[—–-]\s*(In-Depth Tutorial|Tutorial|Deep Dive).*$', '', title, flags=re.IGNORECASE)
    return title.strip()

def extract_description(html):
    # Try <meta name="description"> first
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Fall back to the subtitle <p> in the page header
    m = re.search(r'<p\s+style="[^"]*color:var\(--text-muted\)[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1))
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 30:
            return text
    return None

def extract_date(html):
    """Return (display_str, YYYY-MM-DD sort_key) or (None, None)."""
    m = re.search(r'Published:\s*([A-Za-z]+ \d{1,2},\s*\d{4})', html)
    if m:
        raw = m.group(1).strip()
        try:
            from datetime import datetime
            dt = datetime.strptime(raw, '%B %d, %Y')
            return dt.strftime('%b %d, %Y'), dt.strftime('%Y-%m-%d')
        except ValueError:
            pass
    return None, None

def extract_read_time(html):
    m = re.search(r'Estimated read time:\s*(\d+)\s*min', html)
    if m:
        return m.group(1) + ' min read'
    return None

def extract_source(html):
    m = re.search(r'Source:\s*<a[^>]+>([^<]+)</a>', html)
    if m:
        return m.group(1).strip()
    return 'Anthropic Engineering'


# ── Card HTML ──────────────────────────────────────────────────────────────

TAGS = {
    '1': ('Agents',     'tag-purple'),
    '2': ('Evaluation', 'tag-amber'),
    '3': ('Research',   'tag-purple'),
    '4': ('Safety',     'tag-amber'),
    '5': ('Tools',      'tag-purple'),
}

CARD_TEMPLATE = """\

    <a class="card" href="{filename}">
      <div class="card-meta">
        <span class="card-tag {tag_class}">{tag}</span>
        <span class="card-date">{date} · {source}</span>
      </div>
      <h2>{title}</h2>
      <p>{description}</p>
      <div class="card-footer">
        <div class="card-stats">
          <span>{read_time}</span>
        </div>
        <span class="card-read">Read</span>
      </div>
    </a>"""


# ── index.html insertion ───────────────────────────────────────────────────

def insert_card(index_path, card_html):
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    marker = '<div class="cards">'
    pos = content.find(marker)
    if pos == -1:
        raise ValueError('Could not find <div class="cards"> in index.html')
    insert_at = pos + len(marker)
    new_content = content[:insert_at] + card_html + content[insert_at:]
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


# ── Prompt helpers ─────────────────────────────────────────────────────────

def prompt(label, default=None):
    hint = f' [{default}]' if default else ''
    val = input(f'{label}{hint}: ').strip()
    return val if val else default

def prompt_tag():
    print('\nTag:')
    for k, (name, _) in TAGS.items():
        print(f'  {k}) {name}')
    choice = input('Choose [1]: ').strip() or '1'
    return TAGS.get(choice, TAGS['1'])


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 add-article.py <filename.html>')
        sys.exit(1)

    filename = os.path.basename(sys.argv[1])
    filepath = os.path.join(os.path.dirname(__file__), filename)
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')

    if not os.path.exists(filepath):
        print(f'Error: {filename} not found in the site directory.')
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # ── Extract metadata ──
    title       = extract_title(html)
    description = extract_description(html)
    date_str, _ = extract_date(html)
    read_time   = extract_read_time(html)
    source      = extract_source(html)

    print(f'\n── Metadata found in {filename} ──')
    print(f'  Title      : {title or "(not found)"}')
    print(f'  Date       : {date_str or "(not found)"}')
    print(f'  Read time  : {read_time or "(not found)"}')
    print(f'  Source     : {source}')
    print(f'  Description: {(description[:80] + "…") if description and len(description) > 80 else description or "(not found)"}')
    print()

    # ── Confirm / fill in missing ──
    title       = prompt('Title', title)
    date_str    = prompt('Date (e.g. Jan 9, 2026)', date_str)
    read_time   = prompt('Read time (e.g. 30 min read)', read_time or '20 min read')
    source      = prompt('Source', source)
    description = prompt('Description (1–2 sentences)', description)
    tag, tag_class = prompt_tag()

    # ── Build card ──
    card_html = CARD_TEMPLATE.format(
        filename=filename,
        tag=tag,
        tag_class=tag_class,
        date=date_str,
        source=source,
        title=title,
        description=description,
        read_time=read_time,
    )

    print(f'\nInserting card for "{title}" at the top of index.html…')
    insert_card(index_path, card_html)
    print('Done.')

    # ── Git ──
    push = input('\nCommit and push to GitHub? [Y/n]: ').strip().lower()
    if push in ('', 'y', 'yes'):
        subprocess.run(['git', 'add', 'index.html', filename], cwd=os.path.dirname(__file__))
        subprocess.run(['git', 'commit', '-m', f'Add tutorial: {title}'], cwd=os.path.dirname(__file__))
        subprocess.run(['git', 'push'], cwd=os.path.dirname(__file__))
        print(f'\nLive at: https://popcat001.github.io/{filename}')
    else:
        print(f'\nindex.html updated locally. Run git push when ready.')


if __name__ == '__main__':
    main()
