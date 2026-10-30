# Day 4 Submission Notes — SmartInquiry

**Project:** SmartInquiry — Customer inquiry intake, classification, and draft replies  
**Milestone:** Human Review & Workflow Testing

## What was implemented
- Kept the uploaded Day 2 `classifier.py` and Day 3 `drafts.py` logic.
- Added an explicit human review stage to the existing Streamlit app.
- Added Pending review, Approve draft, and Request changes decisions.
- Approval is blocked if the draft is empty or still contains capitalized placeholders.
- Review decisions are written to a local JSONL file with timestamp, reviewer, decision, final draft, and `sent: false`.
- Added a 10-case matrix that runs against the actual classifier and draft generator.
- Added a CSV download in the app.
- Preserved the safety rule: no automatic sending, no invented prices/order statuses/policies/refund decisions.

## Test coverage
1. Pricing request.
2. Order request with `ORD-1042`.
3. Technical support request.
4. Order inquiry without an order ID.
5. Mixed pricing and support request.
6. Complaint wording.
7. Short/unclear message.
8. Damaged item and replacement request.
9. Quotation request.
10. Delivery/parcel inquiry without an order ID.

## Screenshots to capture after running the app
1. Pricing draft with placeholders listed.
2. Order draft with the supplied `ORD-1042`.
3. Mixed-topic fallback warning.
4. Approval blocked while placeholders remain.
5. Approved-by-human status after resolving placeholders.
6. The 10-case test matrix in the app.

## Progress text for submission form
Day 4 — Extended my existing SmartInquiry project without replacing the Day 2 classifier or Day 3 draft templates. Added a human review step with pending, approve, and request-changes decisions. The draft remains editable, and approval is blocked if the draft is blank or contains unresolved placeholders. Review decisions are recorded locally and the system never sends messages automatically. Added a 10-case workflow test matrix covering pricing, orders, support, missing information, mixed topics, complaints, and unclear input. The app can export the test matrix as CSV. Screenshots should be captured after running the app locally.

## Honest evidence note
The code and test scenarios are included. Screenshots and local interactive execution evidence still need to be captured by running the app on your machine.
