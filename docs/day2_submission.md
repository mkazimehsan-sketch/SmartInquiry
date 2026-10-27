# Day 2 Submission Notes - Tuesday, 27 October 2026

**Milestone:** Build classification rules

| Required evidence | Where it is |
|-------------------|-------------|
| Working classifier | `classifier.py` and the Streamlit app (`app.py`) shows category + review flag |
| Test results | `docs/test_results_sample.md`, `docs/test_results_unseen.md` |
| Mismatches recorded | `docs/test_results_run1_before_fix.md` + "Mismatches found and fixed" in README |

## Screenshots to take
1. Terminal: `python run_tests.py` showing `15/15 rows pass`.
2. Terminal: `python run_tests.py data/unseen_tests.csv unseen` showing `12/12`.
3. Streamlit app after submitting a pricing message (Category: PRICING, review: No).
4. Streamlit app after a mixed/complaint message (Category: OTHER, review: YES).
5. GitHub repo page after pushing (shows classifier.py and the new commit).

## Short progress text (paste into the form)

> Day 2 - Built a rule-based classifier (classifier.py) for pricing, order, support and other/uncertain, using keywords, a priority order (empty -> complaint -> mixed -> single category -> fallback) and review flags (damaged item, refund, order question without order ID). Tested on my 15 sample inquiries: first run 13/15, found 2 mismatches ("package" and "arrives" wrongly counted as order words), fixed them, now 15/15. Also tested on 12 new unseen messages: 12/12. Documented limitations (English-only keywords, "plan" false positive). Connected the classifier to the Streamlit form, which now shows category and whether human review is needed. Next: draft templates and fallback messages (Day 3).

## Be ready to explain
- **Why rules, not AI?** The brief's beginner path is rule-based; rules are predictable and easy to explain.
- **Why does mixed go to `other`?** The brief says not to guess when a message mixes categories.
- **What is a mismatch?** A row where the classifier's answer differs from the expected answer in the CSV. I recorded them, fixed the rules, and re-ran.
- **Honest limitation:** 15/15 was measured on messages the rules were tuned against, so I added unseen messages; keyword rules still fail on meaning (see README limitations).
