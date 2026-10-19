"""Primitive subcommands for the tokenbuffet.extractors package.

The OS entry-point scripts (read-provider.sh / read-provider.ps1) orchestrate these; this
module only exposes the two reusable primitives as a CLI:

    python -m tokenbuffet.extractors capture <op> <config> <out_raw.txt>
    python -m tokenbuffet.extractors parse   <op> <config> <raw.txt> <out.json> [--provider NAME]

`capture` drives the TUI and writes cleaned screen text (expensive). `parse`
runs the regex extraction over captured text and writes the structured JSON
(cheap, re-runnable). Workflow concerns — provider naming, output filenames,
--raw-only / --extract handling, sequencing — live in the shell scripts, not
here.
"""
import argparse
import json
import os
import sys

from . import config as cfgmod
from .tui import drive_tui
from .models import parse_models
from .usage import parse_usage
from .util import clean_screen
from .process_env import build_process_env

_PARSERS = {'models': parse_models, 'usage': parse_usage}


def _name_for(inp):
    """Fallback provider name when a script doesn't pass --provider."""
    base = os.path.basename(inp.rstrip('/\\'))
    if base in ('config.json', 'config'):
        return os.path.basename(os.path.dirname(inp)) or 'provider'
    return base.replace('.json', '') or 'provider'


def _capture(args):
    # Capture runs in its own process, so applying a provider's subprocess
    # environment here covers both the ConPTY TUI and models subcommand.
    provider_config = cfgmod.load_config(args.config)
    os.environ.update(build_process_env(provider_config))
    for key in provider_config.get('process_env', {}).get('unset', []):
        os.environ.pop(key, None)
    cfg = cfgmod.load_section(args.config, args.op)
    # Models can be sourced non-interactively: the `/model` TUI picker shows
    # friendly labels, but the `--model` identifier only lives in the CLI's
    # `models` subcommand. A `list_cmd` in the config opts into that cheaper,
    # cross-platform path; everything else still drives the live TUI.
    list_cmd = (cfg or {}).get('list_cmd')
    try:
        if args.op == 'models' and list_cmd:
            from .subcmd import run_list_cmd
            raw = run_list_cmd(cfg)
        else:
            raw = drive_tui(cfg)
    except Exception as e:
        print(f'capture failed: {type(e).__name__}: {e}', file=sys.stderr)
        return 1
    cleaned = clean_screen(raw, strip_terms=[os.getcwd()],
                           drop_lines=(cfg or {}).get('strip_lines', []))
    # Readiness gate: if the config declares an `expect` marker and it is absent,
    # the TUI never reached the real panel — almost always because the CLI is
    # un-initialized or this folder is not trusted (and any local settings were
    # not honored, e.g. agy, which keeps trust in its global config). Fail loudly
    # with an actionable message instead of handing a half-captured screen to the
    # parser. The partial capture is still written for inspection.
    expect = (cfg or {}).get('expect')
    if expect and expect.lower() not in cleaned.lower():
        with open(args.out, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        stuck = next((ln.strip() for ln in cleaned.splitlines() if ln.strip()), '(blank screen)')
        print(f'cannot extract {args.op} data: CLI stopped at "{stuck}" '
              f'(expected "{expect}") — likely not signed in or onboarding/trust unfinished '
              f'(partial screen: {args.out})', file=sys.stderr)
        return 1
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f'captured {args.out}', file=sys.stderr)
    return 0


def _parse(args):
    cfg = cfgmod.load_section(args.config, args.op)
    try:
        with open(args.raw, encoding='utf-8') as f:
            text = f.read()
    except OSError as e:
        print(f'cannot read {args.raw}: {e}', file=sys.stderr)
        return 1
    try:
        result = _PARSERS[args.op](cfg, text)
    except Exception as e:
        result = {'error': f'{type(e).__name__}: {e}'}
    if args.op == 'usage':
        limits = result.get('limits') or {}
        has_quota = any(isinstance(period, dict) and period.get('remaining_pct') is not None
                        for period in limits.values())
        if not has_quota:
            non_empty = [line.strip() for line in text.splitlines() if line.strip()]
            preview = " | ".join(non_empty[:3]) if non_empty else '<empty capture>'
            print(f'usage unavailable for {_name_for(args.config)}: CLI did not reach quota screen (likely blocked by a gate, prompt, or unhandled theme/login screen). '
                  f'Screen showed: "{preview[:240]}". Check raw capture: {args.raw}', file=sys.stderr)
            return 1
    elif result.get('error'):
        print(f'{args.op} parse failed: {result["error"]}', file=sys.stderr)
        return 1
    envelope = {'provider': args.provider or _name_for(args.config),
                args.op: result}
    with open(args.out, 'w', encoding='utf-8') as f:
        json.dump(envelope, f, indent=2)
    print(f'saved {args.out}', file=sys.stderr)
    print(json.dumps(envelope, indent=2))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(
        prog='python -m tokenbuffet.extractors', description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)

    c = sub.add_parser('capture', help='drive the TUI, write cleaned screen text')
    c.add_argument('op', choices=['models', 'usage'])
    c.add_argument('config', help='provider name, config.json path, or section JSON')
    c.add_argument('out', help='output .txt path for the cleaned screen')
    c.set_defaults(func=_capture)

    pr = sub.add_parser('parse', help='extract structured JSON from captured text')
    pr.add_argument('op', choices=['models', 'usage'])
    pr.add_argument('config', help='provider name, config.json path, or section JSON')
    pr.add_argument('raw', help='captured .txt path to read')
    pr.add_argument('out', help='output .json path')
    pr.add_argument('--provider', help='provider name for the JSON envelope')
    pr.set_defaults(func=_parse)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == '__main__':
    sys.exit(main())
