# Day 3 Submission Notes - Wednesday, 28 October 2026

**Milestone:** Draft helpful responses

| Required evidence | Where it is |
|-------------------|-------------|
| Draft outputs for multiple categories | `docs/draft_examples.md` (27 drafts: pricing, order, support) and the Streamlit app |
| Screenshots of fallback behavior | App screenshots (see below) + fallback drafts in `docs/draft_examples.md` |

## Screenshots to take (run `streamlit run app.py`)
1. **Pricing draft:** message `Hi, how much does your standard package cost?` (no fallback, placeholders listed).
2. **Order draft with ID:** message `Where is my order?` + Order ID `ORD-1042` (draft mentions ORD-1042).
3. **Support draft:** message `The app keeps crashing when I try to log in.`
4. **Fallback - missing info:** message `Has my order been dispatched yet?` with no order ID (yellow FALLBACK warning).
5. **Fallback - mixed:** `Is there a cheaper plan? Also the dashboard won't load for me.`
6. **Fallback - complaint:** `Your price is too high and your service is terrible.`
7. **Fallback - unclear:** `hello`
8. Terminal: `python run_draft_tests.py` showing `27/27 drafts pass safety checks`.
9. GitHub page after push.

## Short progress text (paste into the form)

> Day 3 - Built safe, editable draft replies (drafts.py). Pricing, order and support have templates with [PLACEHOLDERS] for anything the business must supply, so the system never invents prices, policies, order status or refund decisions. Added four fallback drafts (missing order ID, mixed topics, complaint, unclear) that ask for clarification or hand over to a person. The Streamlit app now shows the category, an editable draft, a FALLBACK warning and the list of placeholders to fill. Wrote an automatic safety test over 27 inquiries (no prices, no promises, greeting/sign-off, no invented order ID): 27/27 pass. The test caught a real problem (an example order number that looked real) which I fixed. Next: human review and approval step plus test matrix (Day 4).

## Be ready to explain
- **Why placeholders?** The brief says not to invent prices, policies or order details. A placeholder forces a human to supply the real fact.
- **Why a fallback?** When the message is mixed, unclear, angry or missing information, a wrong confident answer is worse than asking.
- **What the safety test cannot do:** it checks patterns only. A person must still read every draft.
