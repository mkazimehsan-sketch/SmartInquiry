import unittest

from classifier import classify
from drafts import generate_draft
from validation import validate_inquiry


class ValidationTests(unittest.TestCase):
    def test_valid_input_passes(self):
        self.assertEqual(validate_inquiry("Demo User", "demo@example.com", "ORD-1042", "Where is my order?"), [])

    def test_blank_name_is_rejected(self):
        errors = validate_inquiry("", "demo@example.com", "", "Need help please")
        self.assertIn("Customer name is required.", errors)

    def test_invalid_email_is_rejected(self):
        errors = validate_inquiry("Demo User", "not-an-email", "", "Need help please")
        self.assertTrue(any("Email format" in e for e in errors))

    def test_invalid_order_id_is_rejected(self):
        errors = validate_inquiry("Demo User", "demo@example.com", "123", "Where is my order?")
        self.assertTrue(any("Order ID format" in e for e in errors))

    def test_short_message_is_rejected(self):
        errors = validate_inquiry("Demo User", "demo@example.com", "", "hi")
        self.assertTrue(any("too short" in e for e in errors))


class ClassificationAndDraftTests(unittest.TestCase):
    def test_pricing_category(self):
        self.assertEqual(classify("How much does it cost?").category, "pricing")

    def test_order_with_id_category(self):
        result = classify("Where is my order?", "ORD-1042")
        self.assertEqual(result.category, "order")
        self.assertFalse(result.needs_review)

    def test_order_without_id_needs_review_and_fallback(self):
        result = classify("Where is my order?")
        draft = generate_draft("Where is my order?")
        self.assertTrue(result.needs_review)
        self.assertEqual(draft.kind, "fallback_missing_order_id")

    def test_mixed_topics_route_to_other(self):
        result = classify("Is there a cheaper plan? The dashboard won't load.")
        self.assertEqual(result.category, "other")
        self.assertTrue(result.needs_review)

    def test_complaint_routes_to_other(self):
        result = classify("Your service is terrible")
        self.assertEqual(result.category, "other")
        self.assertTrue(result.needs_review)

    def test_all_ten_scenarios_generate_drafts(self):
        cases = [
            ("Hi, how much does your standard package cost?", ""),
            ("Where is my order?", "ORD-1042"),
            ("The app keeps crashing when I try to log in.", ""),
            ("Has my order been dispatched yet?", ""),
            ("Is there a cheaper plan? Also the dashboard won't load for me.", ""),
            ("Your price is too high and your service is terrible.", ""),
            ("hello", ""),
            ("The product I received is damaged. I want a replacement.", ""),
            ("Can you send me a quote for 50 units?", ""),
            ("My parcel has not arrived yet, can you check the delivery status?", ""),
        ]
        self.assertEqual(len(cases), 10)
        for message, order_id in cases:
            draft = generate_draft(message, order_id, "Test Customer")
            self.assertTrue(draft.text.strip())
            self.assertTrue(draft.kind)


if __name__ == "__main__":
    unittest.main()
