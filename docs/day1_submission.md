# Day 1 Submission Notes - Monday, 26 October 2026

**Project:** SmartInquiry - Customer Inquiry Classification & Draft Replies
**Milestone:** Map the business workflow

## Evidence checklist (what to attach to the daily Google Form)

| Required evidence | Where it is |
|-------------------|-------------|
| Flowchart | `docs/flowchart.png` (also `docs/flowchart.svg`, `docs/flowchart.md`) |
| 12+ example inquiries | `data/sample_inquiries.csv` (15 inquiries) |
| Input interface | `app.py` - take a screenshot of the running Streamlit form (see below) |
| Repository evidence | GitHub repo link + screenshot of the commit history |

## Screenshots to take (2 minutes)

1. Run `streamlit run app.py`. Screenshot the empty form.
2. Click **Submit** with blank fields. Screenshot the validation errors.
3. Fill in a valid inquiry and submit. Screenshot the green success message and the structured record.
4. Screenshot your GitHub repo page showing the files and the commit.

## Short progress text (paste into the form)

> Day 1 - Mapped the SmartInquiry workflow (intake -> validate -> classify -> draft -> human review) and drew a flowchart. Wrote 15 realistic example inquiries across pricing, order, support and other/uncertain, including mixed-category cases that must go to human review. Built a Streamlit intake form with validation (blank message, invalid email, bad order ID) that produces a structured record. Set up the GitHub repository with README, .gitignore and requirements. Next: keyword-based classification rules (Day 2).

## Design decisions to be able to explain

- **Four categories:** pricing, order, support, other/uncertain. `other` is the safe fallback bucket.
- **Mixed messages go to review:** if a message touches two categories (e.g. rows 12, 13, 15 in the CSV), it is not guessed; a human decides. This follows the hint in the brief.
- **Missing details go to review:** an order-status question with no order ID (row 6) cannot get a useful draft, so the fallback asks for clarification.
- **Never auto-send:** the workflow ends in human approval; nothing is sent automatically.
- **Fake data only:** all names and emails are invented (`example.com`) to respect the brief's privacy rule.
