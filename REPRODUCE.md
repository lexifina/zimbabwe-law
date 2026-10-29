# How this repository was made (Zimbabwe)

This file is written by the build on 2026-10-29, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Veritas (veritaszim.net): Constitution of Zimbabwe, Word texts | <https://www.veritaszim.net/node/8104> | 2026-10-28 | CC BY-NC-SA 4.0 (footer of every page of www.veritaszim.net: "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License"); the site has no other terms page. Each document says: "Veritas has made every effort to ensure that this updated Constitution is reliable, but cannot take legal responsibility for any errors." |
| Veritas: Act 6 of 2026 as published, SI 117 of 2026, titled list of 2023 statutory instruments, Acts of 2026 | <https://www.veritaszim.net/statutoryinst> | 2026-10-29 | CC BY-NC-SA 4.0 (as above) |
| ZimLII (Zimbabwe Legal Information Institute, on the Laws.Africa Peachjam platform) | <https://zimlii.org> | 2026-10-29 | CC BY-NC 4.0, crediting ZimLII as the source (ZimLII terms of use s. 9, read from the Internet Archive capture 20261012174817 of https://zimlii.org/terms-of-use/) |
| Internet Archive Wayback Machine | <https://web.archive.org> | 2026-10-29 | Archived copies of ZimLII pages; the content licence is ZimLII's |
| ZimLII (on the Laws.Africa Peachjam platform) | <https://zimlii.org> | 2026-10-29 | CC BY-NC 4.0, crediting ZimLII as the source (https://zimlii.org/terms-of-use/) |
| ZimLII (on the Laws.Africa Peachjam platform) | <https://zimlii.org> | 2026-10-29 | CC BY-NC 4.0, crediting ZimLII as the source (https://zimlii.org/terms-of-use/) |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of Zimbabwe | 9 | 2013-05-22 to 2026-07-28 |
| `cyber-data-protection` | Cyber and Data Protection Act, 2021 | 1 | 2022-03-11 to 2022-03-11 |
| `marriages` | Marriages Act, 2022 | 1 | 2022-09-16 to 2022-09-16 |
| `freedom-of-information` | Freedom of Information Act, 2020 | 1 | 2020-07-01 to 2020-07-01 |
| `consumer-protection` | Consumer Protection Act, 2019 | 1 | 2019-12-10 to 2019-12-10 |
| `maintenance-of-peace-order` | Maintenance of Peace and Order Act, 2019 | 1 | 2019-11-15 to 2019-11-15 |
| `insolvency` | Insolvency Act, 2018 | 1 | 2018-06-25 to 2018-06-25 |
| `public-health` | Public Health Act, 2018 | 1 | 2018-08-31 to 2018-08-31 |
| `constitutional-court` | Constitutional Court Act, 2020 | 1 | 2021-05-14 to 2021-05-14 |
| `international-treaties` | International Treaties Act, 2020 | 1 | 2020-07-10 to 2020-07-10 |
| `death-penalty-abolition` | Death Penalty Abolition Act, 2024 | 1 | 2024-12-31 to 2024-12-31 |
| `investment-development-agency` | Zimbabwe Investment and Development Agency Act, 2019 | 1 | 2020-02-07 to 2020-02-07 |
| `coroners-office` | Coroner's Office Act, 2019 | 1 | 2024-09-05 to 2024-09-05 |
| `public-finance-management` | Public Finance Management Act | 2 | 2018-03-14 to 2024-12-31 |
| `administration-of-estates` | Administration of Estates Act | 2 | 2016-12-31 to 2025-02-24 |
| `national-social-security-authority` | National Social Security Authority Act | 2 | 2016-12-31 to 2025-04-11 |
| `civil-aviation` | Civil Aviation Act | 3 | 2016-12-31 to 2024-12-31 |
| `harmful-liquids` | Harmful Liquids Act | 2 | 2016-12-31 to 2025-06-06 |
| `agricultural-finance` | Agricultural Finance Act | 2 | 2016-12-31 to 2024-12-31 |
| `national-peace-and-reconciliation-commission` | National Peace and Reconciliation Commission Act | 1 | 2018-01-05 to 2018-01-05 |
| `land-commission` | Land Commission Act | 1 | 2018-02-26 to 2018-02-26 |
| `veterans-of-the-liberation-struggle` | Veterans of the Liberation Struggle Act, 2020 | 1 | 2020-09-04 to 2020-09-04 |
| `public-procurement-and-disposal-of-public-assets` | Public Procurement and Disposal of Public Assets Act | 2 | 2018-01-01 to 2020-02-07 |

The build made 38 commits:

| Commits | Kind |
| ---: | --- |
| 23 | first version of an act |
| 14 | one law on its in-force day |
| 1 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-29.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 29 laws in the record.
- 68 tags.

## Dates

Each commit is dated at noon (Africa/Harare) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: Not applied as a rule: each amending Act is dated by the commencement date in the amendment table of Veritas's consolidations; the two correction notices (SI 114 of 2023, SI 117 of 2026) by the day of the Gazette that published them, as Veritas records it. https://www.veritaszim.net/node/8104

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `adc729b4c73a8681a69f10e7dbbaa0784cba4c15c6090c4273dd1b1299e94e8d` (3239435 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3d00541d258745461ab52b1b0cb4e1716a27a95d`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

39 versions of 23 acts read back from git on the day each took effect and on the day before: 0 mismatches. Trailers: 0 commits whose trailers git cannot parse. Health: 0 merge commits on main, 0 commit dates that go backwards, 0 commits dated after the build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- Source: Veritas's Word texts, not ZimLII. ZimLII never applied Amendment No. 2 (2021) or No. 3 (2026): its newest archived expression of the Constitution (/akn/zw/act/2013/1, capture 20260121124939) is eng@2017-09-07.
- Licence: Veritas states CC BY-NC-SA 4.0 in its site footer and has no separate terms page; its About page says it "makes public domain information widely available". The repository stays private.
- Units: one file per section, per numbered Schedule paragraph, per Schedule without paragraphs, plus the Preamble and the preamble of Chapter 14. Chapter and Part headings, Veritas's amendment notes and its footnotes are left out of the text; the notes are the credit evidence.
- Typesetting normalised in every version: list bullets dropped (lost in some Word exports), "),(" spaced as "), (", "(3) …]" read as "(3) …" (the bracket of the note below, misplaced). Repealed subsections stay as Veritas shows them ("(3) …"); a repealed section's file is removed.
- As enacted: every provision whose words appear unchanged in Veritas's as-enacted .docx uses the 2018 consolidation's text and layout; the rest is the .docx text itself, broken into lines like the consolidation where the words agree. Where the two exports differ only in letter case (all-capitals headings in one, title case in the other) the consolidation's form is kept.
- The as-enacted s. 180 was checked word for word against the text Veritas appends to its 2018 consolidation ("Section 180 before its amendment by Act 10 of 2017").
- Two-stage commencement: version 1 is dated 22 May 2013, the publication day, when the provisions listed in Sixth Schedule para 3(1) came into operation. The effective date, 22 August 2013, is a version with no change in words, credited to Act 1 of 2013 for the provisions that came into operation then. Chapters 5, 6, 8 and 12 came in partly on each day (para 3(1) names their parts by subject, not by section), so their provisions are not listed on either day.
- Unexplained: Veritas's 2018 consolidation differs from its as-enacted text in ss. 124(1)(b) ("through"/"under"), 218(1)(a) ("appoint"/"employ"), 268(1)(h) and (2), 328(6)(a) ("with in"/"within") and the Third Schedule ("Provincial/Metropolitan"), with no amendment note. They are credited to no law and dated 30 September 2018, the day the consolidation is as amended up to.
- Act 10 of 2017 (Amendment No. 1): commenced 7 September 2017 (Veritas's amendment table). The Constitutional Court's ruling in Gonese v Parliament (CCZ 4/20, 31 March 2020) declared it invalid with the declaration suspended for 180 days; the Senate later passed the Bill. It is a version with no change in words on 31 March 2020, credited to the court for the six provisions Act 10 amended.
- Act 2 of 2021 (Amendment No. 2): commenced 7 May 2021 (amendment table). Every changed provision carries a note naming it, including s. 269, repealed (its note stays under the empty section).
- SI 114 of 2023: the amendment table says Act 2 of 2021 was "corrected by SI 114 of 2023"; the note under s. 268, the one provision that changed between the 2021 and 2023 consolidations, says "SI 144 of 2023". Veritas's titled list of 2023 statutory instruments gives SI 114 of 2023 as the Statute Law Compilation and Revision (Correction of Constitution of Zimbabwe Amendment (No. 2) Act, 2021) Notice, 2023, dated 2023-06-20, so the note is read as a misprint for SI 114 and the change is dated 20 June 2023.
- Act 6 of 2026 (Amendment No. 3): dated 7 July 2026, as in Veritas's amendment table and SI 117 of 2026's explanatory note ("published in the Government Gazette Extraordinary of 7th July, 2026"). Veritas's Acts of 2026 list says gazetted and in force 6 July 2026; the two official-text sources are followed.
- SI 117 of 2026 (Law Reviser's correction under s. 11C of the Statute Law Compilation and Revision Act): Gazette of 28 July 2026, adds to Act 6's s. 20 the repeal of s. 180(3), (4), (4a) and (5). So s. 180 has two versions: 7 July (Act 6: subsections (1) and (2) from the 2026 consolidation, (3) to (5) unchanged from 2023; the new (2) was checked against Act 6 as published) and 28 July (SI 117).
- Part 6 of Chapter 12 (ss. 251 to 253, National Peace and Reconciliation Commission) was repealed by s. 27 of Act 6 of 2026; the note sits under the Part heading and is applied to its three sections.
- Validity: Veritas notes that all three amending Acts are challenged in the Constitutional Court (Act 2 of 2021 for changes made after the Bill's publication; Act 6 of 2026 for extending term limits without a referendum) and that it considers all of them invalid. The history follows the text as published and in force; it takes no view on validity.
- The last version equals Veritas's consolidation as amended up to 28 July 2026, the newest Veritas publishes (retrieved 2026-10-28); Veritas's Acts of 2026 list (to 18 September 2026) names no later constitutional amendment.
- ZimLII acts: chosen by what the archive holds. Every expression ZimLII lists for the Criminal Law (Codification and Reform) Act (2017-03-23, 2019-02-20, 2022-03-11) and the Cyber and Data Protection Act (2022-03-11) has an archived copy.
- Only archived copies are read, only for the acts built. Content licence: CC BY-NC 4.0, crediting ZimLII (terms s. 9).
- Version dates are ZimLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that ZimLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: this is checked per version (verification.json, fidelity).
- Cyber and Data Protection Act: ZimLII's only version is dated 2022-03-11, its page saying "Published on 11 March 2022" and "Commenced on 11 March 2022"; that date is used as ZimLII gives it.
- Part 30-batch2: acts chosen for their weight in practice among the ZimLII acts whose current expression, and every earlier expression ZimLII lists, could be read with its text, and whose newest page lists no amendment ZimLII has not yet applied. Acts that ZimLII still carries only at the Law Development Commission's consolidation as at 31 December 2016 were left out, even where its page shows no later amendment: several such acts have successors made after 2016 that ZimLII also publishes (for example the Marriage Act and the Marriages Act, 2022, or the Insolvency Act and the Insolvency Act, 2018), so a 2016 text cannot be taken as today's law without a check this part does not make. This part takes acts made from 2018 onwards, as ZimLII publishes them, and older acts whose newest ZimLII version is from 2024 or later.
- The acts in this part name ZimLII as their own publisher: the country publisher is Veritas, the source of the Constitution.
- The Persons with Disabilities Act, 2025 is left out: ZimLII marks it "Not commenced".
- Version dates are ZimLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that ZimLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: Lexifina's code checks this per version (verification.json, fidelity).
- Marriages Act: the first version is dated 2022-09-16, the commencement date ZimLII states ("Commenced on 16 September 2022 by Marriages Act, 2022: Commencement"), not 2022-05-27, the date of its expression (Gazette publication).
- Coroner's Office Act: the first version is dated 2024-09-05, the commencement date ZimLII states ("Commenced on 5 September 2024 by Coroner’s Office Act, 2019: Commencement"), not 2020-03-06, the date of its expression (Gazette publication).
- Part 31-batch3: further ZimLII acts under the rule of part 30-batch2: acts enacted after the Law Development Commission's consolidation as at 31 December 2016, as ZimLII publishes them, and older acts whose newest ZimLII version is from 2024 or later; each with every expression ZimLII lists readable and no amendment waiting to be applied.
- The acts in this part name ZimLII as their own publisher: the country publisher is Veritas, the source of the Constitution.
- Version dates are ZimLII's expression dates. Laws.Africa's terminology guide (https://docs.laws.africa/getting-started/terminology-guide) says "Amendments to Principal works come into force on the Commencement date of the Amending work" and that the first point in time is "the work as originally published"; so an amendment's expression is dated by its commencement (in force), and an act's original expression by its publication, which is replaced by the commencement date the page states.
- Credits: a version whose History names exactly one amending law (and no consolidation) between it and the previous version is credited to that law for every provision that changed. Otherwise a provision is credited only to laws that ZimLII's editorial note inside that provision links to; the rest are unexplained (publisher).
- Editorial notes (akn-remark) are left out of the text and used only as credit evidence, except where a provision has no other text (repealed or spent), where the note is the provision's whole printed content.
- Part, Chapter and Division headings are left out; each provision file starts with its own number and heading. Every other text of each version is in a provision file: Lexifina's code checks this per version (verification.json, fidelity).

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote Lexifina's code and the decisions. No model wrote, summarised or transformed legal text: parsing is deterministic code (antiword, pdftotext, the Python standard library).
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and wrappers and chose the acts; the shared Peachjam adapter does the parsing. No model wrote, summarised or transformed legal text.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and wrappers and chose the acts; the shared Peachjam adapter does the parsing. No model wrote, summarised or transformed legal text.
- Claude Code (Claude Opus 5.5, claude-opus-5-5) wrote the configuration and wrappers and chose the acts; the shared Peachjam adapter does the parsing. No model wrote, summarised or transformed legal text.
