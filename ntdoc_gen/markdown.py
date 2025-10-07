"""Markdown processing utilities."""

import re

import markdown2


def markdown_to_html(text: str, header_ids=True) -> str:
    extras = {
        'breaks': {'on_backslash': True},
        'code-friendly': None,  # TODO: replace with: 'middle-word-em': {'allowed': False},
        'cuddled-lists': None,
        'fenced-code-blocks': None,
        'tables': None,
        'target-blank-links': None,
    }

    if header_ids:
        extras['header-ids'] = None

    # Remove HTML comments. markdown2 does not do this in safe mode.
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # Escape \< and \> so that markdown2 safe mode doesn't escape them.
    def bracket_escape(m: re.Match) -> str:
        # Skip if inside of a code block.
        code_block_count = text.count('```', 0, m.start())
        if code_block_count % 2 == 1:
            return m.group(0)

        # Skip if line inside of an inline code span.
        line_start = text.rfind('\n', 0, m.start()) + 1
        backtick_count = text.count('`', line_start, m.start())
        if backtick_count % 2 == 1:
            return m.group(0)

        # Skip if escaped with an odd number of backslashes.
        preceding_text = text[:m.start()]
        trailing_backslashes = 0
        for char in reversed(preceding_text):
            if char == '\\':
                trailing_backslashes += 1
            else:
                break
        if trailing_backslashes % 2 == 1:
            return m.group(0)

        if m.group(0) == r'\<':
            return '&lt;'
        else:
            return '&gt;'

    text = re.sub(r'\\(?!<br>)[<>]', bracket_escape, text)

    html = markdown2.markdown(text, extras=extras, safe_mode='escape')

    # Undo safe mode for <br>.
    html = html.replace('&lt;br&gt;', '<br>')

    # Other replacements which aren't handled by markdown2 safe mode.
    html = html.replace('&lt;code>', '<code>')
    html = html.replace('&lt;/code>', '</code>')
    html = html.replace('<a href="#">', '<a href="">')

    return html
