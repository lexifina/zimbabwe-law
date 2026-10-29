# Zimbabwe: law history in git

The law of Zimbabwe as a git history: one file per provision, one commit per law on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every paragraph; `git log` lists every change to a provision; `tools/on.py` gives the text in force on any day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `zw/`. The Constitution comes from the dated Word editions published by [Veritas](https://www.veritaszim.net), a Zimbabwean non-profit that publishes the laws of Zimbabwe and the work of Parliament. Other acts come from point-in-time versions published by [ZimLII](https://zimlii.org) (Laws.Africa), read from archived copies of its pages.

**What is in it now**

| Folder | Act | Versions | History | Source |
| --- | --- | ---: | --- | --- |
| `constitution/` | [Constitution of Zimbabwe](https://www.veritaszim.net/node/8104) (2013) | 9 | 2013-05-22 to 2026-07-28 | Veritas |
| `cyber-data-protection/` | [Cyber and Data Protection Act, 2021](https://zimlii.org/akn/zw/act/2021/5) (Act 5 of 2021) | 1 | 2022-03-11 | ZimLII |
| `marriages/` | [Marriages Act, 2022](https://zimlii.org/akn/zw/act/2022/1) (Act 1 of 2022) | 1 | 2022-09-16 | ZimLII |
| `freedom-of-information/` | [Freedom of Information Act, 2020](https://zimlii.org/akn/zw/act/2020/1) (Act 1 of 2020) | 1 | 2020-07-01 | ZimLII |
| `consumer-protection/` | [Consumer Protection Act, 2019](https://zimlii.org/akn/zw/act/2019/5) (Act 5 of 2019) | 1 | 2019-12-10 | ZimLII |
| `maintenance-of-peace-order/` | [Maintenance of Peace and Order Act, 2019](https://zimlii.org/akn/zw/act/2019/9) (Act 9 of 2019) | 1 | 2019-11-15 | ZimLII |
| `insolvency/` | [Insolvency Act, 2018](https://zimlii.org/akn/zw/act/2018/7) (Act 7 of 2018) | 1 | 2018-06-25 | ZimLII |
| `public-health/` | [Public Health Act, 2018](https://zimlii.org/akn/zw/act/2018/11) (Act 11 of 2018) | 1 | 2018-08-31 | ZimLII |
| `constitutional-court/` | [Constitutional Court Act, 2020](https://zimlii.org/akn/zw/act/2020/5) (Act 5 of 2020) | 1 | 2021-05-14 | ZimLII |
| `international-treaties/` | [International Treaties Act, 2020](https://zimlii.org/akn/zw/act/2020/2) (Act 2 of 2020) | 1 | 2020-07-10 | ZimLII |
| `death-penalty-abolition/` | [Death Penalty Abolition Act, 2024](https://zimlii.org/akn/zw/act/2024/4) (Act 4 of 2024) | 1 | 2024-12-31 | ZimLII |
| `investment-development-agency/` | [Zimbabwe Investment and Development Agency Act, 2019](https://zimlii.org/akn/zw/act/2019/10) (Act 10 of 2019) | 1 | 2020-02-07 | ZimLII |
| `coroners-office/` | [Coroner's Office Act, 2019](https://zimlii.org/akn/zw/act/2019/12) (Act 12 of 2019) | 1 | 2024-09-05 | ZimLII |
| `public-finance-management/` | [Public Finance Management Act](https://zimlii.org/akn/zw/act/2009/11) (Act 11 of 2009) | 2 | 2018-03-14 to 2024-12-31 | ZimLII |
| `administration-of-estates/` | [Administration of Estates Act](https://zimlii.org/akn/zw/act/ord/1907/6) (Ordinance 6 of 1907) | 2 | 2016-12-31 to 2025-02-24 | ZimLII |
| `national-social-security-authority/` | [National Social Security Authority Act](https://zimlii.org/akn/zw/act/1989/12) (Act 12 of 1989) | 2 | 2016-12-31 to 2025-04-11 | ZimLII |
| `civil-aviation/` | [Civil Aviation Act](https://zimlii.org/akn/zw/act/1998/7) (Act 7 of 1998) | 3 | 2016-12-31 to 2024-12-31 | ZimLII |
| `harmful-liquids/` | [Harmful Liquids Act](https://zimlii.org/akn/zw/act/1949/27) (Act 27 of 1949) | 2 | 2016-12-31 to 2025-06-06 | ZimLII |
| `agricultural-finance/` | [Agricultural Finance Act](https://zimlii.org/akn/zw/act/1971/6) (Act 6 of 1971) | 2 | 2016-12-31 to 2024-12-31 | ZimLII |
| `national-peace-and-reconciliation-commission/` | [National Peace and Reconciliation Commission Act](https://zimlii.org/akn/zw/act/2017/11) (Act 11 of 2017) | 1 | 2018-01-05 | ZimLII |
| `land-commission/` | [Land Commission Act](https://zimlii.org/akn/zw/act/2017/12) (Act 12 of 2017) | 1 | 2018-02-26 | ZimLII |
| `veterans-of-the-liberation-struggle/` | [Veterans of the Liberation Struggle Act, 2020](https://zimlii.org/akn/zw/act/2020/3) (Act 3 of 2020) | 1 | 2020-09-04 | ZimLII |
| `public-procurement-and-disposal-of-public-assets/` | [Public Procurement and Disposal of Public Assets Act](https://zimlii.org/akn/zw/act/2017/5) (Act 5 of 2017) | 2 | 2018-01-01 to 2020-02-07 | ZimLII |

The `preview` branch also holds the **Criminal Law (Codification and Reform) Act** (`criminal-law-code/`, 3 versions, 2017-03-23 to 2022-03-11). It is not on `main`, because ZimLII has not applied two 2024 amendments (the Criminal Laws Amendment (Protection of Children and Young Persons) Act, 2024 and the Death Penalty Abolition Act, 2024), so its newest version is not today's law.

**Constitution of Zimbabwe**

| In force | Author | What happened |
| --- | --- | --- |
| 2013-05-22 | Act 1 of 2013 (as enacted) | Published as the Schedule to the Constitution of Zimbabwe Amendment (No. 20) Act, 2013; the parts listed in Sixth Schedule para 3(1) came into operation |
| 2013-08-22 | Act 1 of 2013 | The effective date: the rest came into operation. No words changed |
| 2017-09-07 | Act 10 of 2017 | Amendment No. 1 (judicial appointments; ss. 172 to 174, 180, 181, Sixth Schedule para 18) |
| 2018-09-30 | publisher (Veritas): unexplained | Five provisions differ between Veritas's as-enacted text and its 2018 consolidation, with no amendment note |
| 2020-03-31 | CCZ 4/20 (court) | *Gonese v Parliament*: Act 10 of 2017 declared invalid, the declaration suspended. No words changed |
| 2021-05-07 | Act 2 of 2021 | Amendment No. 2 (34 provisions) |
| 2023-06-20 | SI 114 of 2023 | Law Reviser's correction of Act 2 of 2021 (s. 268) |
| 2026-07-07 | Act 6 of 2026 | Amendment No. 3 (30 provisions; Part 6 of Chapter 12 repealed) |
| 2026-07-28 | SI 117 of 2026 | Law Reviser's correction of Act 6 of 2026 (s. 180(3) to (5) repealed) |

**Cyber and Data Protection Act, 2021**

| In force | Author |
| --- | --- |
| 2022-03-11 | Act 5 of 2021 (as enacted; ZimLII's only version, "Published on 11 March 2022", "Commenced on 11 March 2022") |

Each folder's `README.md` lists every provision, how often it changed and when.

**Validity.** Veritas notes that all three amending Acts have been challenged in the Constitutional Court: Act 10 of 2017 because the Senate had not passed it by a two-thirds majority (the Court agreed, suspended its declaration, and the Senate later passed the Bill); Act 2 of 2021 because the Bill was substantially changed after publication; Act 6 of 2026 because it extended presidential and parliamentary term limits without a referendum. Veritas considers all of them invalid. This history follows the text as published and applied; it takes no view on validity.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did section 180 say on 2017-01-01? | `python tools/on.py 2017-01-01 constitution sec-180` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2017-01-01T23:59:59Z" main -- constitution/sec-180.md):constitution/sec-180.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2017-01-01T23:59:59Z" main -- constitution/sec-180.md; git show "$($r):constitution/sec-180.md"` |
| Which law wrote each line? | `git blame constitution/sec-180.md` |
| Every change, word by word | `git log -p --word-diff constitution/sec-180.md` |
| Every law in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one law changed | `git show law/<key>` (tags `law/<key>` mark each law's commit, e.g. `law/act-2021-2`) |
| The whole Constitution on a date | `python tools/on.py 2021-05-07 constitution` |
| Which law gave a provision its wording on a date | `python tools/on.py --law 2026-07-10 constitution sec-180` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Dates

- Each commit is dated at **noon, Africa/Harare, on the day the change took effect**. The day is also in the `In-force:` trailer, which the tools read.
- **Amending Acts** are dated by the commencement date in the amendment table of Veritas's consolidations (Act 10 of 2017: 7.9.2017; Act 2 of 2021: 7.5.2021; Act 6 of 2026: 7.7.2026). The two **correction notices** of the Law Reviser are dated by the Gazette that published them: SI 114 of 2023 on 20 June 2023 (Veritas's titled list of 2023 statutory instruments) and SI 117 of 2026 on 28 July 2026 (the notice itself).
- **Two-stage commencement in 2013.** The Constitution was published on 22 May 2013 (the "publication day"); paragraph 3(1) of the Sixth Schedule brought some Chapters into operation that day, and the rest came into operation on 22 August 2013, when the President elected in the first elections took office (the "effective date"). The first commit is 22 May 2013; the 22 August commit changes no words and names the provisions that came into operation then. Chapters 5, 6, 8 and 12 came in partly on each day, described by subject rather than by section, so they are named on neither.
- Unexplained differences are dated by the day the consolidation that first shows them is "as amended up to".
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a law that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## How it is checked

- Every version is read back from git on the day it took effect and on the day before (`tools/check_repo.py`); both must match `corpus.json`. Results are in `REPRODUCE.md`.
- **Against Veritas today:** the last version is, provision for provision, Veritas's consolidation "as amended up to 28th July, 2026", the newest it publishes.
- **Between consolidations, every change is accounted for:** replaying the credited changes on each consolidation gives the next one exactly. Every changed provision carries a Veritas note naming the law, except the five 2018 differences, which are labelled unexplained.
- **Section 180** was checked twice: the as-enacted text word for word against the copy Veritas appends to its 2018 consolidation ("Section 180 before its amendment"), and the subsection (2) that Act 6 of 2026 substituted against the Act as published.
- The repository is rebuilt from the same data a second time and must give identical hashes.

## What "author" means

The author of a commit is the law that made the change, with an e-mail address that cannot exist, so `git blame` and `git log --author` name laws. The committer is always Lexifina.

- **Credits come only from Veritas's own notes.** Under every amended provision Veritas prints a note such as "[Subsection amended by s. 3 of Act No. 2 of 2021]". A changed provision is credited to a law only if its note names that law and the law took effect between the two consolidations compared; any other difference is committed by the publisher and labelled "unexplained".
- **The first commit** is the Constitution as enacted (Act 1 of 2013).
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each change made.

## What it does not show

- **Only what Veritas's editions show.** The history is built from five dated editions (as enacted, and as amended up to 30 September 2018, 7 May 2021, 20 June 2023 and 28 July 2026) plus the amendment notes in them; changes are placed on the dates those notes and tables give.
- **The five unexplained 2018 differences** (ss. 124(1)(b), 218(1)(a), 268(1)(h) and (2), 328(6)(a), and the heading of the provincial council oath in the Third Schedule) may be corrections of errors in one of Veritas's texts rather than changes in the law; nothing in the sources says which.
- **Editorial notes and footnotes** are left out of the text and used only for credits. Repealed subsections stay as Veritas prints them ("(3) …"); a repealed section's file is removed.
- **Headings above the provision** (Chapter, Part) are left out; each file starts with its own number and heading. Images in the First Schedule (flag, anthem score, coat of arms) are marked `[image]`.
- **No OCR.** Veritas's PDF of the Constitution as enacted is a scan and is not used; its Word edition is.
- **ZimLII** ([zimlii.org](https://zimlii.org)) was not used for the Constitution: its newest version (archived January 2026) is still the text of 7 September 2017, without Amendments No. 2 and No. 3.
- **Acts from ZimLII** show only the versions ZimLII publishes and the Internet Archive holds; ZimLII's dates are used as it gives them (an amendment's version is dated by its commencement). Credits come from ZimLII's History and its editorial notes, as for every Laws.Africa country.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

The ZimLII acts come from Lexifina's code (archived captures only, pinned in `tools/sources.json`) and Lexifina's code, through Lexifina's code, the shared adapter for every Laws.Africa legal information institute.

## Sources

| Source | What it gives | Used for |
| --- | --- | --- |
| [Veritas: the Constitution](https://www.veritaszim.net/node/8104) | The Constitution as enacted (Word, .docx) and consolidated as amended up to 2018, 2021, 2023 and 2026 (Word, .doc), each with an amendment table and a note under every amended provision | The text, dates and credits of every version |
| [Veritas: Acts and statutory instruments](https://www.veritaszim.net/statutoryinst) | Act 6 of 2026 as published, SI 117 of 2026, the titled list of 2023 statutory instruments | Dating the correction notices; checking s. 180 |
| [ZimLII](https://zimlii.org) (Laws.Africa) | Point-in-time versions of acts, their History and editorial notes | The text, dates and credits of the other acts (not the Constitution, see above) |
| [Internet Archive](https://web.archive.org/) | Archived copies of ZimLII's pages, pinned by capture time and sha256 in `tools/sources.json` | Reading them |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

See [LICENSE](LICENSE). Constitution: Veritas (www.veritaszim.net), licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International licence (CC BY-NC-SA 4.0), as stated on the Veritas website. Veritas has no separate terms page; each of its editions says that Veritas "cannot take legal responsibility for any errors". Other acts: ZimLII (https://zimlii.org), licensed under the Creative Commons Attribution-NonCommercial 4.0 International licence (CC BY-NC 4.0), crediting ZimLII as the source (ZimLII terms of use, s. 9).

This repository is not legal advice. The Constitution recognises sixteen official languages and provides that the English text prevails over the others; the text here is English, so there is no separate summary in another language.
