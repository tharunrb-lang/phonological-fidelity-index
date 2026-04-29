"""
PIE Cognate Dataset — Strictly Cleaned Version
Tharun Rathod · IIT Roorkee · 2026

Cleaning criteria (ALL must hold for inclusion):
  1. French, Hindi, and English all descend from the SAME PIE root.
  2. Hindi is a genuine Indo-Aryan inheritance (no Persian/Arabic loans or modern replacements).
  3. English is native Germanic (no Latin/French borrowings).
  4. French descends via Latin from the PIE root (no semantic drift or unrelated substitution).
  5. Meanings across all three are semantically aligned.
  6. Phonological correspondence is traceable (not speculative).

Removal: applied if ANY criterion fails. Uncertain → removed.
"""

import csv
from collections import defaultdict

# ---------------------------------------------------------------------------
# CLEAN_DATA  –  41 entries passing ALL criteria
# Corrections applied:
#   • "foot":      Hindi "pav / pada"  → "pada [skt]"  (pada is the attested Sanskrit cognate)
#   • "birth/kin": French "naiss."     → "naissance"   (full spelling)
#   • "age/ever":  English "ever/age"  → "ever"        (remove Latin-derived 'age')
#   • "nine":      PIE root "*hewno"   → "*h1newn"     (standard Leiden notation)
#   • "eye":       PIE root "*hokw-"   → "*okw-"       (corrected laryngeal)
# ---------------------------------------------------------------------------

CLEAN_DATA = [
    # concept           PIE root       cl  French form    fr_pfi  Hindi form        hi_pfi  English form   en_pfi  tag
    # ── PIE *p ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("father", "*ph2ter", "p", "père", 1.0, "pita [skt]", 1.0, "father", 0.0, "p"),
    # père < Lat. pater; pitā < Skt. pitṛ; father < OE fæder — all *ph2ter; Grimm p→f in Gmc ✓
    ("foot", "*pods", "p", "pied", 1.0, "pada [skt]", 1.0, "foot", 0.0, "p"),
    # pied < Lat. pes/pedis; pada < Skt. pada; foot < OE fōt — all *pods; Grimm p→f ✓
    # CORRECTION: original had "pav / pada" — "pav" is ambiguous; canonical Skt. cognate is "pada"
    ("five", "*penkwe", "p", "cinq", 0.5, "pānch", 1.0, "five", 0.0, "p"),
    # cinq < Lat. quinque (*p→qu in Latin, fr_pfi=0.5); pānch < Skt. pañca; five < OE fīf ✓
    ("full", "*pleh1-", "p", "plein", 1.0, "pūrā", 1.0, "full", 0.0, "p"),
    # plein < Lat. plenus; pūrā < Skt. pūrṇa; full < OE full ✓
    ("feed / pasture", "*peh2-", "p", "pâture", 1.0, "pālnā", 1.0, "feed", 0.0, "p"),
    # pâture < Lat. pastura; pālnā < Skt. pāl- (to nurture); feed < OE fēdan < PGmc *fōdijaną
    # All from *peh2- "to protect/shepherd/feed"; Grimm p→f in Gmc ✓
    (
        "before / for",
        "*pro-",
        "p",
        "pour / pro-",
        1.0,
        "pra- [skt]",
        1.0,
        "fore",
        0.5,
        "p",
    ),
    # pour < Lat. pro; pra- < Skt. pra- (prefix "forward/before"); fore < OE fore < *pro-; Grimm p→f ✓
    # ── PIE *d ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("tooth", "*dant-", "d", "dent", 1.0, "dant", 1.0, "tooth", 0.0, "d"),
    # dent < Lat. dens/dentis; dant < Skt. danta; tooth < OE tōþ; Grimm d→t ✓
    ("ten", "*dekmt", "d", "dix", 1.0, "das", 1.0, "ten", 0.0, "d"),
    # dix < Lat. decem; das < Skt. daśa; ten < OE tīen; Grimm d→t ✓
    ("two", "*dwoh1", "d", "deux", 1.0, "do", 1.0, "two", 0.0, "d"),
    # deux < Lat. duo; do < Skt. dvi/dvau; two < OE twā ✓
    ("door", "*dwer-", "d", "porte", 1.0, "dwār", 1.0, "door", 1.0, "d"),
    # porte < Lat. porta (dw→p in Latin); dwār < Skt. dvāra; door < OE duru ✓
    ("do / put", "*dheh1-", "d", "faire", 0.5, "dharnā", 1.0, "do", 1.0, "d"),
    # faire < Lat. facere (*dheh1- "to put/do"); dharnā < Skt. dhā- "to place"; do < OE dōn ✓
    # ── PIE *t ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("you (singular)", "*tuh2", "t", "tu", 1.0, "tu", 1.0, "thou", 0.0, "t"),
    # tu < Lat. tu; tu < Skt. tvam (reduced); thou < OE þū; Grimm t→þ ✓
    ("three", "*treyes", "t", "trois", 1.0, "teen", 1.0, "three", 0.0, "t"),
    # trois < Lat. tres; teen < Skt. tri/trīṇi; three < OE þrēo; Grimm t→þ ✓
    # ── PIE *m ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("mother", "*mater", "m", "mère", 1.0, "mā", 1.0, "mother", 1.0, "m"),
    # mère < Lat. mater; mā < Skt. mātā; mother < OE mōdor ✓
    ("mind", "*men-", "m", "mental", 1.0, "man", 1.0, "mind", 1.0, "m"),
    # mental < Lat. mentalis < mens; man < Skt. manas "mind/soul"; mind < OE gemynd ✓
    ("great / much", "*meg-", "m", "majeur", 1.0, "mahā [skt]", 1.0, "much", 1.0, "m"),
    # majeur < Lat. major < magnus; mahā < Skt. mahā- "great"; much < OE mycel < PGmc *mikilaz ✓
    ("moon / month", "*meh1ns-", "m", "mois", 1.0, "māh", 1.0, "moon", 1.0, "m"),
    # mois < Lat. mensis; māh < Skt. māsa; moon < OE mōna ✓
    # ── PIE *n ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("name", "*nomen", "n", "nom", 1.0, "naam", 1.0, "name", 1.0, "n"),
    # nom < Lat. nomen; naam < Skt. nāman; name < OE nama ✓
    ("new", "*newos", "n", "nouveau", 1.0, "nayā", 1.0, "new", 1.0, "n"),
    # nouveau < Lat. novus; nayā < Skt. nava; new < OE nīwe ✓
    ("nose", "*nas-", "n", "nez", 1.0, "naak", 1.0, "nose", 1.0, "n"),
    # nez < Lat. nasus; naak < Skt. nāsā; nose < OE nosu ✓
    ("not / negation", "*ne-", "n", "ne", 1.0, "nahī", 1.0, "not", 1.0, "n"),
    # ne < Lat. ne/non; nahī < Skt. na (extended); not < OE naht/ne ✓
    ("nine", "*h1newn", "n", "neuf", 1.0, "nau", 1.0, "nine", 1.0, "n"),
    # neuf < Lat. novem; nau < Skt. nava; nine < OE nigon ✓
    # CORRECTION: original PIE root label "*hewno" → standard "*h1newn"
    ("naked", "*nogw-", "n", "nu", 0.5, "nangā", 1.0, "naked", 1.0, "n"),
    # nu < Lat. nudus; nangā < Skt. nagna; naked < OE nacod ✓
    # ── PIE *s ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("seven", "*septm", "s", "sept", 1.0, "sāt", 1.0, "seven", 1.0, "s"),
    # sept < Lat. septem; sāt < Skt. sapta; seven < OE seofon ✓
    ("sun", "*sewol-", "s", "soleil", 1.0, "sūraj", 1.0, "sun", 1.0, "s"),
    # soleil < Lat. sol; sūraj < Skt. sūrya; sun < OE sunne ✓
    ("self", "*swe-", "s", "se / soi", 1.0, "apnā [skt sva]", 1.0, "self", 1.0, "s"),
    # se/soi < Lat. se/sui; apnā < Skt. sva via Prakrit appa + -nā; self < OE self ✓
    # ── PIE *k / *kw / *gw ───────────────────────────────────────────────────────────────────────────────────
    ("who", "*kwo-", "k", "qui", 1.0, "kaun", 1.0, "who", 0.5, "k"),
    # qui < Lat. qui; kaun < Skt. kaḥ/kas; who < OE hwā; Grimm k→hw ✓
    ("four", "*kwetwor-", "k", "quatre", 1.0, "chār", 0.5, "four", 0.0, "k"),
    # quatre < Lat. quattuor; chār < Skt. catur; four < OE fēower; labiovelar *kw→f in Gmc ✓
    ("cow", "*gwows", "k", "vache", 0.5, "gāy", 1.0, "cow", 0.5, "k"),
    # vache < Lat. vacca (labiovelar *gw→v in Latin); gāy < Skt. go/gau; cow < OE cū ✓
    ("birth / kin", "*gen-", "k", "naissance", 1.0, "janma", 1.0, "kin", 1.0, "k"),
    # naissance < Lat. nascere < *gn- (with nasal); janma < Skt. janman; kin < OE cynn ✓
    # CORRECTION: original had abbreviated "naiss." → "naissance"
    ("know", "*gno-", "k", "connaître", 0.5, "jānnā", 0.5, "know", 1.0, "k"),
    # connaître < Lat. cognoscere < *gno-; jānnā < Skt. jñā-; know < OE cnāwan ✓
    ("kind / gender", "*gen-", "k", "genre", 1.0, "jāt", 0.5, "kind", 1.0, "k"),
    # genre < Lat. genus; jāt < Skt. jāti "birth/kind"; kind < OE gecynd ✓
    # (Distinct vocabulary entry from birth/kin, same root *gen-)
    # ── PIE *bh ──────────────────────────────────────────────────────────────────────────────────────────────────
    ("brother", "*bhrater", "b", "frère", 0.5, "bhāī", 1.0, "brother", 0.5, "b"),
    # frère < Lat. frater; bhāī < Skt. bhrātā; brother < OE brōþor ✓
    # ── PIE vowel-initial ────────────────────────────────────────────────────────────────────────────────────────
    ("one", "*oyno-", "v", "un", 1.0, "ek", 1.0, "one", 1.0, "v"),
    # un < Lat. unus; ek < Skt. eka; one < OE ān ✓
    ("eight", "*okto", "v", "huit", 1.0, "āṭh", 1.0, "eight", 1.0, "v"),
    # huit < Lat. octo; āṭh < Skt. aṣṭa; eight < OE eahta ✓
    ("I", "*eg-", "v", "je", 1.0, "main", 0.5, "I", 1.0, "v"),
    # je < Lat. ego; main < Skt. aham via Prakrit "mhaṃ" (extended *eg̑hom); I < OE ic ✓
    ("up / over", "*uper-", "v", "sur", 1.0, "upar", 1.0, "over", 1.0, "v"),
    # sur < Lat. super; upar < Skt. upari; over < OE ofer ✓
    ("age / ever", "*aywo-", "v", "âge", 1.0, "āyū", 1.0, "ever", 1.0, "v"),
    # âge < Lat. aetatem; āyū < Skt. āyus "life-span"; ever < OE ǣfre < *aiwo- ✓
    # CORRECTION: English "age" removed (French borrowing); retained native "ever"
    ("eye", "*okw-", "v", "œil", 0.5, "ānkh", 1.0, "eye", 0.5, "v"),
    # œil < Lat. oculus; ānkh < Skt. akṣi/akṣa; eye < OE ēage ✓
    # CORRECTION: PIE root "*hokw-" → standard "*okw-"
    ("our", "*nes-", "v", "notre", 1.0, "hamārā", 0.5, "our", 1.0, "v"),
    # notre < Lat. noster; hamārā < Skt. asmākam via Prakrit amhāraṃ; our < OE ūre ✓
    ("wind", "*weyh-", "v", "vent", 1.0, "vāyu [skt]", 1.0, "wind", 1.0, "v"),
    # vent < Lat. ventus; vāyu < Skt. vāyu "wind/air"; wind < OE wind ✓
]


# ---------------------------------------------------------------------------
# REMOVED_DATA  –  entries failing one or more criteria
# Format: (original_tuple, "reason code: explanation")
# ---------------------------------------------------------------------------

REMOVED_DATA = [
    # ── PIE *p class ────────────────────────────────────────────────────────
    (
        ("fish", "*pisk-", "p", "poisson", 1.0, "matsya [skt]", 0.0, "fish", 0.0, "p"),
        "Wrong Hindi: Sanskrit 'matsya' traces to *mats-/*meth-, not *pisk-; hi_pfi=0.0 confirms no phonological fidelity",
    ),
    (
        (
            "cattle / fee",
            "*peku-",
            "p",
            "bétail",
            1.0,
            "pashu [skt]",
            1.0,
            "fee",
            0.0,
            "p",
        ),
        "Wrong French: 'bétail' < Latin bestia (not *peku-); true French cognate would be 'pécuniaire'",
    ),
    (
        ("fly", "*pley-", "p", "planer", 1.0, "pat [skt]", 0.5, "fly", 0.0, "p"),
        "Different PIE roots: Sanskrit pat- < *pet- (to fly/fall), OE flēogan < *pleug-, French planer uncertain; three roots conflated",
    ),
    (
        ("journey / pour", "*per-", "p", "pour", 1.0, "pār", 1.0, "fare", 0.0, "p"),
        "Semantic mismatch: French 'pour' (= for/in order to), Hindi 'pār' (= across), English 'fare' (= to travel) represent divergent senses; too broad for strict alignment",
    ),
    (
        ("fall", "*peth-", "p", "tomber", 0.5, "parnā", 1.0, "fall", 0.0, "p"),
        "Wrong French: 'tomber' is of Germanic origin (unrelated); wrong English: OE feallan < *phol-, not *peth-",
    ),
    (
        ("pure", "*pewH-", "p", "pur", 1.0, "pavan [skt]", 1.0, "fire", 0.5, "p"),
        "Wrong English: 'fire' < PIE *pHur- (separate root); semantic mismatch 'pure' vs 'fire'",
    ),
    (
        ("flat / plain", "*plth2-", "p", "plat", 1.0, "patthar", 0.5, "flat", 0.5, "p"),
        "Semantic mismatch Hindi: 'patthar' means 'stone/rock', not 'flat'; different Skt. root",
    ),
    (
        (
            "pray / ask",
            "*prek-",
            "p",
            "prier",
            1.0,
            "prārthanā [skt]",
            1.0,
            "frayne",
            0.0,
            "p",
        ),
        "Non-standard English: 'frayne' is archaic/dialectal and unrecognised in standard modern English; no native Germanic standard form preserved",
    ),
    (
        (
            "first",
            "*preyH-",
            "p",
            "premier",
            1.0,
            "pratham [skt]",
            1.0,
            "first",
            0.0,
            "p",
        ),
        "Different derivatives: Latin primus < *preh3mo-, Sanskrit pratham < *pro-thamo-, OE fyrst < *furistaz; all from *pro- family but different suffixed forms — cross-root comparison",
    ),
    (
        ("bridge / path", "*pent-", "p", "pont", 1.0, "path", 0.5, "find", 0.5, "p"),
        "Wrong English: 'find' < OE findan (unrelated); 'path' is the genuine English cognate but is left as Hindi form creating confusion",
    ),
    (
        ("pay", "*kweyH-", "p", "payer", 1.0, "paythan [skt]", 0.0, "pay", 0.5, "p"),
        "Wrong English: 'pay' was borrowed from Old French payer into Middle English — not native Germanic; hi_pfi=0.0",
    ),
    (
        ("protect / feed", "*pa-", "p", "paître", 1.0, "pāl", 0.0, "fend", 0.5, "p"),
        "Wrong English: 'fend' < 'defend' < Latin defendere — not from *pa-; hi_pfi=0.0",
    ),
    (
        (
            "put / place",
            "*po-",
            "p",
            "poser",
            0.5,
            "paṭakna [skt]",
            0.0,
            "find",
            0.0,
            "p",
        ),
        "Wrong English: 'find' is completely unrelated; hi_pfi=0.0; multiple failures",
    ),
    # ── PIE *d class ────────────────────────────────────────────────────────
    (
        ("deity", "*deywo-", "d", "dieu", 1.0, "dev", 1.0, "divine", 0.0, "d"),
        "Wrong English: 'divine' < Latin divinus — a Latin borrowing into English, not native Germanic; native reflex is archaic 'Tiw' (in Tuesday)",
    ),
    (
        ("earth", "*dher-", "d", "terre", 1.0, "dharti", 1.0, "earth", 0.0, "d"),
        "Different PIE roots: Latin terra < *terh2- (dry/land); OE eorþe < *er- (earth); neither is straightforwardly *dher-",
    ),
    (
        ("give", "*deh3-", "d", "donner", 1.0, "denā", 1.0, "deal", 1.0, "d"),
        "Wrong English: 'deal' < PGmc *dailijaną < *dheh1l- 'to divide' — different root; native English cognate of *deh3- does not survive as a common word",
    ),
    (
        ("day", "*dyew-", "d", "jour", 0.5, "din", 1.0, "day", 1.0, "d"),
        "Different PIE roots: Latin dies < *dyew- (sky/day); PGmc *dagaz (day) < *dhegwh- (to burn) — NOT the same root",
    ),
    (
        (
            "daughter",
            "*dhugh-",
            "d",
            "fille",
            0.5,
            "betī [loan]",
            0.0,
            "daughter",
            1.0,
            "d",
        ),
        "Hindi loanword: 'betī' is a Prakritic replacement; French 'fille' < Latin filia (unrelated root)",
    ),
    (
        (
            "tongue",
            "*dng-",
            "d",
            "langue",
            0.5,
            "zubān [loan]",
            0.0,
            "tongue",
            0.0,
            "d",
        ),
        "Hindi loanword: 'zubān' is Persian; French 'langue' < Latin lingua (different root)",
    ),
    (
        (
            "divide / two",
            "*dwi-",
            "d",
            "diviser",
            1.0,
            "dvitīya [skt]",
            1.0,
            "twain",
            0.0,
            "d",
        ),
        "Wrong French: 'diviser' < Latin dividere < *dʰei- 'to separate' — not directly from *dwi-",
    ),
    (
        ("distant / far", "*deh3-", "d", "dur", 1.0, "dūr", 1.0, "there", 0.0, "d"),
        "Semantic mismatch: French 'dur' means 'hard' (not 'far'); English 'there' is a demonstrative adverb — wrong semantic field",
    ),
    (
        (
            "draw / pull",
            "*dhragh-",
            "d",
            "traîner",
            0.5,
            "dharakhnā",
            1.0,
            "draw",
            0.0,
            "d",
        ),
        "Uncertain Hindi: 'dharakhnā' etymology speculative; uncertain French: traîner < Latin trahere — *tragh- vs *dhragh- conflation",
    ),
    (
        (
            "tame / domestic",
            "*deme-",
            "d",
            "domestique",
            1.0,
            "damān [skt]",
            1.0,
            "tame",
            0.0,
            "d",
        ),
        "Semantic mismatch: French 'domestique' means 'of the household' (from domus/house), English 'tame' means 'to subdue an animal' — different semantic branches of *dem-",
    ),
    (
        ("dew", "*dhewbh-", "d", "rosée", 0.0, "os [replaced]", 0.0, "dew", 1.0, "d"),
        "French and Hindi both lost the root: fr_pfi=0.0, hi_pfi=0.0; only English preserves cognate",
    ),
    (
        ("dear", "*deur-", "d", "cher", 0.0, "pyārā [loan]", 0.0, "dear", 1.0, "d"),
        "French 'cher' < Latin carus (different root); Hindi 'pyārā' is a non-PIE borrowing",
    ),
    (
        ("order / right", "*dher-", "d", "droit", 1.0, "dharm", 1.0, "true", 0.0, "d"),
        "Wrong French: 'droit' < Latin directum < dirigere < *reg- 'to lead straight' — not *dher-",
    ),
    (
        (
            "dance / drag",
            "*dhangh-",
            "d",
            "danser",
            1.0,
            "nachna [repl]",
            0.0,
            "tang",
            0.5,
            "d",
        ),
        "Hindi replacement; English 'tang' is not a standard cognate for *dhangh-",
    ),
    (
        ("death / mortal", "*mrt-", "m", "mort", 1.0, "maut", 1.0, "murder", 1.0, "m"),
        "Uncertain Hindi: 'maut' is classified as an Arabic loanword (Ar. mawt) in standard Urdu/Hindi lexicography; Sanskrit cognate is 'mṛtyu' → not preserved in colloquial Hindi",
    ),
    # ── PIE *t class ────────────────────────────────────────────────────────
    (
        ("skin", "*twer-", "t", "peau", 0.5, "tvacha [skt]", 1.0, "skin", 0.0, "t"),
        "Wrong French: 'peau' < Latin pellis (root *pel-, not *twer-); wrong English: 'skin' is a Norse borrowing",
    ),
    (
        ("that", "*tod", "t", "ça / ce", 0.5, "tab / tab", 1.0, "that", 0.0, "t"),
        "Wrong French: 'ça/ce' < Latin ecce hoc — not from *tod; semantic mismatch Hindi 'tab' (= then, not that)",
    ),
    (
        ("thin", "*ten-", "t", "tenu", 1.0, "thinness", 0.5, "thin", 0.0, "t"),
        "Data error Hindi: 'thinness' is an English word, not a Hindi/Sanskrit form; genuine Hindi/Skt. cognate is 'tanū' (slender)",
    ),
    (
        (
            "through",
            "*trh2-",
            "t",
            "travers",
            0.5,
            "tirchā [skt]",
            0.5,
            "through",
            0.0,
            "t",
        ),
        "Semantic mismatch Hindi: 'tirchā' means 'oblique/slanted', not 'through'; different semantic development",
    ),
    # ── PIE *m class ────────────────────────────────────────────────────────
    (
        (
            "middle",
            "*medhyo-",
            "m",
            "milieu",
            1.0,
            "beech [repl]",
            0.5,
            "mid",
            1.0,
            "m",
        ),
        "Hindi replacement: 'bīc/beech' is not directly inherited from Sanskrit 'madhya' without replacement marker",
    ),
    (
        ("sea", "*mori-", "m", "mer", 1.0, "maru [skt]", 1.0, "mere (arch.)", 1.0, "m"),
        "Semantic mismatch Hindi: Sanskrit 'maru' means 'desert/wasteland', not 'sea' — opposite meaning",
    ),
    (
        ("man", "*man-", "m", "homme", 0.5, "mard", 1.0, "man", 0.5, "m"),
        "Wrong French: 'homme' < Latin homo < *dhghom- 'earthling' — different PIE root; Hindi 'mard' is a Persian loanword",
    ),
    # ── PIE *n class ────────────────────────────────────────────────────────
    (
        ("night", "*nakto-", "n", "nuit", 1.0, "rāt [loan]", 0.0, "night", 1.0, "n"),
        "Hindi loanword: 'rāt' classified as loan in dataset (hi_pfi=0.0); Sanskrit cognate is 'rātri' but marked as replacement",
    ),
    (
        (
            "cloud / sky",
            "*nebh-",
            "n",
            "nuage",
            1.0,
            "nabha [skt]",
            1.0,
            "nebula",
            1.0,
            "n",
        ),
        "Wrong English: 'nebula' is a direct Latin borrowing into English (used in astronomy) — not native Germanic; native OE reflex is lost",
    ),
    # ── PIE *s class ────────────────────────────────────────────────────────
    (
        ("sleep", "*swep-", "s", "sommeil", 1.0, "sapnā", 1.0, "sleep", 1.0, "s"),
        "Wrong English: 'sleep' < OE slæpan < PGmc *slēpaną < *sleb- — different root; native English reflex of *swep- is archaic 'sweven' (dream)",
    ),
    (
        ("serpent", "*serp-", "s", "serpent", 1.0, "sāmp", 1.0, "serpent", 1.0, "s"),
        "Wrong English: 'serpent' was borrowed from Latin serpens via Old French — not native Germanic; native English is 'snake' or 'worm'",
    ),
    (
        ("sit", "*sed-", "s", "s'asseoir", 1.0, "baiṭhnā [repl]", 0.0, "sit", 1.0, "s"),
        "Hindi replacement: 'baiṭhnā' does not descend from *sed-; hi_pfi=0.0",
    ),
    (
        (
            "stand",
            "*steh2-",
            "s",
            "station",
            1.0,
            "khaṛā [repl]",
            0.0,
            "stand",
            1.0,
            "s",
        ),
        "Hindi replacement: 'khaṛā' does not descend from *steh2-; hi_pfi=0.0",
    ),
    (
        ("sow / seed", "*seh1-", "s", "semer", 1.0, "bīj [repl]", 0.0, "sow", 1.0, "s"),
        "Hindi replacement: 'bīj' (seed) is a replacement, not a direct descendant of *seh1-",
    ),
    (
        ("snow", "*sneygwh-", "s", "neige", 0.5, "barf [loan]", 0.0, "snow", 1.0, "s"),
        "Hindi loanword: 'barf' is from Persian barf (snow)",
    ),
    (
        ("salt", "*sal-", "s", "sel", 1.0, "namak [loan]", 0.0, "salt", 1.0, "s"),
        "Hindi loanword: 'namak' is from Arabic/Persian — not Indo-Aryan inheritance",
    ),
    (
        (
            "say / speak",
            "*sekw-",
            "s",
            "suivre",
            1.0,
            "kahnā [repl]",
            0.0,
            "say",
            1.0,
            "s",
        ),
        "Semantic mismatch: *sekw- means 'to follow'; French 'suivre' = to follow (correct); but 'say' is unrelated (OE secgan < *sag-)",
    ),
    (
        ("see", "*sekw-", "s", "voir", 0.5, "dekhnā [repl]", 0.0, "see", 1.0, "s"),
        "Wrong French: 'voir' < Latin videre < *wid- (different root); Hindi replacement",
    ),
    (
        (
            "swallow / swim",
            "*swel-",
            "s",
            "avaler",
            0.0,
            "sūnā [skt]",
            1.0,
            "swallow",
            1.0,
            "s",
        ),
        "Wrong French: fr_pfi=0.0; semantic mismatch Hindi: 'sūnā' means 'to hear', not 'to swallow'",
    ),
    (
        (
            "sharp / shear",
            "*sker-",
            "s",
            "couper",
            0.0,
            "kāṭnā [repl]",
            0.0,
            "shear",
            1.0,
            "s",
        ),
        "French replacement: fr_pfi=0.0; Hindi replacement: hi_pfi=0.0",
    ),
    (
        (
            "smell / scent",
            "*swad-",
            "s",
            "sentir",
            1.0,
            "sunghna",
            1.0,
            "smell",
            1.0,
            "s",
        ),
        "Wrong root: *swad- means 'to taste/be pleasant'; French 'sentir' < Latin sentire 'to feel/sense'; 'smell' has uncertain Germanic origin — speculative",
    ),
    (
        ("star", "*ster-", "s", "étoile", 1.0, "sitāra", 1.0, "star", 1.0, "s"),
        "Hindi loanword: 'sitāra' is from Persian sitāra (star) — not Sanskrit/Skt. inheritance; Sanskrit cognate is 'tāra/nakṣatra'",
    ),
    (
        (
            "seven (alt)",
            "*sep-",
            "s",
            "septième",
            1.0,
            "sapt [skt]",
            1.0,
            "seventh",
            1.0,
            "s",
        ),
        "Duplicate: ordinal forms of 'seven' already represented in the CLEAN_DATA cardinal entry (*septm); redundant",
    ),
    (
        (
            "same / self",
            "*sem-",
            "s",
            "même",
            0.5,
            "saman [skt]",
            1.0,
            "same",
            1.0,
            "s",
        ),
        "Uncertain French: 'même' < Latin met-ipse — derivation from *sem- is indirect and disputed (fr_pfi=0.5)",
    ),
    (
        (
            "send",
            "*senth2-",
            "s",
            "envoyer",
            0.0,
            "bhejnā [repl]",
            0.0,
            "send",
            1.0,
            "s",
        ),
        "French and Hindi both failed: fr_pfi=0.0; Hindi replacement",
    ),
    (
        ("slow / sloth", "*sleh1-", "s", "lent", 0.5, "sust", 1.0, "slow", 1.0, "s"),
        "Wrong French: 'lent' < Latin lentus (possibly *lent-, not *sleh1-); Hindi 'sust' is likely from Persian sust",
    ),
    # ── PIE *k class ────────────────────────────────────────────────────────
    (
        ("heart", "*kerd-", "k", "cœur", 1.0, "dil [loan]", 0.0, "heart", 0.5, "k"),
        "Hindi loanword: 'dil' is from Persian/Arabic",
    ),
    (
        ("head", "*kaput-", "k", "chef", 0.5, "sar [loan]", 0.0, "head", 0.5, "k"),
        "Hindi loanword: 'sar' is from Persian sar (head)",
    ),
    (
        ("come", "*gwa-", "k", "venir", 0.5, "ānā", 0.5, "come", 0.5, "k"),
        "Uncertain Hindi: 'ānā' derivation from *g^wa- is indirect; all three PFIs are only 0.5",
    ),
    (
        ("knee", "*genu-", "k", "genou", 1.0, "ghuṭnā", 1.0, "knee", 0.5, "k"),
        "Uncertain Hindi: 'ghuṭnā' (knee) traces to Sanskrit jaṅghā (leg/calf) or ghuṭikā — not clearly from *genu-; genuine Skt. cognate is 'jānu'",
    ),
    (
        ("cold", "*gel-", "k", "gel", 1.0, "ṭhaṇḍā [repl]", 0.0, "cold", 1.0, "k"),
        "Hindi replacement: 'ṭhaṇḍā' does not descend from *gel-",
    ),
    (
        ("cut", "*sek-", "k", "couper", 0.5, "kāṭnā", 1.0, "cut", 0.5, "k"),
        "Wrong English: 'cut' has obscure origin, possibly Norse; wrong French: 'couper' from Latin colpare (strike) — uncertain *sek- connection",
    ),
    (
        ("kill", "*gwhen-", "k", "occire", 0.5, "mārnā [repl]", 0.0, "quell", 0.5, "k"),
        "Hindi replacement; 'occire' is archaic French",
    ),
    (
        ("hear", "*klew-", "k", "clair", 0.5, "sunnā [repl]", 0.0, "hear", 0.5, "k"),
        "Hindi replacement: 'sunnā' does not descend from *klew-",
    ),
    (
        ("cloud", "*kel-", "k", "ciel", 1.0, "bādal [loan]", 0.0, "cloud", 0.5, "k"),
        "Hindi loanword: 'bādal' is from Arabic badal (cloud)",
    ),
    (
        ("create/karma", "*ker-", "k", "créer", 1.0, "karm", 1.0, "create", 1.0, "k"),
        "Wrong English: 'create' < Latin creare — a Latin borrowing, not native Germanic",
    ),
    (
        ("warm", "*gwermo-", "k", "chaud", 0.5, "garam", 1.0, "warm", 1.0, "k"),
        "Wrong French: 'chaud' < Latin calidus < *kel- (warm) — a related but distinct PIE root",
    ),
    (
        (
            "sky / heaven",
            "*kwyelo-",
            "k",
            "ciel",
            1.0,
            "kshiti [skt]",
            0.5,
            "heaven",
            0.0,
            "k",
        ),
        "Semantic mismatch Hindi: 'kshiti' means 'earth/ground' (opposite meaning!); English 'heaven' from *kap-, not *kwyelo-",
    ),
    (
        (
            "call / cry",
            "*gal-",
            "k",
            "crier",
            0.5,
            "garaj [skt]",
            1.0,
            "call",
            1.0,
            "k",
        ),
        "Uncertain French: 'crier' etymology is disputed; semantic mismatch Hindi: 'garaj' = roar/thunder, not 'call'",
    ),
    (
        ("carry", "*kwer-", "k", "quérir", 1.0, "karnā", 0.5, "carry", 0.5, "k"),
        "Wrong English: 'carry' < Old North French 'carier' — a Romance borrowing; semantic mismatch Hindi: 'karnā' = to do",
    ),
    (
        (
            "grain / corn",
            "*greno-",
            "k",
            "grain",
            0.5,
            "gehūn [repl]",
            0.0,
            "corn",
            0.5,
            "k",
        ),
        "Hindi replacement: 'gehūn' (wheat) is a replacement word",
    ),
    (
        (
            "king / can",
            "*kn̥-",
            "k",
            "can (arch.)",
            0.5,
            "rājā [repl]",
            0.0,
            "can / king",
            1.0,
            "k",
        ),
        "Hindi replacement: 'rājā' < Sanskrit rājan (different root *reg-)",
    ),
    (
        ("cat", "*kattos-", "k", "chat", 0.5, "billī [loan]", 0.0, "cat", 1.0, "k"),
        "Not a PIE root: *kattos is Late Latin, not ancestral PIE; Hindi 'billī' is a loan",
    ),
    (
        (
            "curve / bow",
            "*keu-",
            "k",
            "courber",
            0.5,
            "kurva [skt]",
            0.5,
            "curve",
            0.0,
            "k",
        ),
        "Wrong English: 'curve' < Latin curvus — a Latin borrowing into English",
    ),
    (
        ("go / come", "*kwel-", "k", "aller", 0.0, "chalā", 0.5, "go", 0.0, "k"),
        "Wrong French: 'aller' is from Latin ambulare or vadere — fr_pfi=0.0",
    ),
    (
        ("clean", "*kley-", "k", "clair", 1.0, "sāf [loan]", 0.0, "clean", 1.0, "k"),
        "Hindi loanword: 'sāf' is from Arabic ṣāf (clean/clear)",
    ),
    (
        ("break", "*kreg-", "k", "casser", 0.5, "kaṭnā", 0.5, "crack", 1.0, "k"),
        "Wrong French: 'casser' < Latin quassare — different root; semantic mismatch Hindi: 'kaṭnā' = to cut",
    ),
    (
        ("gather", "*ger-", "k", "garder", 1.0, "ikkatṭhā", 0.0, "gather", 0.5, "k"),
        "Semantic mismatch French: 'garder' = to keep/guard, not gather; hi_pfi=0.0",
    ),
    (
        (
            "give birth",
            "*gwer-",
            "k",
            "grave",
            0.5,
            "garv [skt]",
            1.0,
            "queen",
            0.5,
            "k",
        ),
        "Semantic mismatch: French 'grave' = heavy/serious; 'queen' < *gwen- (woman) — different root",
    ),
    (
        (
            "key / hook",
            "*kayko-",
            "k",
            "clé",
            0.5,
            "chābī [loan]",
            0.0,
            "hook",
            0.5,
            "k",
        ),
        "Hindi loanword: 'chābī' is a borrowing",
    ),
    # ── PIE *b / *bh class ───────────────────────────────────────────────────
    (
        ("carry / bear", "*bher-", "b", "porter", 0.5, "bharnā", 1.0, "bear", 1.0, "b"),
        "Wrong French: 'porter' < Latin portare < *per- 'to carry' — different PIE root from *bher-",
    ),
    (
        (
            "bright",
            "*bhergh-",
            "b",
            "brillant",
            0.5,
            "bhor [skt]",
            1.0,
            "bright",
            0.5,
            "b",
        ),
        "Wrong French: 'brillant' < Italian brillante or Latin beryllus — not from *bhergh-",
    ),
    (
        ("be / exist", "*bhu-", "b", "être", 0.5, "honā", 0.5, "be", 0.5, "b"),
        "Wrong French: 'être' primarily descends from Latin esse < *h1es- (to be), not *bhu-; Latin *bhu- only surfaces in suppletive 'fui' (I was)",
    ),
    (
        ("bite", "*bheid-", "b", "mordre", 0.5, "kāṭnā [repl]", 0.0, "bite", 0.5, "b"),
        "Wrong French: 'mordre' < Latin mordere < *smerd- — different root; Hindi replacement",
    ),
    (
        ("blow", "*bhleh1-", "b", "souffler", 0.0, "phūnknā", 0.5, "blow", 0.5, "b"),
        "Wrong French: 'souffler' < Latin sufflare — fr_pfi=0.0",
    ),
    (
        ("boil", "*bhel-", "b", "bouillir", 1.0, "ubalnā", 0.5, "boil", 1.0, "b"),
        "Wrong English: 'boil' was borrowed from Old French boillir into Middle English — not native Germanic",
    ),
    # ── PIE *r class ────────────────────────────────────────────────────────
    (
        ("red", "*reudh-", "r", "rouge", 1.0, "lāl [repl]", 0.0, "red", 1.0, "r"),
        "Hindi replacement: 'lāl' is a replacement; hi_pfi=0.0",
    ),
    (
        (
            "river / flow",
            "*sreu-",
            "r",
            "ruisseau",
            1.0,
            "nadi [diff]",
            0.0,
            "run / stream",
            0.5,
            "r",
        ),
        "Wrong Hindi: 'nadi' (river) < Sanskrit nadī < *nad- (to flow loudly) — different root from *sreu-",
    ),
    # ── PIE vowel-initial class ──────────────────────────────────────────────
    (
        ("eat", "*ed-", "v", "manger", 0.0, "khānā [repl]", 0.0, "eat", 1.0, "v"),
        "French and Hindi both failed: 'manger' fr_pfi=0.0; 'khānā' is a replacement",
    ),
    (
        ("and", "*eti", "v", "et", 1.0, "aur", 0.5, "and", 1.0, "v"),
        "Uncertain Hindi: 'aur' (and/more) etymology disputed; not clearly from *eti",
    ),
    (
        ("other", "*al-", "v", "autre", 1.0, "aur [also]", 0.5, "other", 1.0, "v"),
        "Wrong Hindi: 'aur' used for 'other' is a stretch; Skt. cognate would be 'anya' (another) from *an-yo-",
    ),
    (
        (
            "animal",
            "*animo-",
            "v",
            "animal",
            1.0,
            "jāwar [repl]",
            0.0,
            "animal",
            1.0,
            "v",
        ),
        "Hindi replacement; English 'animal' < Latin animale — a Latin borrowing",
    ),
    (
        ("water", "*wed-", "v", "eau", 0.5, "pānī [repl]", 0.0, "water", 1.0, "v"),
        "Hindi replacement: 'pānī' does not descend from *wed-; French 'eau' < Latin aqua < *h2ekw- (different root)",
    ),
    (
        ("ear", "*ows-", "v", "oreille", 1.0, "kān [repl]", 0.0, "ear", 1.0, "v"),
        "Hindi marked as replacement in dataset (hi_pfi=0.0); 'kān' may descend from Sanskrit karṇa but annotated as replacement",
    ),
    (
        ("open", "*ap-", "v", "ouvrir", 1.0, "kholnā [repl]", 0.0, "open", 1.0, "v"),
        "Hindi replacement: 'kholnā' does not descend from *ap-",
    ),
    (
        ("bone", "*H3est-", "v", "os", 1.0, "haḍḍī", 0.0, "bone", 1.0, "v"),
        "Wrong English: 'bone' < OE bān < PGmc *bainam < *bhoyno- — different PIE root from *H3est-; hi_pfi=0.0",
    ),
    (
        ("back", "*apo-", "v", "arrière", 0.5, "pīchhe", 0.5, "back", 1.0, "v"),
        "Wrong French: 'arrière' < Latin ad retro — not from *apo-",
    ),
    (
        ("ash", "*hes-", "v", "cendre", 0.0, "rākh [repl]", 0.0, "ash", 1.0, "v"),
        "French and Hindi both failed: fr_pfi=0.0; Hindi replacement",
    ),
    (
        ("all", "*al-", "v", "alle (all)", 0.5, "sab [loan]", 0.0, "all", 1.0, "v"),
        "Hindi loanword: 'sab' is from Arabic/Persian",
    ),
    (
        ("in", "*en-", "v", "en", 1.0, "men", 1.0, "in", 1.0, "v"),
        "Uncertain Hindi: 'mẽ/men' (in) typically traces to Sanskrit 'madhye' (in the middle of) — not directly from *en-",
    ),
    (
        (
            "wood / forest",
            "*widhu-",
            "v",
            "vide",
            0.5,
            "van [skt]",
            1.0,
            "wood",
            1.0,
            "v",
        ),
        "Semantic mismatch French: 'vide' means 'empty' — completely wrong meaning",
    ),
    (
        (
            "wisdom / know",
            "*wid-",
            "v",
            "voir",
            1.0,
            "jānnā [repl]",
            0.5,
            "wisdom",
            1.0,
            "v",
        ),
        "Hindi replacement: 'jānnā' marked as replacement",
    ),
    (
        ("wet", "*wed-", "v", "eau", 0.5, "geelā", 0.0, "wet", 1.0, "v"),
        "Wrong French: 'eau' < Latin aqua < *h2ekw- — different root; hi_pfi=0.0",
    ),
    (
        ("warm (glow)", "*gwarm-", "v", "chaud", 0.5, "garm", 1.0, "warm", 1.0, "v"),
        "Wrong French: 'chaud' < Latin calidus < *kel- (warm) — different root",
    ),
    (
        ("wing", "*pewg-", "v", "aile", 0.5, "pankh", 0.5, "wing", 1.0, "v"),
        "Wrong French: 'aile' < Latin ala < *h2el- — different PIE root",
    ),
    (
        ("woman", "*gwen-", "v", "femme", 0.5, "aurat [loan]", 0.0, "woman", 0.5, "v"),
        "Hindi loanword: 'aurat' is from Arabic 'awra'",
    ),
    (
        ("work", "*werg-", "v", "œuvre", 1.0, "kām [repl]", 0.0, "work", 1.0, "v"),
        "Hindi replacement: 'kām' does not descend from *werg-",
    ),
]


# ---------------------------------------------------------------------------
# Helpers (identical interface to original script)
# ---------------------------------------------------------------------------

BRANCHES = {
    "French": 4,
    "Hindi/Sanskrit": 6,
    "English": 8,
}
CLASS_COL = 9


def mean_scores(entries, branch_idx, class_filter=None):
    scores = [
        row[branch_idx]
        for row in entries
        if row[branch_idx] is not None
        and (class_filter is None or row[CLASS_COL] in class_filter)
    ]
    if not scores:
        return None, 0
    return round(sum(scores) / len(scores), 3), len(scores)


def score_distribution(entries, branch_idx):
    scores = [r[branch_idx] for r in entries if r[branch_idx] is not None]
    return {
        "full": scores.count(1.0),
        "partial": scores.count(0.5),
        "shifted": scores.count(0.0),
        "n": len(scores),
    }


def export_csv(entries, filename="pfi_clean_results.csv"):
    headers = [
        "concept",
        "pie_root",
        "pie_class",
        "fr_form",
        "fr_pfi",
        "hi_form",
        "hi_pfi",
        "en_form",
        "en_pfi",
        "class_tag",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in entries:
            writer.writerow(row)
    print(f"  Exported {len(entries)} clean entries  →  {filename}")


def export_removed_csv(removed, filename="pfi_removed_entries.csv"):
    headers = [
        "concept",
        "pie_root",
        "pie_class",
        "fr_form",
        "fr_pfi",
        "hi_form",
        "hi_pfi",
        "en_form",
        "en_pfi",
        "class_tag",
        "removal_reason",
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for entry, reason in removed:
            writer.writerow(list(entry) + [reason])
    print(f"  Exported {len(removed)} removed entries →  {filename}")


def generate_chart(entries, filename="fig_clean_pfi_bar.pdf"):
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("  matplotlib not installed — skipping chart.")
        return

    grimm = {"p", "d", "t"}
    stable = {"m", "n", "s"}

    class_defs = [
        ("*p", {"p"}),
        ("*d", {"d"}),
        ("*t", {"t"}),
        ("Combined\n*p+d+t", grimm),
        ("*m", {"m"}),
        ("*n", {"n"}),
        ("*s", {"s"}),
        ("Combined\n*m+n+s", stable),
    ]

    cats = [c[0] for c in class_defs]
    fr_v = [mean_scores(entries, 4, c[1])[0] or 0 for c in class_defs]
    hi_v = [mean_scores(entries, 6, c[1])[0] or 0 for c in class_defs]
    en_v = [mean_scores(entries, 8, c[1])[0] or 0 for c in class_defs]

    x, w = np.arange(len(cats)), 0.24

    fig, ax = plt.subplots(figsize=(14, 6), facecolor="white")
    ax.set_facecolor("white")
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)

    b1 = ax.bar(
        x - w, fr_v, w, label="French (Italic/Romance)", color="#1565C0", zorder=3
    )
    b2 = ax.bar(
        x, hi_v, w, label="Hindi/Sanskrit (Indo-Iranian)", color="#B71C1C", zorder=3
    )
    b3 = ax.bar(x + w, en_v, w, label="English (Germanic)", color="#1B5E20", zorder=3)

    for bars, col in [(b1, "#1565C0"), (b2, "#B71C1C"), (b3, "#1B5E20")]:
        for bar in bars:
            h = bar.get_height()
            if h >= 0.04:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + 0.014,
                    f"{h:.2f}",
                    ha="center",
                    va="bottom",
                    fontsize=7.5,
                    color=col,
                    fontweight="bold",
                )

    ax.axvspan(-0.55, 3.55, color="#FFF3E0", alpha=0.55, zorder=0)
    ax.axvspan(3.55, 7.55, color="#E3F2FD", alpha=0.55, zorder=0)
    ax.axvline(3.5, color="#90A4AE", lw=1.6, ls="--", zorder=2)
    ax.text(
        1.5,
        1.11,
        "GRIMM-AFFECTED CLASSES",
        ha="center",
        fontsize=9.5,
        fontweight="bold",
        color="#E65100",
        transform=ax.get_xaxis_transform(),
    )
    ax.text(
        5.75,
        1.11,
        "STABLE CONTROL CLASSES",
        ha="center",
        fontsize=9.5,
        fontweight="bold",
        color="#1565C0",
        transform=ax.get_xaxis_transform(),
    )

    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=10)
    ax.set_ylim(0, 1.18)
    ax.set_yticks(np.arange(0, 1.1, 0.2))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1f}"))
    ax.set_ylabel("Phonological Fidelity Index (PFI)", fontsize=11)
    ax.grid(axis="y", color="#ECEFF1", lw=1.2, zorder=0)
    ax.legend(fontsize=10, framealpha=0.97, edgecolor="#90A4AE")
    ax.set_title(
        "Phonological Fidelity Index by PIE Consonant Class — CLEAN DATASET\n"
        "French · Hindi/Sanskrit · English",
        fontsize=12.5,
        fontweight="bold",
        pad=12,
    )

    fig.tight_layout()
    fig.savefig(filename, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"  Chart saved  →  {filename}")


# ---------------------------------------------------------------------------
# Summary report
# ---------------------------------------------------------------------------


def main():
    entries = CLEAN_DATA
    removed = REMOVED_DATA

    grimm = {"p", "d", "t"}
    stable = {"m", "n", "s"}

    W = 72
    print("=" * W)
    print("  PHONOLOGICAL FIDELITY INDEX — CLEANED DATASET SUMMARY")
    print("  Tharun Rathod · IIT Roorkee · 2026")
    print("=" * W)
    print(f"\n  Original entries : {len(entries) + len(removed)}")
    print(f"  CLEAN_DATA       : {len(entries)}  (passed all 6 criteria)")
    print(f"  REMOVED_DATA     : {len(removed)}  (failed ≥1 criterion)")

    # --- removal reason breakdown ---
    reason_counts = defaultdict(int)
    keywords = [
        "Hindi loanword",
        "Hindi replacement",
        "Wrong French",
        "Wrong English",
        "Semantic mismatch",
        "Different PIE root",
        "Uncertain",
        "Data error",
        "Duplicate",
        "Wrong root",
        "Wrong Hindi",
    ]
    for _, reason in removed:
        matched = False
        for kw in keywords:
            if kw.lower() in reason.lower():
                reason_counts[kw] += 1
                matched = True
                break
        if not matched:
            reason_counts["Other"] += 1

    print("\n── REMOVAL REASON BREAKDOWN " + "─" * 44)
    for kw, cnt in sorted(reason_counts.items(), key=lambda x: -x[1]):
        print(f"  {kw:<35} {cnt:>3}")

    # --- branch PFI ---
    print("\n── CLEAN DATASET — OVERALL PFI " + "─" * 40)
    print(f"\n  {'Branch':<32} {'PFI':>7}  {'n':>4}")
    print("  " + "-" * 46)
    for label, idx in BRANCHES.items():
        score, n = mean_scores(entries, idx)
        print(f"  {label:<30} {score:>7.3f}  {n:>4}")

    # --- class-level ---
    print("\n── CLASS-LEVEL RESULTS " + "─" * 49)
    print(f"\n  {'Class':<40} {'n':>4}  {'FR':>7} {'HI':>7} {'EN':>7}")
    print("  " + "-" * 66)

    class_rows = [
        ("PIE *p  (voiceless bilabial stop)", {"p"}, "Grimm"),
        ("PIE *d  (voiced alveolar stop)", {"d"}, "Grimm"),
        ("PIE *t  (voiceless alveolar stop)", {"t"}, "Grimm"),
        ("COMBINED *p + *d + *t", grimm, "GRIMM-TOTAL"),
        ("PIE *m  (bilabial nasal)", {"m"}, "Stable"),
        ("PIE *n  (alveolar nasal)", {"n"}, "Stable"),
        ("PIE *s  (fricative)", {"s"}, "Stable"),
        ("COMBINED *m + *n + *s", stable, "STABLE-TOTAL"),
        ("PIE *k / *kw / *gw  (velar class)", {"k"}, "Complex"),
        ("PIE *b / *bh  (aspirate class)", {"b"}, "Aspirate"),
        ("PIE vowel-initial", {"v"}, "Vowel"),
    ]

    for label, cf, kind in class_rows:
        fr_s, fr_n = mean_scores(entries, 4, cf)
        hi_s, _ = mean_scores(entries, 6, cf)
        en_s, _ = mean_scores(entries, 8, cf)
        prefix = "  **" if "TOTAL" in kind else "    "
        print(
            f"{prefix} {label:<40} {fr_n:>4}  "
            f"{(fr_s or 0):>7.3f} {(hi_s or 0):>7.3f} {(en_s or 0):>7.3f}"
        )

    # --- score distribution ---
    print("\n── SCORE DISTRIBUTION " + "─" * 49)
    print(
        f"\n  {'Branch':<20} {'Full (1.0)':>12} {'Partial (0.5)':>14}"
        f" {'Shifted (0.0)':>14}  {'n':>4}"
    )
    print("  " + "-" * 68)
    for label, idx in BRANCHES.items():
        d = score_distribution(entries, idx)
        n = d["n"]
        print(
            f"  {label:<20}  {d['full']:>5} ({100*d['full']/n:4.1f}%)"
            f"  {d['partial']:>5} ({100*d['partial']/n:4.1f}%)"
            f"  {d['shifted']:>5} ({100*d['shifted']/n:4.1f}%)  {n:>4}"
        )

    # --- Grimm differentials ---
    print("\n── KEY DIFFERENTIALS (Grimm signature) " + "─" * 32)
    fr_stable, _ = mean_scores(entries, 4, stable)
    fr_grimm, _ = mean_scores(entries, 4, grimm)
    en_stable, _ = mean_scores(entries, 8, stable)
    en_grimm, _ = mean_scores(entries, 8, grimm)
    hi_grimm, _ = mean_scores(entries, 6, grimm)
    print(
        f"\n  ΔGrimm French  : {fr_stable:.3f} (stable) "
        f"− {fr_grimm:.3f} (Grimm) = {fr_stable - fr_grimm:+.3f} pp"
    )
    print(
        f"  ΔGrimm English : {en_stable:.3f} (stable) "
        f"− {en_grimm:.3f} (Grimm) = {en_stable - en_grimm:+.3f} pp"
    )
    print(
        f"\n  French–English gap (Grimm classes)  : " f"{fr_grimm - en_grimm:+.3f} pp"
    )
    print(f"  Hindi –English gap (Grimm classes)  : " f"{hi_grimm - en_grimm:+.3f} pp")

    print("\n" + "=" * W)
    print(f"  Clean dataset : {len(entries)} entries")
    print(f"  Grimm-affected classes  : *p, *d, *t")
    print(f"  Stable control classes  : *m, *n, *s")
    print("=" * W + "\n")

    export_csv(entries)
    export_removed_csv(removed)
    generate_chart(entries)


if __name__ == "__main__":
    main()
