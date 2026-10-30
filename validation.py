"""Input validation shared by the Streamlit UI and automated tests."""
import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
ORDER_ID_PATTERN = re.compile(r"^[A-Za-z]{3}-\d{3,}$")


def validate_inquiry(name: str, email: str, order_id: str, message: str) -> list[str]:
    errors = []
    if not name.strip():
        errors.append("Customer name is required.")
    if not email.strip():
        errors.append("Email is required.")
    elif not EMAIL_PATTERN.match(email.strip()):
        errors.append("Email format looks invalid (example: name@example.com).")
    if order_id.strip() and not ORDER_ID_PATTERN.match(order_id.strip()):
        errors.append("Order ID format should look like ORD-1042 (or leave it blank).")
    if not message.strip():
        errors.append("Message cannot be blank.")
    elif len(message.strip()) < 5:
        errors.append("Message is too short to understand. Please add more detail.")
    return errors
