"""Regenerate the interactive documentation site from a folder of Markdown files.

    python scripts/build_interactive_docs.py [SRC] [--out OUT]

SRC defaults to docs/interactive-documentation and OUT to site (both relative to the repo root).

Each <name>.md in SRC becomes an interactive page <out>/<name>.html (plus downloads/). Each .md in
docs/static-pages becomes a plain static page <out>/<name>.html. <out>/index.html links to all of them.
Needs `pip install "concept-mapmaker>=0.2.0"`. Everything in --out is replaced.
"""
import argparse
import html
import re
import shutil
from pathlib import Path

from concept_mapmaker import build_map
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "docs/static-pages"

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{--bg:#fff;--fg:#1b1f24;--muted:#57606a;--line:#d0d7de;--link:#0969da;--code:#f6f8fa}}
@media (prefers-color-scheme:dark){{:root{{--bg:#0d1117;--fg:#e6edf3;--muted:#8b949e;--line:#30363d;--link:#58a6ff;--code:#161b22}}}}
body{{background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif;max-width:46rem;margin:2.5rem auto;padding:0 16px}}
a{{color:var(--link)}}h1{{line-height:1.25}}h2{{margin-top:2rem;padding-bottom:.3rem;border-bottom:1px solid var(--line)}}
li{{margin:.4rem 0}}code{{background:var(--code);padding:.1rem .3rem;border-radius:4px}}
.back{{color:var(--muted);font-size:.9rem}}
</style>
</head>
<body>
<p class="back"><a href="index.html">&larr; Token Buffet Documentation</a></p>
{body}
</body>
</html>
"""


def headings(md: Path, level: str) -> list[str]:
    return re.findall(rf"^{level} (.+?)\s*$", md.read_text(encoding="utf-8"), re.M)


def spec_for(md: Path) -> dict:
    return {
        "title": "Token Buffet",
        "subtitle": "Interactive Documentation",
        "page_title": headings(md, "#")[0],
        "legend": [
            {"match": f"^{re.escape(h)}$", "key": f"b{i}", "label": h}
            for i, h in enumerate(headings(md, "##"), 1)
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src", type=Path, nargs="?", default=ROOT / "docs/interactive-documentation",
                    help="folder of .md files")
    ap.add_argument("--out", type=Path, default=ROOT / "site")
    args = ap.parse_args()

    mds = sorted(args.src.glob("*.md"))
    if not mds:
        raise SystemExit(f"no .md files in {args.src}")

    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.iterdir():
        shutil.rmtree(old) if old.is_dir() else old.unlink()

    links = []
    for md in mds:
        build_map(md, spec_for(md), output=args.out / f"{md.stem}.html")
        links.append(f'  <li><a href="{md.stem}.html">{html.escape(headings(md, "#")[0])}</a></li>')

    md_it = MarkdownIt("commonmark", {"linkify": False}).enable("table")
    pages = []
    for md in sorted(STATIC.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        title = headings(md, "#")[0]
        (args.out / f"{md.stem}.html").write_text(
            PAGE.format(title=html.escape(title), body=md_it.render(text)), encoding="utf-8")
        pages.append(f'  <li><a href="{md.stem}.html">{html.escape(title)}</a></li>')

    (args.out / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Token Buffet Interactive Documentation</title>\n"
        "<style>body{font:16px/1.5 system-ui,sans-serif;max-width:40rem;margin:3rem auto;padding:0 16px}"
        "li{margin:.5rem 0}</style>\n</head>\n<body>\n<h1>Token Buffet Interactive Documentation</h1>\n<ul>\n"
        + "\n".join(links)
        + "\n</ul>\n"
        + ("<h2>Guides</h2>\n<ul>\n" + "\n".join(pages) + "\n</ul>\n" if pages else "")
        + "</body>\n</html>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
