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
                        "―": "—", "﻿": "", "–": "—",
                        "": "—", "": "—", "⎯": "—", "": "•"})

ORD = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6}


# ---------------------------------------------------------------- documents -> raw lines

def _numbering(z: zipfile.ZipFile) -> dict:
    """{numId: (numFmt, lvlText, start)} for level 0 of each list in word/numbering.xml."""
    try:
        root = ET.fromstring(z.read("word/numbering.xml"))
    except KeyError:
        return {}
    absn = {}
    for a in root.iter(W + "abstractNum"):
        for lvl in a.iter(W + "lvl"):
            if lvl.get(W + "ilvl") == "0":
                fmt = lvl.find(W + "numFmt")
                txt = lvl.find(W + "lvlText")
                st = lvl.find(W + "start")
                absn[a.get(W + "abstractNumId")] = (fmt.get(W + "val") if fmt is not None else "decimal",
                                                    txt.get(W + "val") if txt is not None else "%1",
                                                    int(st.get(W + "val")) if st is not None else 1)
    out = {}
    for n in root.iter(W + "num"):
        a = n.find(W + "abstractNumId")
        if a is not None and a.get(W + "val") in absn:
            out[n.get(W + "numId")] = absn[a.get(W + "val")]
    return out


def _fmt_num(n: int, fmt: str) -> str:
    if fmt == "lowerLetter":
        return chr(ord("a") + n - 1)
    if fmt == "lowerRoman":
        vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
        out = ""
        for v, r in vals:
            while n >= v:
                out += r
                n -= v
        return out
    return str(n)


def docx_lines(b: bytes) -> list[str]:
    """Paragraphs of word/document.xml, tabs kept as \\t (they separate numbers from text). Word's automatic list
    numbers (w:numPr) are not in the text runs, so they are generated from word/numbering.xml, counting per list."""
    with zipfile.ZipFile(BytesIO(b)) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        numbering = _numbering(z)
    counters: dict = {}
    out = []
    for p in root.iter(W + "p"):
        parts = []
        ppr = p.find(W + "pPr")
        num = ppr.find(W + "numPr") if ppr is not None else None
        if num is not None:
            nid = num.find(W + "numId")
            lvl = num.find(W + "ilvl")
            nid = nid.get(W + "val") if nid is not None else None
            if nid in numbering and (lvl is None or lvl.get(W + "val") == "0"):
                fmt, txt, start = numbering[nid]
                counters[nid] = counters.get(nid, start - 1) + 1
                parts.append(txt.replace("%1", _fmt_num(counters[nid], fmt)) + "\t")
        for el in p.iter():
            if el.tag == W + "t":
                parts.append(el.text or "")
            elif el.tag == W + "tab":
                parts.append("\t")
            elif el.tag in (W + "br", W + "cr"):
                parts.append("\n")
            elif el.tag in (W + "drawing", W + "pict"):
                parts.append("[pic]")
        out.extend("".join(parts).split("\n"))
    return out


def doc_lines(path: str) -> list[str]:
    """antiword's UTF-8 text of a Word 97 file (no wrapping)."""
    r = subprocess.run(["antiword", "-m", "UTF-8.txt", "-w", "0", path], capture_output=True, check=True)
    lines = r.stdout.decode("utf-8").replace("\r\n", "\n").split("\n")
    # antiword renders the Symbol-font dash that Veritas uses before a list ("consists of—") as "(": a "(" right
    # after a letter and before the end of the line, a space or a quote is that dash.
    return [re.sub(r'(?<=[A-Za-z])\((?=$|\s|")', "—", line) for line in lines]


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
CHAPTER_RX = re.compile(r"^(chapter|part)\s*(\d+|[IVX]+)$|^(chapter|part)\s+\d+\b", re.I)
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
    # Veritas appends superseded text after the Sixth Schedule ("Section 180 before its amendment by Act 10 of 2017")
    for i in range(start, end):
        if re.match(r"^Section \d+[A-Z]? (as it was )?before its amendment", norm(raw[i])):
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
        if not body:
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
            refs = ""
            if title.startswith("(") and not m.group(2).strip():  # "(Sections 94, 104, ...)" on its own line
                refs = " " + title
                j += 1
                while not norm(lines[j]):
                    j += 1
                title = norm(lines[j])
            i = j + 1
            sched = (n, title)
            ch = "schedule"
            cur = {"key": f"sch-{n:02d}", "label": f"{m.group(1).capitalize()} Schedule", "kind": "schedule",
                   "head": f"{m.group(1).capitalize()} Schedule{(' ' + m.group(2).strip()) if m.group(2).strip() else ''}{refs}: {title}",
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
                if j < len(lines) and not SECTION_RX.match(lines[j]):
                    i = j + 1  # the Chapter or Part title
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
            if t.lower() == "preamble" and ch != "preamble" and not rawl[:1] == " ":
                flush()  # a Chapter's own preamble (Chapter 14)
                cur = {"key": f"chapter-{ch:02d}-preamble", "label": f"Chapter {ch}, preamble", "kind": "preamble",
                       "head": f"Chapter {ch}: Preamble", "lines": [], "notes": [], "chapter": ch}
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
        if (not rawl[:1].isspace() and not t.startswith(("(", "[", '"')) and t.upper() != t and not t.endswith(":")
                and nxt < len(lines) and PARA_RX.match(norm(lines[nxt]))):
            pending_head = t
            continue
        cur["lines"].append(t)
    flush()
    return units, notes, chapter


# ---------------------------------------------------------------- the Constitution as enacted (2013)

def tokens(text: str, fold: bool = False) -> str:
    """Word sequence of a unit for comparison across Veritas's two formats: headings, the "N." after a heading
    number, dash forms and spacing around punctuation are ignored; line breaks are ignored."""
    t = re.sub(r"^# ", "", text, flags=re.M)
    t = re.sub(r"^(\d+[A-Z]?)\.(?= )", r"\1", t, flags=re.M)
    t = t.replace("\u2014", "-").replace("\u2013", "-")
    t = re.sub(r"\s*-\s*", " - ", t)
    t = re.sub(r"([;:,.\]\[()])", r" \1 ", t)
    t = " ".join(t.split())
    return t.lower() if fold else t


def body_of(text: str) -> str:
    return "\n".join(text.split("\n")[1:])


def docx_segments(raw: list[str], order: list[str], units: dict) -> dict:
    """Cut the as-enacted .docx into the units of a consolidated text (same keys), by finding each unit's start in
    document order: a section by its number and the first words of its heading, a Schedule paragraph by its number
    after its heading line, a Schedule by its title. Chapter and Part headings are dropped. Returns {key: [lines]}."""
    lines = [norm(l) for l in raw]
    start = next(i for i, l in enumerate(lines) if l.startswith("We the people of Zimbabwe"))
    pos = {}
    i = start
    sched_seen = False
    for k in order:
        u = units[k]
        head = u["text"].split("\n")[0][2:]
        if k == "preamble":
            pos[k] = start
            continue
        m = re.match(r"(\d+[A-Z]?)\. (.*)$", head)
        if k.startswith("sec-"):
            num, words = m.group(1), m.group(2).split()[:2]
            rx = re.compile(rf"^{num}\.?\s+{re.escape(' '.join(words))}", re.I)
        elif k.startswith("chapter-"):
            rx = re.compile(r"^preamble$", re.I)
        elif "-para-" in k:
            num = m.group(1)
            rx = re.compile(rf"^{num}\.(\s|\(|$)")
        else:  # a Schedule
            n = int(k.split("-")[1])
            name = [w for w, v in ORD.items() if v == n][0]
            rx = re.compile(rf"^{name} schedule\b", re.I)
        j = i
        while j < len(lines) and not rx.match(lines[j]):
            j += 1
        if j == len(lines):
            raise ValueError(f"{k}: start not found in the as-enacted text")
        if "-para-" in k:  # the heading line before the number belongs to the paragraph
            h = j - 1
            while not lines[h]:
                h -= 1
            j = h
        pos[k] = j
        i = j + 1
    out = {}
    ks = [k for k in order if k in pos]
    for n, k in enumerate(ks):
        a = pos[k] + 1
        b = pos[ks[n + 1]] if n + 1 < len(ks) else len(lines)
        seg = []
        for l in lines[a:b]:
            if not l:
                continue
            if CHAPTER_RX.match(l) or SCHEDULE_RX.match(l):
                break
            seg.append(l)
        out[k] = seg
    return out


def as_enacted(raw2013: list[str], units: dict, notes: dict, act10_rx: str) -> tuple[dict, dict]:
    """The Constitution as enacted, in the layout of the first consolidation (`units`, Veritas 2018).

    For every unit the 2017 Act did not touch and whose words appear unchanged (same order, same case) in Veritas's
    as-enacted text, the consolidated unit is used: same words, Veritas's consolidated line layout. Every other unit
    (touched by the 2017 Act, or with any difference in words) is taken from the as-enacted text itself, one Word
    paragraph per line. Returns (units, report {key: reason})."""
    lines = [norm(l) for l in raw2013]
    start = next(i for i, l in enumerate(lines) if l.startswith("We the people of Zimbabwe"))
    stream = " " + tokens("\n".join(lines[start:])) + " "
    order = list(units)
    segs = docx_segments(raw2013, order, units)
    out, report = {}, {}
    for k in order:
        u = units[k]
        touched = any(re.search(act10_rx, n) for n in notes.get(k, []))
        if not touched and (" " + tokens(body_of(u["text"])) + " ") in stream:
            out[k] = u
            continue
        head = u["text"].split("\n")[0]
        body = segs[k]
        if "-para-" in k and body:
            body = body[1:] if not PARA_RX.match(body[0]) else body
        out[k] = {"label": u["label"], "kind": u["kind"], "text": "\n".join([head] + body) + "\n"}
        report[k] = "amended in 2017" if touched else (
            "letter case differs" if (" " + tokens(body_of(u["text"]), True) + " ") in stream.lower() else
            "words differ")
    return out, report
