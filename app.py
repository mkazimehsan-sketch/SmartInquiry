"""SmartInquiry - Day 1: intake form + validation.

Run with:  streamlit run app.py

Day 1 scope: capture an inquiry as a structured record and validate it.
Classification (Day 2), drafting (Day 3) and review (Day 4) come later.
"""
import json
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

DATA_DIR = Path(__file__).parent / "data"
SUBMITTED_FILE = DATA_DIR / "submitted_inquiries.jsonl"  # git-ignored, local only

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ORDER_ID_PATTERN = re.compile(r"^[A-Za-z]{3}-\d{3,}$")  # e.g. ORD-1042


def validate_inquiry(name: str, email: str, order_id: str, message: str) -> list[str]:
    """Return a list of error messages (empty list means the input is valid)."""
    errors = []
    if not name.strip():
        errors.append("Customer name is required.")
    if not email.strip():
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(email.strip()):
        errors.append("Email format looks invalid (example: name@example.com).")
    if order_id.strip() and not ORDER_ID_PATTERN.match(order_id.strip()):
        errors.append("Order ID format should look like ORD-1042 (or leave it blank).")
    if not message.strip():
        errors.append("Message cannot be blank.")
    elif len(message.strip()) < 5:
        errors.append("Message is too short to understand. Please add more detail.")
    return errors


def build_record(name: str, email: str, order_id: str, message: str, channel: str) -> dict:
    """Turn raw form input into one structured inquiry record."""
    return {
        "received_at": datetime.now().isoformat(timespec="seconds"),
        "customer_name": name.strip(),
        "email": email.strip(),
        "order_id": order_id.strip().upper() or None,
        "channel": channel,
        "message": message.strip(),
        "status": "received",  # later: classified -> drafted -> approved
    }


def save_record(record: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with SUBMITTED_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> None:
    st.set_page_config(page_title="SmartInquiry", page_icon="📨")
    st.title("📨 SmartInquiry")
    st.caption("Customer inquiry intake - Day 1 (human-reviewed workflow, never auto-sends)")
    st.info("Use fake/demo data only. Do not enter real customer personal information.")

    with st.form("inquiry_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        name = col1.text_input("Customer name")
        email = col2.text_input("Customer email")
        order_id = col1.text_input("Order ID (optional)", placeholder="ORD-1042")
        channel = col2.selectbox("Channel", ["Email", "Website form", "Phone note", "Social media"])
        message = st.text_area("Inquiry message", height=150)
        submitted = st.form_submit_button("Submit inquiry")

    if submitted:
        errors = validate_inquiry(name, email, order_id, message)
        if errors:
            for err in errors:
                st.error(err)
        else:
            record = build_record(name, email, order_id, message, channel)
            save_record(record)
            st.success("Inquiry received and validated. Next steps (Days 2-4): classify -> draft -> human review.")
            st.subheader("Structured record")
            st.json(record)


if __name__ == "__main__":
    main()
