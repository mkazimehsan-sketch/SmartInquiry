# SmartInquiry Workflow (Mermaid source)

GitHub renders the diagram below automatically. A standalone image is in `flowchart.svg`.

```mermaid
flowchart TD
    A([Customer inquiry arrives]) --> B[1. INTAKE<br/>name, email, order ID, message]
    B --> C{2. VALIDATE<br/>message not blank?<br/>email format OK?}
    C -- no --> E[Show error,<br/>ask user to fix input]
    E --> B
    C -- yes --> D[3. CLASSIFY<br/>keyword rules:<br/>pricing / order / support / other]
    D --> F{One clear<br/>category?}
    F -- yes --> G[4a. DRAFT<br/>category template + placeholders]
    F -- "no: mixed / unclear / unsupported" --> H[4b. FALLBACK DRAFT<br/>ask for clarification, flag for review]
    G --> I[5. HUMAN REVIEW<br/>assistant reads and edits draft]
    H --> I
    I --> J{Approve draft?}
    J -- no --> K[Reviewer edits draft] --> I
    J -- yes --> L([Reply marked APPROVED<br/>human sends manually])
```

## Step notes

| Step | What happens | Output |
|------|--------------|--------|
| 1. Intake | Support assistant enters the inquiry in a form | Structured record (name, email, order ID, message, timestamp) |
| 2. Validate | Reject blank messages and malformed emails | Valid record or an error message |
| 3. Classify | Keyword rules with priority and fallback (built Day 2) | `pricing`, `order`, `support` or `other` |
| 4. Draft | Category template, or a clarification fallback (built Day 3) | Editable draft text |
| 5. Human review | Explicit approve step before anything is final (built Day 4) | Approved or revised reply |

**Key rule:** if a message mixes categories (for example pricing and a complaint) it is marked `other` and sent to human review rather than guessed.
