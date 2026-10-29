"""Fetch Zimbabwe's ZimLII acts (acts.json) through the shared Peachjam adapter.

    python -X utf8 scripts/zimbabwe-law/zimlii_fetch.py

All the work is in peachjam.py (canonical copy: scripts/africa-law/peachjam.py, never edited here; this folder carries
the exact copy it was built with). Network: Common Crawl and the Wayback Machine (CDX API and raw `id_` captures of
ZimLII expression pages) only; ZimLII itself is never requested. Cache: .cache/ (sha256 of the URL), every request in
.cache/requests.jsonl. The Constitution is not read from ZimLII (see fetch.py / parse.py: Veritas).
"""
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARED = HERE.parent / "africa-law" / "peachjam.py"
if SHARED.exists() and (not (HERE / "peachjam.py").exists()
                        or SHARED.read_bytes() != (HERE / "peachjam.py").read_bytes()):
    shutil.copyfile(SHARED, HERE / "peachjam.py")
sys.path.insert(0, str(HERE))
import peachjam  # noqa: E402

peachjam.fetch(HERE)
