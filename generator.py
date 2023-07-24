import json
from datetime import datetime
from pathlib import Path

import pypandoc
from jinja2 import Environment, FileSystemLoader


CONTENT_DIR = Path('content')
DOCS_DIR = Path('docs')
CONFIG_FILE = Path('standalone_configs.json')

CONTEXT_BASE = {
    'title': 'grepmam',
    'year': datetime.now().year,
}


def load_config() -> list:
    return json.loads(CONFIG_FILE.read_text())


def convert_md_to_html(md_path: Path) -> str:
    content = md_path.read_text()
    if content.lstrip().startswith('<'):
        return content
    return pypandoc.convert_text(content, to='html5', format='markdown')


def generate_pages():
    config = load_config()
    env = Environment(loader=FileSystemLoader('templates'))

    # Standalone pages (from config)
    for page in config:
        template = env.get_template(page['template_file'])
        context = CONTEXT_BASE | page.get('context', {})
        output_file = page['template_file']
        (DOCS_DIR / output_file).write_text(template.render(context))
        print(f"{page['template_file']} => {output_file}")

    # Content pages (from .md files)
    for md_path in CONTENT_DIR.glob('*.md'):
        template = env.get_template('content.html')
        context = CONTEXT_BASE | {'content': convert_md_to_html(md_path)}
        filename = f'{md_path.stem}.html'
        (DOCS_DIR / filename).write_text(template.render(context))
        print(f"{md_path.name} => {filename}")


if __name__ == "__main__":
    generate_pages()
