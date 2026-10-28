"""Veritas (veritaszim.net) Word texts of the Constitution of Zimbabwe -> units, one file per section or paragraph.

Veritas publishes the Constitution as enacted (Act 1 of 2013, .docx) and consolidated "as amended up to" a date
(.doc, Word 97). Both are text, not scans: .docx is read with the standard library (zipfile + the XML), .doc with
antiword (UTF-8 output, no line wrapping). parse.py reads only the cache; this module turns one document into units.

The text rule (same as the Peachjam adapter): one unit per section of the Constitution and per numbered paragraph of
a Schedule; a Schedule (or the part of one) without numbered paragraphs is one unit; the Preamble is a unit. One
paragraph or item per line; the unit's number and heading as the first line. Chapter and Part headings above the
provisions are left out. Veritas's bracketed amendment notes ("[Subsection amended by s. 3 of Act No. 2 of 2021]") are
left out of the text and returned as credit evidence; its footnote markers ("[1]") and footnotes are left out.
"""
from __future__ import annotations

import re
import subprocess
import unicodedata
import zipfile
from io import BytesIO
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

QUOTES = str.maketrans({"“": '"', "”": '"', "„": '"', "″": '"', "‘": "'", "’": "'",
                        "‚": "'", "′": "'", " ": " ", " ": " ", " ": " ", " ": " ",
                        "​": "", "­": "", "‐": "-", "‑": "-", "‒": "-", "−": "-",
                        "―": "—", "﻿": "", "–": "—"})

ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6}


# ---------------------------------------------------------------- documents -> raw lines

def docx_lines(b: bytes) -> list[str]:
    """Paragraphs of word/document.xml, tabs kept as \\t (they separate numbers from text)."""
    with zipfile.ZipFile(BytesIO(b)) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    out = []
    for p in root.iter(W + "p"):
        parts = []
        for el in p.iter():
            if el.tag == W + "t":
                parts.append(el.text or "")
            elif el.tag == W + "tab":
                parts.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                parts.append(" ")
            elif el.tag in (W + "drawing", W + "pict"):
                parts.append("[pic]")
        out.append("".join(parts))
    return out


def doc_lines(path: str) -> list[str]:
    """antiword's UTF-8 text of a Word 97 file (no wrapping)."""
    r = subprocess.run(["antiword", "-m", "UTF-8.txt", "-w", "0", path], capture_output=True, check=True)
    return r.stdout.decode("utf-8").replace("\r\n", "\n").split("\n")


def antiword_version() -> str:
    r = subprocess.run(["antiword", "-h"], capture_output=True)
    m = re.search(rb"Version:\s*([^\r\n]+)", r.stdout + r.stderr)
    return m.group(1).decode().strip() if m else "unknown"


# ---------------------------------------------------------------- normalisation

def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).translate(QUOTES)
    s = re.sub(r"\[(\d{1,2})\]", "", s)          # Veritas footnote markers
    s = s.replace("[pic]", " [image] ")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^(\d+[A-Z]?\.)\s*(\()", r"\1 \2", s)   # "2.(1) An emergency" -> "2. (1) An emergency"
    s = re.sub(r"(\[image\] ?)+", "[image] ", s).strip()
    s = s.replace(" ;", ";").replace(" ,", ",")
    return s


NOTE_RX = re.compile(r"^\[[^\]]*\b(amended|substituted|inserted|repealed|corrected|renumbered|added)\b.*"
                     r"\b(Act|SI|S\.I\.|Statutory Instrument)\b", re.I)
SECTION_RX = re.compile(r"^\t?(\d{1,3}[A-Z]?)\t+(\S.*)$")       # raw line, column 0: "43A\tRegistration of Voters"
SCHEDULE_RX = re.compile(r"^(first|second|third|fourth|fifth|sixth) schedule\b(.*)$", re.I)
CHAPTER_RX = re.compile(r"^(chapter|part)\s+\d+\b", re.I)
PARA_RX = re.compile(r"^(\d{1,2}[A-Z]?)\.(?=\s|\(|$)")


def is_note(t: str) -> bool:
    return bool(NOTE_RX.match(t))


# ---------------------------------------------------------------- lines -> units

def _key(num: str) -> str:
    m = re.fullmatch(r"(\d+)([A-Za-z]*)", num)
    return f"{int(m.group(1)):03d}{m.group(2).lower()}" if m else re.sub(r"[^a-z0-9]+", "-", num.lower())


def units_of(raw: list[str]) -> tuple[dict, dict, dict]:
    """(units {key: {label, kind, text}}, notes {key: [Veritas notes]}, chapter {key: chapter number or 'schedule'}).

    The body starts at the Preamble ("We the people of Zimbabwe"); everything before it (the Act's own sections,
    Veritas's cover notes and the arrangement of sections) is not the Constitution's text."""
    start = next(i for i, l in enumerate(raw) if norm(l).startswith("We the people of Zimbabwe"))
    # the Preamble heading is the last non-empty line before it
    h = start - 1
    while not norm(raw[h]):
        h -= 1
    # footnote texts at the end of an antiword document follow a line of dashes
    end = len(raw)
    for i in range(len(raw) - 1, start, -1):
        if re.fullmatch(r"\s*-{10,}\s*", raw[i]):
            end = i
            break
    units: dict = {}
    notes: dict = {}
    chapter: dict = {}
    cur = {"key": "preamble", "label": "Preamble", "kind": "preamble", "head": "Preamble", "lines": []}
    order = []
    ch = "preamble"
    sched = None          # (number, heading) while inside a Schedule
    in_arrangement = False

    def flush():
        if cur is None:
            return
        body = [x for x in cur["lines"] if x]
        if not body and cur["kind"] != "schedule":
            return
        k = cur["key"]
        if k in units:
            n = 2
            while f"{k}-{n}" in units:
                n += 1
            k = f"{k}-{n}"
        units[k] = {"label": cur["label"], "kind": cur["kind"],
                    "text": "\n".join([f"# {cur['head']}"] + body) + "\n"}
        notes[k] = cur.get("notes", [])
        chapter[k] = cur.get("chapter", ch)
        order.append(k)

    i = start
    lines = raw[:end]
    pending_head = None   # a Schedule paragraph heading waiting for its number
    while i < len(lines):
        rawl = lines[i].rstrip("\n")
        t = norm(rawl)
        i += 1
        if not t:
            continue
        m = SCHEDULE_RX.match(t)
        if m and not rawl[:1].isspace() and ("(" in m.group(2) or not m.group(2).strip() or m.group(2).strip().startswith("(")):
            flush()
            n = ORD[m.group(1).lower()]
            # the Schedule's title is the next non-empty line
            j = i
            while not norm(lines[j]):
                j += 1
            title = norm(lines[j])
            i = j + 1
            sched = (n, title)
            ch = "schedule"
            cur = {"key": f"sch-{n:02d}", "label": f"{m.group(1).capitalize()} Schedule", "kind": "schedule",
                   "head": f"{m.group(1).capitalize()} Schedule{(' ' + m.group(2).strip()) if m.group(2).strip() else ''}: {title}",
                   "lines": [], "notes": [], "chapter": "schedule"}
            in_arrangement = False
            pending_head = None
            continue
        if sched is None:
            if CHAPTER_RX.match(t) and not rawl[:1].isspace():
                if t.lower().startswith("chapter"):
                    ch = int(re.search(r"\d+", t).group(0))
                # the Chapter or Part title line that follows is a heading too: skip it
                j = i
                while j < len(lines) and not norm(lines[j]):
                    j += 1
                if j < len(lines) and not SECTION_RX.match(lines[j]) and norm(lines[j]).upper() == norm(lines[j]):
                    i = j + 1
                continue
            m = SECTION_RX.match(rawl)
            if m and not rawl[:1] == " ":
                flush()
                num, head = m.group(1), norm(m.group(2))
                cur = {"key": f"sec-{_key(num)}", "label": f"Section {num}", "kind": "sec",
                       "head": f"{num}. {head}", "lines": [], "notes": [], "chapter": ch}
                continue
            if is_note(t):
                cur.setdefault("notes", []).append(t)
                continue
            cur["lines"].append(t)
            continue
        # inside a Schedule
        if re.fullmatch(r"arrangement of paragraphs.*", t, re.I):
            in_arrangement = True
            continue
        if CHAPTER_RX.match(t) or t.lower() == "paragraph":
            # Part headings: skip with their title; the second "PART 1" ends the arrangement
            if in_arrangement and t.lower().startswith("part") and re.search(r"\b1\b", t) and cur.get("seen_part1"):
                in_arrangement = False
            if t.lower().startswith("part") and re.search(r"\b1\b", t):
                cur["seen_part1"] = True
            j = i
            while j < len(lines) and not norm(lines[j]):
                j += 1
            if j < len(lines) and norm(lines[j]).upper() == norm(lines[j]) and not PARA_RX.match(norm(lines[j])):
                i = j + 1
            continue
        if in_arrangement:
            continue
        if is_note(t):
            cur.setdefault("notes", []).append(t)
            continue
        pm = PARA_RX.match(t)
        if pm and pending_head is not None:
            flush()
            num = pm.group(1)
            cur = {"key": f"sch-{sched[0]:02d}-para-{_key(num)}", "label": f"Schedule {sched[0]}, paragraph {num}",
                   "kind": "para", "head": f"{num}. {pending_head}", "lines": [t], "notes": [], "chapter": "schedule"}
            pending_head = None
            continue
        if pending_head is not None:
            cur["lines"].append(pending_head)
            pending_head = None
        # a paragraph heading: a column-0 line in sentence case, followed by a numbered line
        nxt = i
        while nxt < len(lines) and not norm(lines[nxt]):
            nxt += 1
        if (not rawl[:1].isspace() and not t.startswith(("(", "[", '"')) and t.upper() != t
                and nxt < len(lines) and PARA_RX.match(norm(lines[nxt]))):
            pending_head = t
            continue
        cur["lines"].append(t)
    flush()
    return units, notes, chapter
