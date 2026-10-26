# SmartInquiry - Customer Inquiry Classification & Draft Replies

Stack & Scale Remote Internship 2026 | Week 01 | AI Agents & Automations

A human-reviewed workflow for a small business support assistant: accept a customer inquiry, classify it, and prepare an editable draft reply from safe templates. **Replies are never auto-sent.**

## Project status (daily progress)

| Day | Milestone | Status |
|-----|-----------|--------|
| 1 (Mon 26 Oct) | Map the workflow, example inquiries, flowchart, intake form, repo | Done |
| 2 (Tue 27 Oct) | Classification rules | Planned |
| 3 (Wed 28 Oct) | Draft templates and fallback | Planned |
| 4 (Thu 29 Oct) | Human review step and test matrix | Planned |
| 5 (Fri 30 Oct) | Full demo, documentation, final handover | Planned |

## Workflow

See [`docs/flowchart.md`](docs/flowchart.md) (Mermaid) or [`docs/flowchart.svg`](docs/flowchart.svg).

`Intake -> Validate -> Classify -> Draft -> Human review`

## Categories

| Category | Typical messages | Handling |
|----------|------------------|----------|
| `pricing` | cost, price, discount, plan, quote | Draft pricing template (no invented prices) |
| `order` | where is my order, tracking, delivery, dispatch | Draft order-status template (needs order ID) |
| `support` | not working, crash, login, damaged, refund | Draft support template |
| `other` | anything unclear, unsupported or mixed | Clarification fallback + flagged for human review |

Rule from the brief: if a message mixes categories (e.g. pricing + complaint), mark it for review instead of guessing.

## Day 1 deliverables

- `data/sample_inquiries.csv` - 15 realistic (fake) inquiries with expected category and whether review is needed. These become the test cases for Day 2.
- `docs/flowchart.md` / `docs/flowchart.svg` - workflow flowchart.
- `app.py` - Streamlit intake form with validation (blank message, bad email, bad order ID) that builds a structured record.

## Setup and run

```bash
git clone <your-repo-url>
cd smartinquiry
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).

## Data and safety

- Only fake/demo data is used. No real customer information, API keys or credentials are committed.
- Submitted test records are written to `data/submitted_inquiries.jsonl`, which is git-ignored.

## Known limitations (Day 1)

- Classification, drafting and review are not implemented yet (Days 2-4).
- Validation is basic (regex checks), not full email verification.

## Credits and AI assistance

Project structure, example inquiries and starter code were drafted with help from Claude (Anthropic) and then reviewed and understood by the author. Update this section with your own changes as you go.
