# Structure

| Folder | What it holds |
| --- | --- |
| `constitution/` | The Constitution of Zimbabwe, 2013, with every amendment (one file per section, `sec-180.md`) |
| `chapters/<CC>-<NN>-<slug>/` | A consolidated Act of the Laws of Zimbabwe, by its Chapter number, e.g. `chapters/09-23-criminal-law-codification-and-reform/` is the Criminal Law Code [Chapter 9:23] |
| `acts/<year>/<NNN>-<slug>/` | An Act of Parliament by the year and number of the Act, e.g. `acts/2023/011-labour-amendment/` is the Labour Amendment Act (Act 11 of 2023), as enacted |
| `subsidiary/<year>/<NNN>-<slug>/` | A statutory instrument by its year and number, as published, e.g. `subsidiary/2026/148-public-holidays-and-prohibition-of-business-declaration-of-pub/` is S.I. 148 of 2026; one file per numbered paragraph (`sec-001.md`), the enacting words in `preamble.md`, or `text.md` when it has no numbered paragraphs |

Each act folder holds one file per section (`sec-012-c.md` is section 12C), per Schedule (`schedule-1.md`), the long
title (`long-title.md`), and a `README.md` listing the files and, for a consolidated Act, the amending Acts the
publisher lists. No folder holds more than 1,000 entries.

## Dates

Each version is one commit, dated 12:00 Africa/Harare on the day it took effect, which its `In-force:` trailer
repeats; `In-force-basis:` says where that day comes from:

- `acts-table-commencement`: an Act as enacted, in force on the "Date into force" in Veritas's table of the Acts of
  that year;
- `last-amending-act-commencement`: a consolidated Act, dated the day the last amending Act in its own amendment list
  came into force (by the same tables);
- `title-as-at`: a consolidated Act whose title says "as amended on <date>";
- `own-commencement`: a statutory instrument that names the day it comes into operation;
- `gazette-date`: a statutory instrument that names no day, in force on the day of the Gazette that published it
  (Interpretation Act [Chapter 1:01]); one that commences "on a date to be fixed" is held;
- the Constitution and the acts from ZimLII keep the dates given in their commits (see README.md).

Versions with no reliable date are held back, not dated by guess. No date in this repository is the day we
downloaded anything. `Source-status: secondary copy (Veritas, ...)` marks text taken from Veritas, a
non-governmental publisher, and `Text-source: publisher OCR` text from a PDF whose own text layer shows scanning
errors (we run no OCR).
