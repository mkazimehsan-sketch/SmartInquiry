# Classifier test results - sample_inquiries.csv

- Inquiries tested: **15**
- Category correct: **13/15**
- Review flag correct: **13/15**
- Fully passing rows: **13/15**

| ID | Message | Expected | Got | Review expected | Review got | Result |
|----|---------|----------|-----|-----------------|------------|--------|
| 1 | Hi, how much does your standard package cost? | pricing | other | no | yes | MISMATCH |
| 2 | Do you offer any discounts if I buy 20 units? | pricing | pricing | no | no | PASS |
| 3 | Can you send me your price list for the premium plan? | pricing | pricing | no | no | PASS |
| 4 | Where is my order ORD-1042? It was supposed to arrive yester... | order | order | no | no | PASS |
| 5 | I placed an order last week and want to track my shipment. | order | order | no | no | PASS |
| 6 | Has my order been dispatched yet? | order | order | yes | yes | PASS |
| 7 | The app keeps crashing when I try to log in. Please help. | support | support | no | no | PASS |
| 8 | I forgot my password and the reset email never arrives. | support | other | no | yes | MISMATCH |
| 9 | The product I received is damaged. I want a replacement. | support | support | yes | yes | PASS |
| 10 | What are your opening hours on weekends? | other | other | yes | yes | PASS |
| 11 | Do you collaborate with schools for sponsorship events? | other | other | yes | yes | PASS |
| 12 | Your price is too high and your service is terrible. I want ... | other | other | yes | yes | PASS |
| 13 | How much is shipping, and where is my order ORD-4455? | other | other | yes | yes | PASS |
| 14 | hello | other | other | yes | yes | PASS |
| 15 | Is there a cheaper plan? Also the dashboard won't load for m... | other | other | yes | yes | PASS |

## Mismatches

- **#1** "Hi, how much does your standard package cost?" - expected `pricing` (review=False), got `other` (review=True). Reason given: Mixed message: matches order + pricing. Not guessing; human decides.
- **#8** "I forgot my password and the reset email never arrives." - expected `support` (review=False), got `other` (review=True). Reason given: Mixed message: matches order + support. Not guessing; human decides.
