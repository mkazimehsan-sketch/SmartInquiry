"""SmartInquiry — Day 5: complete workflow demonstration and handover.

Keeps the existing Day 1 intake, Day 2 classifier, and Day 3 draft generator.
Run with: streamlit run app.py
Nothing is sent automatically.
"""
import csv
import json
import re
from datetime import datetime
from pathlib import Path

import streamlit as st

from classifier import classify
from drafts import generate_draft
from validation import validate_inquiry

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SUBMITTED_FILE = DATA_DIR / "submitted_inquiries.jsonl"
REVIEW_LOG_FILE = DATA_DIR / "review_decisions.jsonl"

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ORDER_ID_PATTERN = re.compile(r"^[A-Za-z]{3}-\d{3,}$")


def append_jsonl(path: Path, record: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def build_record(name, email, order_id, message, channel):
    return {
        "inquiry_id": datetime.now().strftime("SI-%Y%m%d-%H%M%S-%f"),
        "received_at": datetime.now().isoformat(timespec="seconds"),
        "customer_name": name.strip(),
        "email": email.strip(),
        "order_id": order_id.strip().upper() or None,
        "channel": channel,
        "message": message.strip(),
        "status": "awaiting_human_review",
    }


TEST_CASES = [
    {"id":"TC01","message":"Hi, how much does your standard package cost?","order_id":"","purpose":"Clear pricing request"},
    {"id":"TC02","message":"Where is my order?","order_id":"ORD-1042","purpose":"Order inquiry with ID"},
    {"id":"TC03","message":"The app keeps crashing when I try to log in.","order_id":"","purpose":"Technical support"},
    {"id":"TC04","message":"Has my order been dispatched yet?","order_id":"","purpose":"Order inquiry missing ID"},
    {"id":"TC05","message":"Is there a cheaper plan? Also the dashboard won't load for me.","order_id":"","purpose":"Mixed pricing and support"},
    {"id":"TC06","message":"Your price is too high and your service is terrible.","order_id":"","purpose":"Complaint wording"},
    {"id":"TC07","message":"hello","order_id":"","purpose":"Too-short / unclear message"},
    {"id":"TC08","message":"The product I received is damaged. I want a replacement.","order_id":"","purpose":"Damaged item / replacement flag"},
    {"id":"TC09","message":"Can you send me a quote for 50 units?","order_id":"","purpose":"Pricing / quotation"},
    {"id":"TC10","message":"My parcel has not arrived yet, can you check the delivery status?","order_id":"","purpose":"Order request missing ID"},
]


def run_test_cases():
    rows = []
    for case in TEST_CASES:
        result = classify(case["message"], case["order_id"])
        draft = generate_draft(case["message"], case["order_id"], "Test Customer")
        # The classifier's existing rules are the expected behavior; the matrix records
        # actual output rather than claiming all inquiries have a predetermined category.
        rows.append({
            "Test ID": case["id"],
            "Purpose": case["purpose"],
            "Customer inquiry": case["message"],
            "Order ID": case["order_id"] or "(none)",
            "Category": result.category,
            "Needs human review": "Yes" if result.needs_review or draft.is_fallback else "No",
            "Draft type": draft.kind,
            "Fallback draft": "Yes" if draft.is_fallback else "No",
            "Placeholder count": len(draft.placeholders),
            "Reviewer note / classifier reason": result.reason + " " + draft.review_note,
            "Test result": "PASS" if bool(draft.text.strip()) and draft.kind else "FAIL",
        })
    return rows


def main():
    st.set_page_config(page_title="SmartInquiry | Final Demo", page_icon="📨", layout="wide")
    st.title("📨 SmartInquiry")
    st.caption("Final Demo — Intake, Classification, Draft & Human Review")
    st.info("Safety rule: generated replies are drafts only. A human must review and approve every reply. This app never sends messages.")
    st.warning("Use fictional/demo data only. Do not enter real customer personal information.")

    tab_intake, tab_tests, tab_guide = st.tabs(["Inquiry workflow", "10-case test matrix", "Day 4 checklist"])

    with tab_intake:
        st.subheader("1. Customer inquiry intake")
        with st.form("inquiry_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            name = col1.text_input("Customer name")
            email = col2.text_input("Customer email")
            order_id = col1.text_input("Order ID (optional)", placeholder="ORD-1042")
            channel = col2.selectbox("Channel", ["Email", "Website form", "Phone note", "Social media"])
            message = st.text_area("Inquiry message", height=145, placeholder="Enter a customer inquiry...")
            submitted = st.form_submit_button("Classify and create draft", type="primary")

        if submitted:
            errors = validate_inquiry(name, email, order_id, message)
            if errors:
                st.session_state.pop("current_inquiry", None)
                for err in errors:
                    st.error(err)
            else:
                record = build_record(name, email, order_id, message, channel)
                result = classify(message, order_id)
                draft = generate_draft(message, order_id, name)
                record.update({
                    "category": result.category,
                    "needs_review": bool(result.needs_review or draft.is_fallback),
                    "classifier_reason": result.reason,
                    "draft_kind": draft.kind,
                    "draft_text": draft.text,
                    "placeholders": draft.placeholders,
                    "status": "awaiting_human_review",
                })
                append_jsonl(SUBMITTED_FILE, record)
                st.session_state["current_inquiry"] = record
                st.session_state["review_decision"] = "Pending review"
                st.session_state["review_note"] = ""
                st.success("Inquiry validated, classified, drafted, and saved for human review.")

        record = st.session_state.get("current_inquiry")
        if record:
            st.divider()
            st.subheader("2. Classification and draft")
            a, b, c = st.columns(3)
            a.metric("Category", record["category"].upper())
            b.metric("Human review", "REQUIRED" if record["needs_review"] else "REQUIRED BEFORE USE")
            c.metric("Draft type", record["draft_kind"].replace("_", " ").title())
            st.caption("Classifier explanation: " + record["classifier_reason"])
            if record["draft_kind"].startswith("fallback_"):
                st.warning("FALLBACK draft: this inquiry is unclear, mixed, a complaint, or missing information. Check it carefully.")
            edited = st.text_area("Editable reply draft", value=record["draft_text"], height=280, key="edited_reply")
            if record["placeholders"]:
                st.info("Placeholders to fill or remove before sending: " + ", ".join(record["placeholders"]))
            st.caption("Approval rule: all placeholders must be filled or removed, and the reviewer must confirm the content is accurate.")

            st.subheader("3. Explicit human review / approval")
            decision = st.radio(
                "Reviewer decision",
                ["Pending review", "Approve draft", "Request changes"],
                horizontal=True,
                key="review_decision",
            )
            reviewer = st.text_input("Reviewer name or initials (demo)", key="reviewer_name")
            review_note = st.text_area("Reviewer notes (optional)", key="review_note", height=80)
            placeholders_remain = bool(re.search(r"\[[A-Z][^\[\]]*\]", edited))
            if placeholders_remain:
                st.warning("Placeholders remain in the draft. For a safe approval, fill in or remove every placeholder first.")
            if decision == "Approve draft" and placeholders_remain:
                st.error("Approval is blocked while placeholders remain.")
            if st.button("Save human review decision", type="primary"):
                if decision == "Pending review":
                    st.info("Still pending. The draft is not approved and must not be sent.")
                elif decision == "Approve draft" and (not edited.strip() or placeholders_remain):
                    st.error("Cannot approve an empty draft or a draft with unresolved placeholders.")
                else:
                    final_status = "approved_by_human_not_sent" if decision == "Approve draft" else "changes_requested"
                    review_record = {
                        "inquiry_id": record["inquiry_id"],
                        "reviewed_at": datetime.now().isoformat(timespec="seconds"),
                        "reviewer": reviewer.strip() or "(not provided)",
                        "decision": decision,
                        "status": final_status,
                        "review_note": review_note.strip(),
                        "final_draft": edited,
                        "sent": False,
                    }
                    append_jsonl(REVIEW_LOG_FILE, review_record)
                    record["status"] = final_status
                    record["review_decision"] = decision
                    record["reviewer"] = review_record["reviewer"]
                    record["review_note"] = review_note.strip()
                    record["draft_text"] = edited
                    st.session_state["current_inquiry"] = record
                    if decision == "Approve draft":
                        st.success("Human approval recorded. The reply is approved but NOT sent.")
                    else:
                        st.warning("Changes requested. Edit the draft and submit it for review again.")
            status = record.get("status", "awaiting_human_review")
            st.write("**Workflow status:** " + status.replace("_", " ").title())
            st.caption("No email, social message, or other external communication is sent by this app.")

    with tab_tests:
        st.subheader("Final workflow test matrix")
        st.write("Run the 10 provided inquiry scenarios against your existing classifier and draft generator.")
        rows = run_test_cases()
        st.dataframe(rows, use_container_width=True, hide_index=True)
        passed = sum(row["Test result"] == "PASS" for row in rows)
        st.metric("Draft-generation checks passed", f"{passed}/{len(rows)}")
        csv_text = "Test ID,Purpose,Customer inquiry,Order ID,Category,Needs human review,Draft type,Fallback draft,Placeholder count,Reviewer note / classifier reason,Test result\n"
        import io
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
        st.download_button("Download test matrix (CSV)", output.getvalue(), "day5_test_matrix.csv", "text/csv")
        st.caption("These checks verify that each scenario produces a non-empty draft and records the existing classifier output. They do not replace a human quality/safety review.")

    with tab_guide:
        st.subheader("Final project checklist")
        checklist = [
            "Explicit human review decision added: pending, approve, or request changes.",
            "Draft remains editable before review.",
            "Approval is blocked if draft is blank or still contains [PLACEHOLDERS].",
            "Review decisions are saved locally to data/review_decisions.jsonl.",
            "Fallback / mixed / complaint / missing-order cases are visibly flagged.",
            "Ten test scenarios are available in the test matrix tab and CSV download.",
            "No reply is sent automatically.",
        ]
        for item in checklist:
            st.write("☑ " + item)
        st.markdown("**Evidence to capture for submission**")
        st.markdown(
            "1. A clear pricing draft with placeholders.\n"
            "2. An order draft with `ORD-1042`.\n"
            "3. A fallback warning for a mixed inquiry.\n"
            "4. An approval-blocked screen while placeholders remain.\n"
            "5. A successful human approval status after placeholders are resolved.\n"
            "6. The 10-case test matrix and CSV download."
        )
        st.markdown("**Limitations:** classifier is keyword/rule based; there is no live order lookup, email verification service, authentication, or message-sending integration. The review log is local demo storage, not a tamper-proof audit system.")


if __name__ == "__main__":
    main()
