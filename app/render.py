"""Markdown → HTML with Pygments code highlighting."""

from __future__ import annotations

from functools import cache

from markdown_it import MarkdownIt
from markupsafe import Markup, escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_FORMATTER = HtmlFormatter(nowrap=True)


def highlight_code(code: str, language: str = "python") -> str:
    """Returns the code with Pygments spans (no `<pre>`); escapes it if there is no lexer."""
    try:
        lexer = get_lexer_by_name(language or "text")
    except ClassNotFound:
        return str(escape(code))
    return highlight(code, lexer, _FORMATTER)


def _highlight(code: str, language: str, _attrs: str) -> str:
    # markdown-it wraps the result in <pre><code class="language-…">.
    return highlight_code(code, language or "text")


_MD = MarkdownIt("commonmark", {"highlight": _highlight}).enable("table").enable("strikethrough")


def _open_external_links_in_new_tab(self, tokens, idx, options, env):  # type: ignore[no-untyped-def]
    token = tokens[idx]
    if str(token.attrGet("href") or "").startswith("http"):
        token.attrSet("target", "_blank")
        token.attrSet("rel", "noopener")
    return _MD.renderer.renderToken(tokens, idx, options, env)


_MD.add_render_rule("link_open", _open_external_links_in_new_tab)


def markdown(text: str) -> Markup:
    return Markup(_MD.render(text))


def markdown_inline(text: str) -> Markup:
    return Markup(_MD.renderInline(text))


def code_html(code: str, language: str = "python") -> Markup:
    html = highlight_code(code, language)
    return Markup(f'<pre><code class="language-{language}">{html}</code></pre>')


@cache
def pygments_css() -> str:
    """Highlighting CSS for light and dark themes, scoped to code blocks."""
    light = HtmlFormatter(style="friendly").get_style_defs("pre code")
    dark = HtmlFormatter(style="github-dark").get_style_defs("pre code")
    return f"{light}\n@media (prefers-color-scheme: dark) {{\n{dark}\n}}\n"
