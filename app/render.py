"""Markdown → HTML con resaltado de código de Pygments."""

from __future__ import annotations

from functools import cache

from markdown_it import MarkdownIt
from markupsafe import Markup, escape
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name
from pygments.util import ClassNotFound

_FORMATTER = HtmlFormatter(nowrap=True)


def resaltar(codigo: str, lenguaje: str = "python") -> str:
    """Devuelve el código con spans de Pygments (sin `<pre>`); escapa si no hay lexer."""
    try:
        lexer = get_lexer_by_name(lenguaje or "text")
    except ClassNotFound:
        return str(escape(codigo))
    return highlight(codigo, lexer, _FORMATTER)


def _highlight(codigo: str, lenguaje: str, _attrs: str) -> str:
    # markdown-it envuelve el resultado en <pre><code class="language-…">.
    return resaltar(codigo, lenguaje or "text")


_MD = MarkdownIt("commonmark", {"highlight": _highlight}).enable("table").enable("strikethrough")


def _abrir_links_afuera(self, tokens, idx, options, env):  # type: ignore[no-untyped-def]
    token = tokens[idx]
    if str(token.attrGet("href") or "").startswith("http"):
        token.attrSet("target", "_blank")
        token.attrSet("rel", "noopener")
    return _MD.renderer.renderToken(tokens, idx, options, env)


_MD.add_render_rule("link_open", _abrir_links_afuera)


def markdown(texto: str) -> Markup:
    return Markup(_MD.render(texto))


def markdown_inline(texto: str) -> Markup:
    return Markup(_MD.renderInline(texto))


def codigo_html(codigo: str, lenguaje: str = "python") -> Markup:
    html = resaltar(codigo, lenguaje)
    return Markup(f'<pre><code class="language-{lenguaje}">{html}</code></pre>')


@cache
def css_pygments() -> str:
    """CSS de resaltado para tema claro y oscuro, scoped a los bloques de código."""
    claro = HtmlFormatter(style="friendly").get_style_defs("pre code")
    oscuro = HtmlFormatter(style="github-dark").get_style_defs("pre code")
    return f"{claro}\n@media (prefers-color-scheme: dark) {{\n{oscuro}\n}}\n"
