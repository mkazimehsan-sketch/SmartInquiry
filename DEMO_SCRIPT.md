# Friday Screen-Recording Demo Script (about 2–3 minutes)

**Before recording:** Start the app with `python -m streamlit run app.py`, open the local URL, and use fictional details only. Close unrelated tabs and make sure the app is readable.

## 1. Introduction (15–20 seconds)

"Hello, this is my SmartInquiry project for the Stack & Scale Week 1 internship. It helps a small business organize customer inquiries, classify them, prepare editable response drafts, and keep a human in control before any reply is used."

## 2. Demonstrate a clear pricing inquiry (30 seconds)

- Enter a demo name and email.
- Message: `Hi, how much does your standard package cost?`
- Select **Classify and create draft**.
- Show the pricing category, reason, editable draft, and pricing placeholders.

Say: "The system detects a pricing request and prepares a template. It does not invent a price; a team member must add verified pricing."

## 3. Demonstrate order tracking (25 seconds)

- Use message: `Where is my order?`
- Order ID: `ORD-1042`
- Submit and show the order draft.

Say: "The provided order number is included in the draft, but this demo does not connect to a real order database, so it cannot claim a live delivery status."

## 4. Demonstrate human review safeguards (35 seconds)

- Show the editable draft with placeholders still present.
- Choose **Approve draft** and save; show that approval is blocked.
- Explain that the reviewer must fill or remove placeholders and verify the wording.
- Do not claim a reply was sent.

Say: "Even after a human approves, the status is approved but not sent. This project intentionally has no automatic sending integration."

## 5. Demonstrate fallback and test matrix (25 seconds)

- Submit a mixed inquiry such as: `Is there a cheaper plan? Also the dashboard won't load for me.`
- Show the fallback/review warning.
- Open the **10-case test matrix** tab and briefly show the scenarios and CSV download.

## 6. Close (10–15 seconds)

"I tested pricing, order, support, mixed, complaint, and unclear inquiries. The main limitation is that classification uses keyword rules and there is no live business-system integration. The project is documented in the README, and the source code and test evidence are included in my submission."

**Recording reminder:** Save the actual screen recording and submit its viewable file/link through the official Friday Google Form. Do not use mock screenshots as evidence of a live run.
