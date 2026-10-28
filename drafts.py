"""SmartInquiry - Day 3: safe, editable draft replies.

Safety rules for every draft:
  * NEVER invent prices, policies, delivery dates, order status or refund decisions.
    Anything the business must supply is a [PLACEHOLDER IN CAPITALS].
  * An order ID is only written into a draft if the customer actually gave one.
  * Drafts are for a human to edit and approve. Nothing is sent automatically.
  * Unclear / mixed / complaint / missing-information messages get a FALLBACK draft
    that asks for clarification or hands over to a person.
"""
import re
from dataclasses import dataclass

from classifier import (COMPLAINT_KEYWORDS, ORDER_ID_PATTERN, REVIEW_FLAGS, _find,
                        classify)

SIGN_OFF = "Kind regards,\n[YOUR NAME]\n[BUSINESS NAME]"
PLACEHOLDER_PATTERN = re.compile(r"\[[A-Z][^\[\]]*\]")  # [CAPITAL START ...]

# ---- Category templates (used when the category is clear) -------------------
TEMPLATES = {
    "pricing": (
        "Hi {name},\n\n"
        "Thank you for your interest in {business}. We'd be happy to help with pricing.\n\n"
        "[PRICING DETAILS: add the current price / plan information here before sending]\n\n"
        "If you can tell us [WHAT WE NEED TO KNOW, e.g. quantity or plan], "
        "we can prepare an accurate quote for you.\n\n"
    ),
    "order": (
        "Hi {name},\n\n"
        "Thank you for contacting {business} about order {order_id}. "
        "We are checking it for you.\n\n"
        "[ORDER STATUS: check the order system and add the real status / tracking details here]\n\n"
        "If anything looks wrong, just reply to this message and we will look into it.\n\n"
    ),
    "support": (
        "Hi {name},\n\n"
        "Sorry to hear you are having trouble, and thank you for letting {business} know.\n\n"
        "[SUPPORT STEPS: add the correct troubleshooting steps or next action here]\n\n"
        "To help us look into it faster, could you reply with [DETAILS NEEDED, "
        "e.g. what you see on screen, device, or when it started]?\n\n"
    ),
}

# Extra paragraph for support messages about damaged items / refunds (no promises!).
SENSITIVE_SUPPORT_NOTE = (
    "[REFUND / REPLACEMENT DECISION: a team member must decide this. "
    "Do not promise a refund or replacement until it is approved]\n\n"
)

# ---- Fallback templates (used when we should not guess) ----------------------
FALLBACKS = {
    "missing_order_id": (
        "Hi {name},\n\n"
        "Thank you for contacting {business}. We would be glad to check on your order, "
        "but we could not find an order number in your message.\n\n"
        "Could you please reply with your order number (you can find it in [WHERE THE CUSTOMER FINDS THE ORDER NUMBER, e.g. confirmation email])?\n\n"
    ),
    "mixed": (
        "Hi {name},\n\n"
        "Thank you for contacting {business}. Your message covers more than one topic, "
        "and we want to make sure each part is handled properly.\n\n"
        "[TOPICS DETECTED: {topics}. Reviewer: answer each part or split into separate replies]\n\n"
        "Could you confirm which of these is most urgent for you?\n\n"
    ),
    "complaint": (
        "Hi {name},\n\n"
        "Thank you for telling us, and we are sorry for your experience with {business}. "
        "We take this seriously and a member of our team will review your message personally.\n\n"
        "[PERSONAL RESPONSE: reviewer to write a specific reply. Do not promise compensation or outcomes yet]\n\n"
        "To help us understand what happened, could you share [DETAILS NEEDED, e.g. order number, date, what went wrong]?\n\n"
    ),
    "unclear": (
        "Hi {name},\n\n"
        "Thank you for contacting {business}. We want to help, but we are not sure we "
        "understood your request.\n\n"
        "Could you please tell us a little more about what you need, for example a question "
        "about [PRICING / YOUR ORDER / A PROBLEM YOU ARE HAVING]?\n\n"
    ),
}


@dataclass
class Draft:
    kind: str            # pricing / order / support / fallback_<type>
    is_fallback: bool
    text: str            # the full editable draft
    placeholders: list   # placeholders the reviewer MUST fill or remove
    review_note: str     # short note for the human reviewer


def _fill(template: str, name: str, business: str, **extra) -> str:
    return (template.format(name=name or "there", business=business, **extra) + SIGN_OFF)


def _finish(kind, is_fallback, text, note) -> Draft:
    found = []
    for p in PLACEHOLDER_PATTERN.findall(text):
        if p not in found:
            found.append(p)
    return Draft(kind, is_fallback, text, found, note)


def generate_draft(message: str, order_id: str = "", customer_name: str = "",
                   business: str = "[BUSINESS NAME]") -> Draft:
    """Build an editable draft for one inquiry. Never raises, never invents facts."""
    result = classify(message, order_id)
    text = (message or "").lower()
    name = (customer_name or "").strip().split(" ")[0] if customer_name else ""
    found_id = ORDER_ID_PATTERN.search(message or "")
    given_id = order_id.strip().upper() or (found_id.group(0).upper() if found_id else "")

    # --- fallbacks first: do not guess ---
    if _find(COMPLAINT_KEYWORDS, text):
        return _finish("fallback_complaint", True, _fill(FALLBACKS["complaint"], name, business),
                       "Complaint wording. Write a personal reply; do not promise outcomes.")
    if len(result.matches) >= 2:
        topics = " + ".join(sorted(result.matches))
        return _finish("fallback_mixed", True, _fill(FALLBACKS["mixed"], name, business, topics=topics),
                       f"Mixed topics ({topics}). Human decides how to answer.")
    if result.category == "other":
        return _finish("fallback_unclear", True, _fill(FALLBACKS["unclear"], name, business),
                       "No clear category. Ask the customer to clarify.")
    if result.category == "order" and not given_id:
        return _finish("fallback_missing_order_id", True, _fill(FALLBACKS["missing_order_id"], name, business),
                       "Order question without an order number. Ask for it.")

    # --- clear category: use the template ---
    body = TEMPLATES[result.category]
    if result.category == "support" and any(_find(p, text) for p in REVIEW_FLAGS.values()):
        # insert the 'no promises' note before the closing question
        body = body.replace("To help us look into it", SENSITIVE_SUPPORT_NOTE + "To help us look into it")
    note = ("Check every [PLACEHOLDER] before sending. " +
            ("Sensitive topic: needs a person to decide." if result.needs_review else "Edit freely."))
    return _finish(result.category, False, _fill(body, name, business, order_id=given_id), note)
