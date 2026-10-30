# SmartInquiry — Workflow Guide

## End-to-end flow

```text
Customer inquiry
      ↓
Validate required fields and formats
      ↓
Classify using keyword rules
      ↓
Generate category template or clarification fallback
      ↓
Human reviews and edits the draft
      ↓
Pending review ── Request changes
      ↓
Approve only after placeholders are removed and content is checked
      ↓
Record approval locally (NOT SENT)
```

## Input fields

- Customer name: required; used for the greeting.
- Customer email: required; basic email-shape validation only (not email ownership verification).
- Order ID: optional; if supplied, it must resemble `ORD-1042`.
- Channel: Email, Website form, Phone note, or Social media.
- Inquiry message: required and at least five characters.

## Routing outcomes

| Outcome | Typical trigger | Draft behavior |
|---|---|---|
| Pricing | Price, cost, pricing, quote, plan, discount | Pricing template with business-supplied price placeholders |
| Order | Order, tracking, shipment, dispatch, delivery | Order template if an ID is present; otherwise ask for the order number |
| Support | Login, crash, error, not working, help | Support template with verified troubleshooting placeholders |
| Other / uncertain | No match, short input, complaint, or mixed categories | Clarification or human-written fallback |

Complaint language and mixed-topic messages are not guessed. Damaged/faulty items and refund/replacement requests receive additional human review flags.

## Approval safeguards

- The draft is editable.
- A blank draft cannot be approved.
- Any remaining capitalized bracket placeholder blocks approval.
- Reviewer decision, timestamp, reviewer, note, final draft, and `sent: false` are written to the local review log.
- Approval means only that a human reviewed the draft; it does not send the reply.

## Data and boundaries

Use fictional sample information. The app does not connect to live customer accounts, an order database, payment systems, a CRM, or outbound messaging. Verify all prices, policies, order status, tracking details, and support instructions outside this demo before using any wording in a real business context.
