# Vendored front-end libraries

Third-party files served by the app from `/static/vendor/`, so it works without internet access.
They are copied unmodified from the official npm builds published on the CDNs below.

| Library | Version | License | Source |
|---|---|---|---|
| [htmx](https://htmx.org/) | 2.0.4 | 0BSD (`htmx/LICENSE`) | `https://cdn.jsdelivr.net/npm/htmx.org@2.0.4/dist/htmx.min.js` |
| [CodeMirror 5](https://codemirror.net/5/) | 5.65.18 | MIT (`codemirror/LICENSE`) | `https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.18/` |

CodeMirror files used: `codemirror.min.js`, `codemirror.min.css`, `mode/python/python.min.js`,
and the addons `edit/matchbrackets`, `edit/closebrackets`, `selection/active-line` and
`comment/comment` (`.min.js`).

## Updating

Download the new version of each file to the same path, update this table, and check the
templates that load them (`app/templates/base.html` and `app/templates/chapter.html`).
`tests/test_app.py::test_no_cdn_dependencies` checks that every vendored file the pages
reference is served.
