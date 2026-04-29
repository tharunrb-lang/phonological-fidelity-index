# Phonetic Siblings
### Convergent Preservation of Proto-Indo-European Consonants in French and Hindi/Sanskrit Against the Germanic Shift

**Tharun Rathod** · B.Tech Electrical Engineering (2027) · IIT Roorkee  
Independent Research · 2026

---

## What This Paper Is About

French *dent* and Hindi *dant* both mean tooth. French *tu* and Hindi *tu* both mean you. French *père* and Hindi *pita* both mean father. These are not coincidences or borrowings — they are the same words, inherited from a 5,000-year-old ancestor language, preserved independently by two branches that happen to never have met.

Meanwhile, English says *tooth*, *thou*, and *father* — because English underwent **Grimm's Law** around 1000 BCE, a systematic consonant shift that converted PIE `*p → f`, `*d → t`, and `*t → th` across the entire Germanic branch. French and Hindi did not. This paper documents, formalises, and quantifies that fact.

---

## Core Findings

| Consonant Class | French PFI | Hindi/Sanskrit PFI | English PFI |
|---|---|---|---|
| `*p` (father, foot, full) | 0.917 | **1.000** | 0.083 |
| `*d` (tooth, ten, two) | 0.900 | **1.000** | 0.400 |
| `*t` (you, three) | 1.000 | **1.000** | 0.000 |
| **Combined Grimm classes** | **0.923** | **1.000** | **0.192** |
| `*m`, `*n`, `*s` (control) | 0.962 | 1.000 | 1.000 |

The gap between Hindi/Sanskrit and English in Grimm-affected classes: **80.8 percentage points.**  
The gap between French and English: **73.1 percentage points.**  
In the stable control classes, all three languages score identically. The differential is entirely concentrated where Grimm's Law operated.

---

## Two New Theoretical Constructs

**Convergent Preservation** — when two branches independently retain an ancestral phonological feature while a third branch systematically loses it. French and Hindi are phonetically similar not because they influenced each other (they had virtually zero contact), but because *neither underwent Grimm's Law*. They converge on the same ancient sounds through independent inheritance.

**Phonetic Triangulation** — a three-branch comparative method. When French and Hindi both preserve the same PIE consonant, and English shows the predicted Grimm shift, all three data points simultaneously (a) confirm the cognate relationship, (b) identify which branch shifted, and (c) reconstruct the PIE form. Higher confidence than any two-branch comparison.

---

## The Instrument: Phonological Fidelity Index (PFI)

The PFI scores how faithfully a modern language preserves the initial consonant of its PIE ancestor root:

| Score | Meaning | Example |
|---|---|---|
| **1.0** | Full preservation | French *père* from PIE `*p` |
| **0.5** | Partial / conditioned shift | French *cinq* from PIE `*penkwe` (palatalisation) |
| **0.0** | Documented systemic shift | English *tooth* from PIE `*d` (Grimm's Law) |

Branch-level PFI = arithmetic mean of all scored entries. Computed separately for Grimm-affected and stable classes to isolate the effect.

---

## Dataset

- **Source:** Swadesh 200-word list (universal, pre-existing, researcher-independent)
- **Starting pool:** 146 candidate entries from 200 concepts (73%)
- **Final dataset:** 41 strictly verified entries after six-criterion cleaning
- **Removal policy:** Entries removed only for clear etymological reasons — never for producing an inconvenient score

**Six inclusion criteria (all must pass):**
1. All three branches descend from the same PIE root
2. Hindi/Sanskrit form is genuine Indo-Aryan inheritance (no Persian/Arabic substitution)
3. English form is native Germanic (no Latin/French borrowing)
4. French form descends via Latin from the PIE root
5. Meanings are semantically aligned across branches
6. Phonological correspondence is traceable and not speculative

**Why Hindi sometimes uses Sanskrit:** ~25% of everyday Hindi vocabulary is Persian/Arabic loanwords from the Mughal period. When a common Hindi word is a loan, the Sanskrit form is used and marked `[skt]`. The strict cleaning reveals that when loanword contamination is removed, the Indo-Aryan branch actually outperforms the Italic branch in PIE consonant fidelity.

---

## The *tu* Example (The Whole Thesis in One Word)

| Language | Word | PIE root |
|---|---|---|
| Hindi | **tu** | `*tuh₂` |
| French | **tu** | `*tuh₂` |
| English | **thou** → (now archaic) | `*tuh₂` → Grimm `*t → th` |

Same spelling. Same pronunciation. Same meaning. Same 5,000-year-old PIE root. Two branches kept it; one shifted it by law.

---

## Repository Contents

```
phonetics.pdf              — Full paper (50 pages)
pfi_compute.py             — Python script encoding all 41 entries; reproduces all scores
pfi_results.csv            — Scored dataset in CSV format
README.md                  — This file
```

---

## Reproducing the Results

```bash
python pfi_compute.py
```

The script encodes all 41 entries directly and prints:
- Overall PFI per branch
- Grimm-class PFI (`*p`, `*d`, `*t` combined)
- Stable-class PFI (`*m`, `*n`, `*s` combined)

Expected output:
```
French: 0.915 (n=41)
Hindi/Sanskrit: 0.939 (n=41)
English: 0.671 (n=41)
Grimm FR=0.923, HI=1.000, EN=0.192
Stable FR=0.962, HI=1.000, EN=1.000
```

---

## Implications

**For language learners:** A Hindi speaker learning French already possesses the PIE-derived consonant inventory preserved in French. The *p* in *pita* is the same consonant as the *p* in *père*. The *d* in *dant* is the same as the *d* in *dent*. These are not similarities to memorise — they are shared inheritances to recognise. A curriculum built around the 41 verified cognates could substantially reduce phonological learning burden.

**For PIE reconstruction:** When French and Hindi independently preserve the same consonant from the same PIE root, and English shows the predicted Grimm shift, the three-branch combination provides higher reconstruction confidence than any two-branch comparison. Hindi/Sanskrit's perfect 1.000 Grimm-class score makes it a particularly strong reconstruction anchor.

**For cross-cultural understanding:** The perceived phonological "foreignness" between French and Hindi is driven by different writing systems, different loanword overlays, and geographic separation — not by genuine ancestral distance at the level of core vocabulary. At the consonant level of inherited words, they are closer to each other than either is to English.

---

## Known Limitations

- PFI scores only the **initial consonant** of each entry. Medial consonants, final consonants, and vowels are not measured.
- The `*t` class has only **n=2** entries; the `*b` aspirate class has **n=1**. Results for these classes should be treated with caution pending dataset expansion.
- PFI scores are **descriptive arithmetic means**, not inferential statistics. The 80.8 percentage point differential is established by Grimm's Law theoretically; formal significance testing awaits dataset expansion toward 150–200 entries.
- The **0.0% Shifted rate for French and Hindi/Sanskrit** is a methodological consequence, not a discovery: the cleaning criteria structurally exclude entries where either non-Germanic branch has failed to transmit the PIE consonant. English's 26.8% Shifted rate, by contrast, is a genuine empirical finding — Grimm-shifted native Germanic entries are retained because the shift is what the study measures.
- Sanskrit's merger of PIE `*e` and `*o` into `a` creates systematic vowel differences (e.g., *dant* vs *dent*) that are predictable and do not affect the consonant-level analysis, but would require a separate framework if vowels were to be measured.

---

## Proposed Follow-Up Experiment (Section 15 of paper)

A psycholinguistic experiment is proposed to test **Corollary 1** (that French speakers will find Hindi phonology more intuitive than English speakers will):

- **3 groups:** native French speakers, native English speakers, native Hindi speakers (baseline)
- **3 conditions:** Grimm-affected Hindi words (`dant`, `do`, `tu`), stable Hindi words (`naam`, `naak`), Persian/Arabic loanword controls
- **Task:** Rate phonological similarity to a prime word in their native language (1–7 Likert)
- **Prediction:** French speakers rate Grimm-affected Hindi words significantly higher than English speakers; no difference in stable or loanword conditions
- **Analysis:** 2×3 mixed ANOVA; item-level regression on PFI differential

---

## Citation

```
Rathod, Tharun (2026). Phonetic Siblings: Convergent Preservation of Proto-Indo-European
Consonants in French and Hindi/Sanskrit Against the Germanic Shift. Working Paper,
Independent Research, IIT Roorkee.
```

---

*"Saying tu and tu, or sapta and sept, out loud back to back is not coincidence. It is the same word, carried by two branches of the same family, across five thousand years of complete separation."*
