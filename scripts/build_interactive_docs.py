"""Regenerate the interactive documentation site from a folder of Markdown files.

    python scripts/build_interactive_docs.py [SRC] [--out OUT]

SRC defaults to docs/interactive-documentation and OUT to site (both relative to the repo root).

Each <name>.md becomes <out>/<name>.html (plus downloads/), and <out>/index.html links to them.
Needs `pip install concept-mapmaker`. Everything in --out is replaced.
"""
import argparse
import html
import re
import shutil
from pathlib import Path

from concept_mapmaker import build_map

ROOT = Path(__file__).resolve().parent.parent


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

    (args.out / "index.html").write_text(
        '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Token Buffet Interactive Documentation</title>\n"
        "<style>body{font:16px/1.5 system-ui,sans-serif;max-width:40rem;margin:3rem auto;padding:0 16px}"
        "li{margin:.5rem 0}</style>\n</head>\n<body>\n<h1>Token Buffet Interactive Documentation</h1>\n<ul>\n"
        + "\n".join(links)
        + "\n</ul>\n</body>\n</html>\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
