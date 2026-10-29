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
    s = s.replace("),(", "), (")                      # "subsections (3),(4), (5)": one spacing for lists
    s = re.sub(r"^•\s*", "", s)                    # list bullets: Word auto-bullets are lost in some exports
    s = re.sub(r"^(\(\d+[a-z]?\)) …\]$", r"\1 …", s)  # "(3) …]": the bracket of the note below, misplaced
    return s


NOTE_RX = re.compile(r"^\[[^\]]*\b(amended|substituted|inserted|repealed|corrected|renumbered|added)\b.*"
                     r"\b(Act|SI|S\.I\.|Statutory Instrument)\b", re.I)
# raw line, column 0: "43A\tRegistration of Voters" (2026 has "159A\xa0\xa0Delimitation Commission")
SECTION_RX = re.compile(r"^\t?(\d{1,3}[A-Z]?)(?:\t|\xa0)+(\S.*)$")
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
    cur = {"key": "preamble", "label": "Preamble", "kind": "preamble", "head": "Preamble", "lines": [],
           "chapter": "preamble"}
    order = []
    ch = "preamble"
    sched = None          # (number, heading) while inside a Schedule
    in_arrangement = False

    part_notes: list = []   # notes under a Part heading ("[Part 6 repealed by ...]") apply to its sections

    def flush():
        if cur is None:
            return
        body = [x for x in cur["lines"] if x]
        if cur["key"] == "_heading":
            if body:
                raise ValueError(f"text between a Chapter or Part heading and its first section: {body[:3]}")
            return
        if not body:
            # a repealed section ("251 …", or a heading with only its note): no text, but its notes are evidence
            if cur.get("notes") and cur["key"] not in units:
                notes[cur["key"]] = cur["notes"]
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
                flush()
                cur = {"key": "_heading", "label": "", "kind": "", "head": "", "lines": [], "notes": []}
                part_notes = []
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
                       "head": f"{num}. {head}", "lines": [], "notes": list(part_notes), "chapter": ch}
                continue
            if is_note(t):
                if cur["key"] == "_heading":
                    part_notes.append(t)
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
        # a heading wrapped over two column-0 lines ("Parliament not to deal with ... except on" / "recommendation of
        # Vice-President, ..."), the second followed by the numbered line
        if (not rawl[:1].isspace() and not t.startswith(("(", "[", '"')) and t.upper() != t
                and not re.search(r"[.;:—,]$", t) and nxt < len(lines) and not lines[nxt][:1].isspace()):
            t2 = norm(lines[nxt])
            n2 = nxt + 1
            while n2 < len(lines) and not norm(lines[n2]):
                n2 += 1
            if (t2 and not PARA_RX.match(t2) and t2[:1].islower() and n2 < len(lines)
                    and PARA_RX.match(norm(lines[n2]))):
                pending_head = f"{t} {t2}"
                i = nxt + 1
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


PART_RX = re.compile(r"^part\s*(\d+|[IVX]+)\b", re.I)
SCHED_HEAD_RX = {n: re.compile(rf"^{w} schedule\s*(\(|$)", re.I) for w, n in ORD.items()}


def docx_norm_lines(raw: list[str]) -> list[str]:
    """The as-enacted .docx, normalised: `norm`, plus the PDF line-break hyphen spacing of this export
    ("Vice- President" -> "Vice-President"; the consolidations never have a letter, hyphen, space, letter)."""
    return [re.sub(r"(?<=[A-Za-z])- (?=[A-Za-z])", "-", norm(l)) for l in raw]


def _fold(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def docx_segments(raw: list[str], order: list[str], units: dict) -> dict:
    """Cut the as-enacted .docx into the units of a consolidated text (same keys, same order).

    Each unit's start is searched in document order, from the end of the previous unit:
    - a section: its number and the first two words of its heading ("124. Composition", "47 Chapter 4");
    - a Chapter's preamble: a line "Preamble";
    - a Schedule paragraph: its heading line (as in the consolidation, letter case and punctuation aside) followed by
      a line starting with its number; the arrangement of paragraphs ("1.  Interpretation in Fifth Schedule.") never
      matches, because there the number comes first;
    - a Schedule: "<ordinal> SCHEDULE" followed by "(" or the end of the line (not the arrangement's
      "FIRST SCHEDULE:  National Flag ..."); its section references and its title are skipped.
    Inside a segment, Part headings are skipped with their title line, and a Chapter or Schedule heading ends it.
    Returns {key: [lines of the unit's body]} (no heading line)."""
    lines = docx_norm_lines(raw)
    start = next(i for i, l in enumerate(lines) if l.startswith("We the people of Zimbabwe"))

    def next_text(j: int) -> int:
        while j < len(lines) and not lines[j]:
            j += 1
        return j

    pos: dict = {}      # key -> index of the first body line
    i = start
    for k in order:
        u = units[k]
        head = u["text"].split("\n")[0][2:]
        if k == "preamble":
            pos[k] = start
            continue
        j = i
        if k.startswith("sec-"):
            m = re.match(r"(\d+[A-Z]?)\. (.*)$", head)
            rx = re.compile(rf"^{m.group(1)}\.?\s+{re.escape(' '.join(m.group(2).split()[:2]))}", re.I)
            while j < len(lines) and not rx.match(lines[j]):
                j += 1
            body = j + 1
        elif k.startswith("chapter-"):
            while j < len(lines) and lines[j].lower() != "preamble":
                j += 1
            body = j + 1
        elif "-para-" in k:
            m = re.match(r"(\d+[A-Z]?)\. (.*)$", head)
            want = _fold(m.group(2))
            num = re.compile(rf"^{m.group(1)}\.(\s|\(|$)")
            while j < len(lines):
                if lines[j] and _fold(lines[j]) == want:
                    n = next_text(j + 1)
                    if n < len(lines) and num.match(lines[n]):
                        break
                j += 1
            body = j + 1
        else:
            rx = SCHED_HEAD_RX[int(k.split("-")[1])]
            while j < len(lines) and not rx.match(lines[j]):
                j += 1
            body = next_text(j + 1)
            if body < len(lines) and lines[body].startswith("(") and "(" not in lines[j]:
                body = next_text(body + 1)          # "(Sections 94, 104, ...)" on its own line
            body = next_text(body) + 1              # the Schedule's title
        if j >= len(lines):
            raise ValueError(f"{k}: start not found in the as-enacted text")
        pos[k] = (j, body)
        i = body
    out = {}
    ks = [k for k in order if k in pos]
    for n, k in enumerate(ks):
        a = pos[k][1] if k != "preamble" else start
        b = pos[ks[n + 1]][0] if n + 1 < len(ks) else len(lines)
        seg = []
        j = a
        while j < b:
            l = lines[j]
            j += 1
            if not l:
                continue
            if CHAPTER_RX.match(l) and l.lower().startswith("chapter") or any(r.match(l) for r in SCHED_HEAD_RX.values()):
                break
            if PART_RX.match(l):
                rest = PART_RX.sub("", l).strip()
                if not rest:                         # the title is on the next line
                    t = next_text(j)
                    if t < b and lines[t].upper() == lines[t] or (t < b and "[image]" in lines[t]):
                        j = t + 1
                continue
            seg.append(l)
        out[k] = seg
    return out


def _wrapped(prev: str, cur: str) -> bool:
    """A PDF line wrap kept in the .docx: the line goes on from the one before it."""
    if not prev or not cur:
        return False
    if cur[0].islower():
        return True
    if prev[-1] in ".;:—!?\"']" or prev.endswith((" and", " or")):
        return False
    return not re.match(r'^("|\[|\d+[A-Z]?\.)', cur)


def relayout(ref_lines: list[str], src_lines: list[str]) -> list[str]:
    """The words of `src_lines` (the as-enacted text), broken into lines like `ref_lines` (the consolidation):
    where the two texts agree word for word, a line starts where the consolidation starts one; elsewhere, where the
    .docx starts a paragraph that is not a PDF line wrap. Only line breaks move; every word comes from the source."""
    from difflib import SequenceMatcher
    ref, ref_start = [], []
    for l in ref_lines:
        for n, w in enumerate(l.split()):
            ref.append(w)
            ref_start.append(n == 0)
    src, src_start = [], []
    prev = ""
    for l in src_lines:
        for n, w in enumerate(l.split()):
            src.append(w)
            src_start.append(n == 0 and not _wrapped(prev, l))
        prev = l
    breaks = {0}
    sm = SequenceMatcher(None, ref, src, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            breaks.update(j1 + d for d in range(i2 - i1) if ref_start[i1 + d])
        elif tag in ("replace", "insert"):
            breaks.update(j for j in range(j1, j2) if src_start[j])
            if tag == "replace" and ref_start[i1]:
                breaks.add(j1)
    out, cur = [], []
    for j, w in enumerate(src):
        if j in breaks and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(w)
    if cur:
        out.append(" ".join(cur))
    # a line that differs from a consolidation line only in letter case takes the consolidation's form (all-capitals
    # headings in one export, title case in the other: Word formatting, not wording)
    folded = {l.casefold(): l for l in ref_lines}
    return [folded.get(l.casefold(), l) for l in out]


def as_enacted(raw2013: list[str], units: dict, notes: dict, act10_rx: str) -> tuple[dict, dict]:
    """The Constitution as enacted, in the layout of the first consolidation (`units`, Veritas 2018).

    - A unit the 2017 Act did not touch, whose words appear unchanged (same order) in Veritas's as-enacted text, is
      the consolidated unit: same words, the consolidation's line layout. Letter case is compared too, except where
      the two exports differ only in letter case (all-capitals headings in one, sentence case in the other: Word
      formatting, not wording); there the consolidation's form is kept.
    - Every other unit (touched by the 2017 Act, or with any difference in words) is the as-enacted text itself, its
      lines broken like the consolidation's wherever the words agree (`relayout`).
    Returns (units, report {key: reason})."""
    lines = docx_norm_lines(raw2013)
    start = next(i for i, l in enumerate(lines) if l.startswith("We the people of Zimbabwe"))
    stream = " " + tokens("\n".join(lines[start:])) + " "
    stream_fold = stream.lower()
    order = list(units)
    segs = docx_segments(raw2013, order, units)
    out, report = {}, {}
    for k in order:
        u = units[k]
        touched = any(re.search(act10_rx, n) for n in notes.get(k, []))
        body = " " + tokens(body_of(u["text"])) + " "
        if not touched and body in stream:
            out[k] = u
            continue
        if not touched and body.lower() in stream_fold:
            out[k] = u
            report[k] = "letter case differs only: consolidation's form kept"
            continue
        head = u["text"].split("\n")[0]
        seg = segs[k]
        if not seg:
            raise ValueError(f"{k}: empty as-enacted segment")
        new = relayout(body_of(u["text"]).rstrip("\n").split("\n"), seg)
        out[k] = {"label": u["label"], "kind": u["kind"], "text": "\n".join([head] + new) + "\n"}
        report[k] = ("amended in 2017" if touched else
                     "same text (the exports differ only in images or layout)" if out[k]["text"] == u["text"] else
                     "words differ")
    return out, report


