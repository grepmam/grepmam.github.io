from pathlib import Path

import pypandoc
from jinja2 import Environment, FileSystemLoader


CONTENT_DIR = Path('content')
DOCS_DIR = Path('docs')

CONTEXT_BASE = {
    'title': 'Grepmam Blog',
    'navbar': {
        'brand': {
            'content': 'grepmam@home:~$',
            'href': 'index.html',
        },
        'nav_items': [
            {'name': 'Writeups', 'href': 'writeups.html'},
            {'name': 'Projects', 'href': 'projects.html'},
            {'name': 'About Me', 'href': 'about_me.html'},
        ]
    },
    'footer': {
        'brand': 'grepmam © 2025',
        'href': 'https://github.com/grepmam',
    },
}


def generate_page():
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template('base.html')

    for md_path in CONTENT_DIR.glob('*.md'):
        content_html = convert_md_to_html(md_path)
        context = CONTEXT_BASE | {'content': content_html}
        full_html = template.render(context)
        filename = f'{md_path.stem}.html'
        output_file = DOCS_DIR / filename
        output_file.write_text(full_html)
        print(f"{md_path.name} => {filename}")

def convert_md_to_html(md_path: str):
    markdown_content = md_path.read_text()
    return pypandoc.convert_text(
        markdown_content,
        to='html5',
        format='markdown',
    )


if __name__ == "__main__":
    generate_page()