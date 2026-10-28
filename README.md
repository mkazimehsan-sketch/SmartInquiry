# SmartInquiry - Customer Inquiry Classification & Draft Replies

Stack & Scale Remote Internship 2026 | Week 01 | AI Agents & Automations

A human-reviewed workflow for a small business support assistant: accept a customer inquiry, classify it, and prepare an editable draft reply from safe templates. **Replies are never auto-sent.**

## Project status (daily progress)

| Day | Milestone | Status |
|-----|-----------|--------|
| 1 (Mon 26 Oct) | Map the workflow, example inquiries, flowchart, intake form, repo | Done |
| 2 (Tue 27 Oct) | Classification rules and test results | Done |
| 3 (Wed 28 Oct) | Draft templates and fallback | Done |
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

## Day 3 deliverables - draft replies

- `drafts.py` - builds an editable draft for each inquiry:
  - **Category templates** for pricing, order and support. Anything the business must supply (prices, order status, troubleshooting steps) is a `[PLACEHOLDER]`, never an invented fact.
  - **Fallback drafts** that ask for clarification or hand over to a person: `missing_order_id`, `mixed` topics, `complaint`, `unclear`.
  - Damaged-item / refund messages get a note: "do not promise a refund or replacement until approved".
  - An order ID is written into a draft only if the customer gave one.
- `run_draft_tests.py` - generates drafts for all 27 test inquiries and runs automatic safety checks (no prices, no promises, greeting and sign-off present, no invented order ID, expected fallback used).
- `docs/draft_examples.md` - every generated draft with its placeholders and safety result.
- `app.py` - after submit, shows the category, an editable draft, a FALLBACK warning when relevant and the list of placeholders to fill.

Result: **27/27 drafts pass safety checks.** Run: `python run_draft_tests.py`

**Problems found and fixed:** (1) the "missing order number" fallback used the example `ABC-1234`, which looks like a real order ID, so it was replaced by a placeholder; (2) the placeholder detector missed placeholders containing lowercase letters; (3) the app saved the record before the draft was created, so `draft_kind` was missing from the saved record.

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

## Known limitations

- Human review/approval step is not implemented yet (Day 4).
- Drafts are English only and generic; the business must fill in every `[PLACEHOLDER]`.
- Safety checks only look for the patterns listed in `run_draft_tests.py`; they cannot catch every possible unsafe sentence, so a person must always read the draft.
- Validation is basic (regex checks), not full email verification.
- The classifier only understands English keywords. Roman Urdu such as "Kitni qeemat hai?" falls back to `other` + review (safe, but not helpful).
- "In order to join..." contains the word "order" and is treated as an order question (it is flagged for review because there is no order ID).
- "Do you have a plan to open a new branch?" is wrongly classified as `pricing` without review, because "plan" is a pricing keyword. Keyword rules cannot understand meaning; a future fix is to require two signals or add more exceptions.
- A negated complaint ("this is not a complaint") still counts as a complaint. That is safe because it goes to a human.

## Credits and AI assistance

Project structure, example inquiries and starter code were drafted with help from Claude (Anthropic) and then reviewed and understood by the author. Update this section with your own changes as you go.
