"""Markdown processing utilities."""

import markdown2


def markdown_to_html(text: str, header_ids=True) -> str:
    extras = {
        'breaks': {'on_backslash': True},
        'cuddled-lists': None,
        'fenced-code-blocks': None,
        'middle-word-em': {'allowed': False},
        'tables': None,
        'target-blank-links': None,
    }

    if header_ids:
        extras['header-ids'] = None

    return markdown2.markdown(text, extras=extras)
