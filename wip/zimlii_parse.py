"""Build Zimbabwe's ZimLII part, corpus.d/20-zimlii.json, from the cache only, through the shared Peachjam adapter.

    python -X utf8 scripts/zimbabwe-law/zimlii_parse.py

Reads acts.json (configuration), sources.json (pinned archived captures, written by zimlii_fetch.py) and .cache/.
Writes corpus.d/20-zimlii.json (atomically: acts, laws, sources, decisions, ai_use; the country block and the
repository docs belong to the Constitution part and repo/, so peachjam's write_corpus/write_docs are not used) and
.tmp/zimlii_verification.json (the adapter's checks). Deterministic: the same cache gives the same bytes.
"""
import json
import os
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

# One part per act, so each can be verified (<part>.PUBLISH) on its own. The first part also carries the ZimLII
# sources, the shared decisions and ai_use.
PARTS = {"cyber-data-protection": "20-cyber-data-protection", "criminal-law-code": "21-criminal-law-code"}
EXTRA = {"criminal-law-code": [
    "Criminal Law Code: not verified for main. ZimLII's newest archived page (capture 20260311101030) says its newest "
    "version, 2022-03-11, applied \"from 11 March 2022 to 17 September 2024\", and lists two amendments it has not "
    "applied: the Criminal Laws Amendment (Protection of Children and Young Persons) Act, 2024 (18 September 2024) "
    "and the Death Penalty Abolition Act, 2024 (31 December 2024). The last version here is therefore not today's "
    "law, so this part stays on the preview branch.",
    "Criminal Law Code: the first version, 2017-03-23, is ZimLII's consolidation (\"revised and consolidated by the "
    "Law Development Commission of Zimbabwe ... up-to-date as at 31st December 2016\"), credited to the publisher as "
    "the oldest version available."],
    "cyber-data-protection": [
    "Cyber and Data Protection Act: ZimLII's only version is dated 2022-03-11, its page saying \"Published on 11 "
    "March 2022\" and \"Commenced on 11 March 2022\"; that date is used as ZimLII gives it."]}

corpus, report = peachjam.parse(HERE)
(HERE / "corpus.d").mkdir(exist_ok=True)
for n, act in enumerate(corpus["acts"]):
    used = {act.get("first_law")} | set(act.get("earlier_laws", []))
    for v in act["versions"]:
        used |= {l for ls in v.get("credits", {}).values() for l in ls}
    mine = [d for d in corpus["decisions"] if d.startswith(act["short"] + ":")]
    shared = [d for d in corpus["decisions"] if not any(d.startswith(a["short"] + ":") for a in corpus["acts"])]
    first = PARTS[act["slug"]] == min(PARTS.values())
    part = {"sources": corpus["sources"] if first else [],
            "laws": {k: v for k, v in corpus["laws"].items() if k in used},
            "acts": [act], "applies": [],
            "decisions": (shared if first else []) + mine + EXTRA.get(act["slug"], []),
            "ai_use": corpus["ai_use"] if first else []}
    out = HERE / "corpus.d" / f"{PARTS[act['slug']]}.json"
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(part, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, out)
(HERE / ".tmp").mkdir(exist_ok=True)
(HERE / ".tmp" / "zimlii_verification.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n",
                                                         encoding="utf-8", newline="\n")
print(json.dumps(peachjam.summary(corpus, report), indent=1))
