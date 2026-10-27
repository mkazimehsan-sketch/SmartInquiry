# Classifier test results - unseen_tests.csv

- Inquiries tested: **12**
- Category correct: **12/12**
- Review flag correct: **12/12**
- Fully passing rows: **12/12**

| ID | Message | Expected | Got | Review expected | Review got | Result |
|----|---------|----------|-----|-----------------|------------|--------|
| 101 | What is the cost of the annual subscription? | pricing | pricing | no | no | PASS |
| 102 | Can I get a quote for 50 units? | pricing | pricing | no | no | PASS |
| 103 | My parcel has not arrived yet, can you check the delivery st... | order | order | no | no | PASS |
| 104 | Please track my shipment | order | order | yes | yes | PASS |
| 105 | The website shows an error when I click pay. | support | support | no | no | PASS |
| 106 | I want a refund for my purchase. | support | support | yes | yes | PASS |
| 107 | WHERE IS MY ORDER ORD-7788??? | order | order | no | no | PASS |
| 108 | This is unacceptable, I want to speak to a manager. | other | other | yes | yes | PASS |
| 109 | Are you hiring developers? | other | other | yes | yes | PASS |
| 110 | What is the delivery fee and can you help me log in? | other | other | yes | yes | PASS |
| 111 | Mera order kahan hai? ORD-9000 | order | order | no | no | PASS |
| 112 |     | other | other | yes | yes | PASS |

## Mismatches

None.
