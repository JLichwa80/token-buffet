from pathlib import Path

# LOG_DIR lives under wherever tbuffet is run from — not derived from __file__,
# since an installed package lives inside site-packages.
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
