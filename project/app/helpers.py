import re

# ---------------- BASIC CLEAN ----------------

def clean(text):
    return re.sub(r"\s+", " ", str(text).lower().strip())

def numbers(text):
    return [int(x) for x in re.findall(r"\d+", str(text))]

def normalize(text):
    return str(text).lower().replace(" ", "").replace("_", "")


# ---------------- KEYWORDS ----------------

ROLL_KEYS  = ["roll", "application", "reg", "registration"]
SCORE_KEYS = ["score", "marks", "neet"]
RANK_KEYS  = ["rank", "air"]
NAME_KEYS  = ["name"]
CAT_KEYS   = ["category", "cat", "quota"]

# ---------------- CHECKS ----------------

def is_roll(text):
    return any(k in text for k in ROLL_KEYS)

# ---------------- FINDERS ----------------

def find_score(row):
    for k, v in row.items():
        text = clean(k + " " + v)
        if any(x in text for x in SCORE_KEYS) and not is_roll(text):
            for n in numbers(v):
                if 100 <= n <= 720:   # ✔ NEET score range
                    return n
    return None


def find_rank(row):
    for k, v in row.items():
        text = clean(k + " " + v)
        if any(x in text for x in RANK_KEYS) and not is_roll(text):
            for n in numbers(v):
                if n > 720:          # ✔ rank always > score
                    return n
    return None


def find_value(row, keys):
    for k, v in row.items():
        if any(x in clean(k) for x in keys):
            return v.strip()
    return None


def extract_college_name(doc):
    for p in doc.paragraphs[:10]:
        if "college" in p.text.lower():
            return p.text.strip()
    return "UNKNOWN"
