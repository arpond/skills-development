import re, sys, json, glob, os

# Score v2: adds complex_tense (perfect tenses, modal stacks), exempts
# adjectival/stative participles from the passive count, moves "provide" to the
# banned list, adds a noun-train marker and a --strict mode. The episode's
# published numbers were measured with score v1 (this file's git history at the
# episode date); v1 and v2 totals are close but not directly comparable.
SCORE_VERSION = 2

MARKETING = ["seamless","seamlessly","robust","powerful","cutting-edge","effortless","effortlessly",
    "world-class","next-generation","revolutionary","blazing","lightning-fast","elegant","delightful",
    "turnkey","best-in-class","state-of-the-art","game-changing","first-class","battle-tested",
    "enterprise-grade","supercharge","unlock","unleash","empower","empowers"]
BANNED = ["begin","begins","commence","commences","initiate","initiates","originate",
    "utilize","utilizes","utilizing","leverage","leverages","leveraging","facilitate","facilitates",
    "ensure","ensures","ensuring","prior to","subsequent to","obtain","obtains","acquire","acquires",
    "demonstrate","demonstrates","additionally","furthermore","moreover","comprehensive","comprehensively",
    "utilization","aforementioned","henceforth","therein","whilst","amongst","numerous","myriad","plethora",
    "provide","provides","provided",
    "in order to","a variety of","in the event that","due to the fact that","it is important to note"]
# STE's own recurring-errors list (see ste-recurring-errors.md). Counted only
# with --strict: these are correct STE but would flag normal prose in docs.
STRICT_BANNED = ["however","since","should","shall","using","follow","follows","followed"]
PHRASAL = ["spin up","spin down","reach out","dive into","dives into","diving into","kick off","kicks off",
    "roll out","rolls out","tear down","ramp up","circle back","drill down","spun up","reaching out"]
MODAL_HEDGE = ["it is important to note","it should be noted","it is worth noting","please note that",
    "as mentioned","as noted above"]
BE = r"(?:am|is|are|was|were|be|been|being)"
PP_IRREG = r"(?:done|made|sent|read|built|kept|held|set|put|run|written|shown|given|taken|found|got|gotten|seen|known|thrown|drawn)"
# Rule 3.3: a past participle used as an adjective is not passive. These
# stative participles only count as passive when a by-agent follows.
STATIVE = r"(?:closed|opened?|damaged|completed?|installed|connected|required|expected|configured|enabled|disabled|deprecated|supported)"
FUNC_WORDS = set("""a an the this that these those of for to in on at by with from as and or but if
when then than not no is are was were be been being am do does did has have had will would can could
may might must should shall it its their your our his her they we you i""".split())

def strip_code(t):
    # Keep the newlines a fenced block spans, so line numbers stay true and
    # the paragraphs either side of a block aren't merged into one.
    t = re.sub(r"```.*?```", lambda m: "\n" * m.group(0).count("\n"), t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", " ", t)
    return t

# Lines that stand alone: headings, table rows, horizontal rules. List items
# start a new block but absorb their own wrapped continuation lines.
STANDALONE = re.compile(r"^\s*(?:#{1,6}\s|\||-{3,}\s*$|\*{3,}\s*$)")
LIST_START = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+")

def unwrap_blocks(text):
    """Join hard-wrapped lines into one block per paragraph or list item.
    Returns (first_line_number, text) pairs, 1-based. A wrapped line is not a
    sentence boundary: without this, a 90-word sentence wrapped at 100 columns
    counts as five short ones and the long-sentence and long-paragraph checks
    never fire on wrapped markdown."""
    out, buf, start = [], [], 0
    def flush():
        if buf:
            out.append((start, " ".join(buf))); buf.clear()
    for n, line in enumerate(text.split("\n"), 1):
        s = line.strip()
        if not s or STANDALONE.match(line):
            flush(); out.append((n, line))
        elif LIST_START.match(line):
            flush(); start = n; buf.append(s)
        else:
            if not buf: start = n
            buf.append(s)
    flush()
    return out

def unwrap(text):
    return "\n".join(t for _, t in unwrap_blocks(text))

def split_sentences(line):
    s = line.strip()
    if not s: return []
    s = re.sub(r"^\s*#{1,6}\s*", "", s)
    s = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", s)
    if not s: return []
    # A sentence can open with markdown emphasis (**Also check ...**) and
    # can close with it after the punctuation (**Do this first.** Then ...).
    parts = re.split(r"(?:(?<=[.!?:])|(?<=[.!?:]\*)|(?<=[.!?:]\*\*))\s+(?=[A-Z0-9\"'\-*_])", s)
    return [p.strip() for p in parts if p.strip()]

def sentences(text):
    out = []
    for _, line in unwrap_blocks(text):
        out += split_sentences(line)
    return out

def located(text, cap, para_cap=6):
    """Long sentences and long paragraphs with the line each starts on, for
    --show. Line numbers are of the original (unstripped) text, which is why
    strip_code keeps newlines."""
    text = strip_code(text)
    long_s = []
    for line_no, block in unwrap_blocks(text):
        for s in split_sentences(block):
            if wc(s) > cap: long_s.append((line_no, wc(s), s))
    long_p, line_no = [], 1
    for para in re.split(r"(\n\s*\n)", text):
        if para.strip() and not re.fullmatch(r"\n\s*\n", para):
            n = len(sentences(para))
            if n > para_cap: long_p.append((line_no, n, para.strip().split("\n")[0]))
        line_no += para.count("\n")
    return long_s, long_p

def wc(s):
    return len([w for w in re.findall(r"[A-Za-z0-9][A-Za-z0-9'\-/]*", s)])

def count_ci(text, phrases):
    n = 0; hits = []
    low = text.lower()
    for ph in phrases:
        for m in re.finditer(r"(?<![a-z])" + re.escape(ph) + r"(?![a-z])", low):
            n += 1; hits.append(ph)
    return n, hits

def noun_trains(text):
    """Runs of 4+ consecutive non-function lowercase words (Rule 2.1 proxy).
    Heuristic marker only - proper nouns break a run, the leading word of each
    sentence is skipped, and the count stays out of the total."""
    hits = []
    for s in sentences(text):
        words = re.findall(r"[A-Za-z][A-Za-z'\-]*", s)[1:]
        run = []
        for w in words + [""]:
            if w and w.lower() not in FUNC_WORDS and not w[0].isupper():
                run.append(w)
            else:
                if len(run) >= 4: hits.append(" ".join(run))
                run = []
    return hits

def lint(text, strict=False, cap=20):
    raw = text
    text = strip_code(text)
    sents = sentences(text)
    words = sum(wc(s) for s in sents) or 1
    v = {}
    longs = [(wc(s), s) for s in sents if wc(s) > cap]
    v[f"long_sentence(>{cap}w)"] = len(longs)
    v["semicolon"] = text.count(";")
    v["contraction"] = len(re.findall(r"\b\w+['’](?:t|re|ve|ll|d|s|m)\b", text))
    passive_parts = re.findall(rf"\b{BE}\s+(\w+ed|{PP_IRREG})\b", text, re.I)
    v["passive_voice"] = sum(1 for p in passive_parts if not re.fullmatch(STATIVE, p, re.I)) \
        + len(re.findall(rf"\b{BE}\s+{STATIVE}\s+by\b", text, re.I))
    v["complex_tense"] = len(re.findall(
        rf"\b(?:(?:may|might|could|would|should|must|will|shall|can)\s+)?(?:have|has|had)\s+(?:been\s+)?(?:\w+ed|{PP_IRREG})\b",
        text, re.I))
    v["ing_main_verb"] = len(re.findall(rf"\b{BE}\s+\w+ing\b", text, re.I))
    v["nominalization"] = len(re.findall(r"\b(?:perform(?:s|ed)?|conduct(?:s|ed)?|carry out|carries out|make use of|makes use of)\b", text, re.I)) + len(re.findall(r"\b\w{4,}(?:tion|ment|ance|ence)\s+of\b", text, re.I))
    v["phrasal_verb"], _ = count_ci(text, PHRASAL)
    v["banned_word"], bh = count_ci(text, BANNED)
    v["marketing_adjective"], mh = count_ci(text, MARKETING)
    v["modal_hedge"], _ = count_ci(text, MODAL_HEDGE)
    paras = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    v["long_paragraph(>6s)"] = sum(1 for p in paras if len(sentences(strip_code(p))) > 6)
    em = raw.count("—") + raw.count("–")
    trains = noun_trains(text)
    if strict:
        n_strict, sh = count_ci(text, STRICT_BANNED)
        # "may" is matched case-sensitively so the month "May" stays clean
        n_strict += len(re.findall(r"(?<![A-Za-z])may(?![a-z])", text))
        v["strict_banned_word"] = n_strict
        v["em_dash"] = em
    total = sum(v.values())
    return {
        "score_version": SCORE_VERSION,
        "mode": "strict" if strict else "flavored",
        "words": words, "sentences": len(sents),
        "violations": v, "total": total,
        "total_per100w": round(total*100.0/words, 2),
        "em_dash(slop-marker)": em,
        "noun_train(>=4w,marker)": len(trains),
        "longest_sentence_words": (max(longs)[0] if longs else max((wc(s) for s in sents), default=0)),
        "sample_marketing": list(dict.fromkeys(mh))[:6],
        "sample_banned": list(dict.fromkeys(bh))[:6],
        "sample_noun_train": trains[:3],
    }

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    strict = "--strict" in args
    as_json = "--json" in args
    show = "--show" in args        # list each long sentence/paragraph with its line
    fail_over = None
    if "--fail-over" in args:
        i = args.index("--fail-over")
        fail_over = float(args[i + 1])
        del args[i:i + 2]
    cap = 20                        # --cap N: long-sentence threshold (STE: 20 instruction, 25 descriptive)
    if "--cap" in args:
        i = args.index("--cap")
        cap = int(args[i + 1])
        del args[i:i + 2]
    files = [a for a in args if a not in ("--strict", "--json", "--show")]
    worst = 0.0
    if not files:
        sys.stdin.reconfigure(encoding="utf-8")
        r = lint(sys.stdin.read(), strict=strict, cap=cap)
        print(json.dumps(r, indent=2))
        worst = r["total_per100w"]
    else:
        exp = []
        for f in files: exp += sorted(glob.glob(f)) if any(c in f for c in "*?[") else [f]
        for f in exp:
            with open(f, encoding="utf-8") as fh: text = fh.read()
            r = lint(text, strict=strict, cap=cap)
            worst = max(worst, r["total_per100w"])
            if as_json:
                print(json.dumps({"file": f, **r}, indent=2))
            else:
                print(f"{os.path.basename(f):32} words={r['words']:4d} total={r['total']:3d} per100w={r['total_per100w']:6.2f} em_dash={r['em_dash(slop-marker)']:2d}")
            if show:
                long_s, long_p = located(text, cap)
                for line_no, n, s in long_s:
                    print(f"  {f}:{line_no}: [{n}w] {s}")
                for line_no, n, first in long_p:
                    print(f"  {f}:{line_no}: [{n} sentences] {first[:80]}")
    if fail_over is not None and worst > fail_over:
        sys.exit(1)
