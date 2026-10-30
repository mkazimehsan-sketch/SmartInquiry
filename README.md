# SmartInquiry — Customer Inquiry Classification & Draft Replies

A beginner-friendly Python + Streamlit project that captures customer inquiries, classifies them with transparent keyword rules, creates an editable response draft, and requires a human decision before a reply is considered approved.

**Safety principle:** SmartInquiry never sends an email, social message, or other customer communication. An approval is only recorded locally as `approved_by_human_not_sent`.

## 1. Features

- Structured inquiry intake: customer name, email, optional order ID, channel, and message.
- Input validation for required fields, email shape, order ID format, and minimum message length.
- Four outcomes: `pricing`, `order`, `support`, and `other` (fallback/uncertain).
- Rule-based classification with visible reasons and review flags.
- Category-specific editable drafts and clarification fallbacks.
- Explicit reviewer decisions: Pending review, Approve draft, or Request changes.
- Approval is blocked when the draft is blank or contains unresolved capitalized placeholders such as `[ORDER STATUS: ...]`.
- Local JSON Lines records for submitted inquiries and review decisions.
- Ten repeatable test scenarios displayed in the Streamlit app and downloadable as CSV.

## 2. Project structure

```text
SmartInquiry_Day5_Final/
├── app.py                  # Streamlit user interface and end-to-end workflow
├── validation.py           # Shared input validation rules
├── classifier.py           # Day 2 keyword classification rules
├── validation.py           # Shared input validation rules
├── drafts.py               # Day 3 safe response templates and fallbacks
├── requirements.txt        # Python dependency
├── day5_test_matrix.csv    # Existing 10-scenario test evidence
├── tests/
│   └── test_workflow.py    # Repeatable validation/classifier/draft checks
├── data/                   # Created at runtime; local JSONL logs (git-ignored)
├── README.md               # Setup, usage, rules, limitations
├── WORKFLOW_GUIDE.md       # Process and decision rules
├── DEMO_SCRIPT.md          # Suggested screen-recording walkthrough
└── FINAL_HANDOVER_CHECKLIST.md
```

## 3. Requirements and setup

- Python 3.10 or newer
- Internet is only needed to install Streamlit the first time; the app itself runs locally.

### Windows (PowerShell or Git Bash)

```bash
cd SmartInquiry_Day5_Final
python -m venv .venv
```

Activate the environment:

```bash
# PowerShell
.venv\Scripts\Activate.ps1

# Git Bash
source .venv/Scripts/activate
```

Install and launch:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit prints a local URL (normally `http://localhost:8501`). Open it in your browser. If Streamlit is already installed in the active Python environment, run only `python -m streamlit run app.py`.

## 4. How to use the app

1. Open **Inquiry workflow**.
2. Enter fictional/demo customer details. Do not use real customer personal data.
3. Enter a message and optional order ID, then select **Classify and create draft**.
4. Review the category, explanation, review warning, and generated response.
5. Edit the draft. Fill in or remove every `[CAPITALIZED PLACEHOLDER]` using verified business information.
6. Enter reviewer initials/name and choose **Approve draft** or **Request changes**.
7. Select **Save human review decision**. Approval is recorded as approved-but-not-sent; no external message is transmitted.
8. Open **10-case test matrix** to inspect the scenarios and download the CSV.

## 5. Classification rules

Rules are evaluated in a deliberate order:

1. Empty or too-short message → `other`, human review.
2. Match keyword groups for pricing, order, and support.
3. Complaint language → `other`, human review.
4. Two or more matched categories → `other`, human review (mixed request).
5. No category match → `other`, clarification fallback.
6. Exactly one category → that category.
7. Additional review flags apply to damaged/faulty items, refund/replacement language, and order requests without an order ID.

See `classifier.py` for the exact keyword lists and regex patterns. See `drafts.py` for response wording and placeholders.

## 6. Test and verify

Run the automated checks from the project root:

```bash
python -m unittest discover -s tests -v
```

Then launch the UI and manually verify:

- Pricing inquiry produces a pricing draft.
- `Where is my order?` with `ORD-1042` produces an order draft.
- An order inquiry without an ID asks the customer for the order number.
- Mixed, complaint, and unclear messages are routed to a fallback/reviewer.
- Approval is blocked while placeholders remain.
- After placeholders are resolved, a reviewer can record approval; the record still says `sent: false`.
- Blank or malformed input is rejected.

The test matrix records the actual classifier/draft outputs; a non-empty draft check does not prove that every response is factually correct. Human review remains necessary.

## 7. Local records and privacy

The app creates a `data/` folder when records are saved:

- `data/submitted_inquiries.jsonl`
- `data/review_decisions.jsonl`

These are local demo records and are excluded from Git by `.gitignore`. Use fictional data only. Never commit customer details, credentials, API keys, or private business information.

## 8. Known limitations

- Classification is deterministic keyword/rule matching, not an AI/LLM model; wording outside the keyword lists may be misclassified.
- No live order-management lookup, tracking integration, pricing database, CRM, email verification, authentication, role management, or message-sending service is connected.
- Draft placeholders must be completed with verified company information by a person.
- JSONL logs are local and are not encrypted, authenticated, tamper-proof, or shared across devices.
- The current test suite checks validation and core classification/draft behavior; it does not replace full manual UI testing or human factual review.

## 9. GitHub publishing

Create an empty public or private repository on GitHub, then run these commands in this folder (replace the URL with your own repository URL):

```bash
git init
git add .
git status
git commit -m "Complete SmartInquiry Week 1 project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/SmartInquiry.git
git push -u origin main
```

Check `git status` before pushing. Confirm that `data/`, `.venv/`, and secrets are not staged. After pushing, copy the repository URL into the official Friday submission form.

## 10. Final submission items

- Accessible GitHub repository URL (after you publish it).
- This README and the workflow guide.
- Source files and test matrix.
- Actual screenshots captured from the running local app.
- A short screen recording following `DEMO_SCRIPT.md`.
- Official Google Form submission.

See `FINAL_HANDOVER_CHECKLIST.md` before submitting.
