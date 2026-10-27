"""SmartInquiry - Day 2: rule-based inquiry classifier.

No AI model is used. The logic is a small set of readable rules:

  Rule order (priority)
  1. Empty / too-short message         -> other, needs review
  2. Find keyword matches per category (pricing / order / support)
  3. Complaint words found             -> other, needs review   (never guess on angry customers)
  4. Two or more categories matched    -> other, needs review   (mixed message)
  5. Exactly one category matched      -> that category
  6. Nothing matched                   -> other, needs review   (fallback)
  7. Extra review flags (see REVIEW_FLAGS), e.g. damaged item, refund,
     or an order question with no order ID -> needs review even if category is clear
"""
import re
from dataclasses import dataclass, field

# Each keyword is a regex that must start at a word boundary, so "price" matches
# "prices" and "pricing", but not "surprise". Add or change keywords here.
CATEGORY_KEYWORDS = {
    "pricing": [
        r"\bprice", r"\bpricing", r"\bcost", r"\bhow much", r"\bdiscount",
        r"\bquote", r"\bplans?\b", r"\bcheap", r"\bfee\b", r"\bfees\b", r"\brate\b",
    ],
    "order": [
        r"\border", r"\btrack", r"\bshipp?", r"\bdeliver", r"\bdispatch",
        r"\bparcel", r"\b(not|hasn'?t|didn'?t) arriv", r"\bsupposed to arrive", r"\bwhere is my",
    ],
    "support": [
        r"\bcrash", r"\blog ?in\b", r"\bpassword", r"\bnot working", r"\bdoesn'?t work",
        r"\bwon'?t (load|open|work)", r"\bbroken", r"\bdamag", r"\bdefect", r"\berror",
        r"\bbug\b", r"\bfaulty", r"\brefund", r"\breplacement", r"\bhelp\b", r"\bproblem",
    ],
}

# Words that signal an unhappy customer: always handled by a human.
COMPLAINT_KEYWORDS = [
    r"\bcomplain", r"\bterrible", r"\bawful", r"\bworst", r"\bangry",
    r"\bunacceptable", r"\bdisappoint", r"\bscam", r"\blegal\b", r"\blawyer",
]

# Messages that need a person even when the category is clear.
REVIEW_FLAGS = {
    "damaged or faulty item": [r"\bdamag", r"\bdefect", r"\bfaulty", r"\bbroken"],
    "refund or replacement": [r"\brefund", r"\breplacement", r"\bmoney back"],
}

MIN_MESSAGE_LENGTH = 5
ORDER_ID_PATTERN = re.compile(r"\b[A-Za-z]{3}-\d{3,}\b")


@dataclass
class Result:
    category: str                       # pricing / order / support / other
    needs_review: bool
    reason: str                         # plain-English explanation (shown to the reviewer)
    matches: dict = field(default_factory=dict)  # category -> list of matched keywords


def _find(patterns, text):
    """Return the list of pattern hits found in text (as the matched strings)."""
    hits = []
    for p in patterns:
        m = re.search(p, text)
        if m:
            hits.append(m.group(0).strip())
    return hits


def classify(message: str, order_id: str = "") -> Result:
    """Classify one inquiry. Never raises; unclear input falls back to 'other'."""
    text = (message or "").lower().strip()

    # Rule 1: empty or too short
    if len(text) < MIN_MESSAGE_LENGTH:
        return Result("other", True, "Message is empty or too short to classify.")

    # Rule 2: keyword matches per category
    matches = {cat: _find(pats, text) for cat, pats in CATEGORY_KEYWORDS.items()}
    matches = {cat: hits for cat, hits in matches.items() if hits}

    # Rule 3: complaint words
    complaints = _find(COMPLAINT_KEYWORDS, text)
    if complaints:
        return Result("other", True,
                      f"Complaint wording detected ({', '.join(complaints)}). A person should reply.",
                      matches)

    # Rule 4: mixed categories
    if len(matches) >= 2:
        return Result("other", True,
                      f"Mixed message: matches {' + '.join(sorted(matches))}. Not guessing; human decides.",
                      matches)

    # Rule 6: nothing matched (fallback)
    if not matches:
        return Result("other", True,
                      "No known keywords found. Ask the customer to clarify.",
                      matches)

    # Rule 5: exactly one category
    category = next(iter(matches))
    needs_review = False
    reasons = [f"Matched {category} keywords: {', '.join(matches[category])}."]

    # Rule 7: extra review flags
    for flag, pats in REVIEW_FLAGS.items():
        if _find(pats, text):
            needs_review = True
            reasons.append(f"Flagged for review: {flag}.")
    if category == "order" and not (order_id.strip() or ORDER_ID_PATTERN.search(message)):
        needs_review = True
        reasons.append("Order question but no order ID given; ask the customer for it.")

    return Result(category, needs_review, " ".join(reasons), matches)
