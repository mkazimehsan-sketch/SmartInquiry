# SmartInquiry - Customer Inquiry Classification & Draft Replies

Stack & Scale Remote Internship 2026 | Week 01 | AI Agents & Automations

A human-reviewed workflow for a small business support assistant: accept a customer inquiry, classify it, and prepare an editable draft reply from safe templates. **Replies are never auto-sent.**

## Project status (daily progress)

| Day | Milestone | Status |
|-----|-----------|--------|
| 1 (Mon 26 Oct) | Map the workflow, example inquiries, flowchart, intake form, repo | Done |
| 2 (Tue 27 Oct) | Classification rules and test results | Done |
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

## Day 2 deliverables - classification rules

- `classifier.py` - rule-based classifier (no AI model). Rules run in priority order:
  1. empty/too-short message -> `other` + review
  2. complaint words (terrible, complain, unacceptable...) -> `other` + review
  3. keywords from two or more categories (mixed) -> `other` + review
  4. keywords from exactly one category -> that category
  5. no keywords at all -> `other` (fallback) + review
  6. extra review flags: damaged/faulty item, refund/replacement, order question without an order ID
- `run_tests.py` - runs the classifier on a CSV and writes a results table with mismatches.
- `data/unseen_tests.csv` - 12 extra messages written after the rules, to check the rules are not just memorising the samples.
- `docs/test_results_*.md` - results (see below).

### Test results

| Test set | Result |
|----------|--------|
| `sample_inquiries.csv`, first run | 13/15 pass (2 mismatches) - `docs/test_results_run1_before_fix.md` |
| `sample_inquiries.csv`, after fixes | 15/15 pass - `docs/test_results_sample.md` |
| `unseen_tests.csv` (new messages) | 12/12 pass - `docs/test_results_unseen.md` |

**Mismatches found and fixed:** the words "package" and "arrives" were counted as order keywords, so "how much does your standard package cost?" and "the reset email never arrives" were wrongly treated as mixed. Fixed by removing "package" and matching "arrive" only in phrases like "has not arrived".

Run the tests: `python run_tests.py` and `python run_tests.py data/unseen_tests.csv unseen`

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

- Drafting and review are not implemented yet (Days 3-4).
- Validation is basic (regex checks), not full email verification.
- The classifier only understands English keywords. Roman Urdu such as "Kitni qeemat hai?" falls back to `other` + review (safe, but not helpful).
- "In order to join..." contains the word "order" and is treated as an order question (it is flagged for review because there is no order ID).
- "Do you have a plan to open a new branch?" is wrongly classified as `pricing` without review, because "plan" is a pricing keyword. Keyword rules cannot understand meaning; a future fix is to require two signals or add more exceptions.
- A negated complaint ("this is not a complaint") still counts as a complaint. That is safe because it goes to a human.

## Credits and AI assistance

Project structure, example inquiries and starter code were drafted with help from Claude (Anthropic) and then reviewed and understood by the author. Update this section with your own changes as you go.
