import unittest
from ai_classification import classify_lead

class TestClassification(unittest.TestCase):
    def setUp(self):
        self.base_payload = {
            "name": "Test User",
            "email": "test@example.com",
            "message": "",
            "status": "valid",
            "intent": "",
            "urgency": ""
        }

    def test_support_intent(self):
        payload = self.base_payload.copy()
        payload["message"] = "I need help"
        result = classify_lead(payload)
        self.assertEqual(result["intent"], "Support")
        print(f"\nTest 1 - Message: '{payload['message']}'")
        print(f"Result -> Intent: {result['intent']}, Urgency: {result['urgency']}")

    def test_sales_intent(self):
        payload = self.base_payload.copy()
        payload["message"] = "I want to buy"
        result = classify_lead(payload)
        self.assertEqual(result["intent"], "Sales")
        print(f"\nTest 2 - Message: '{payload['message']}'")
        print(f"Result -> Intent: {result['intent']}, Urgency: {result['urgency']}")

    def test_partnership_intent(self):
        payload = self.base_payload.copy()
        payload["message"] = "Let's collaborate"
        result = classify_lead(payload)
        self.assertEqual(result["intent"], "Partnership")
        print(f"\nTest 3 - Message: '{payload['message']}'")
        print(f"Result -> Intent: {result['intent']}, Urgency: {result['urgency']}")
        
    def test_urgency_high(self):
        payload = self.base_payload.copy()
        payload["message"] = "I need help ASAP"
        result = classify_lead(payload)
        self.assertEqual(result["urgency"], "High")
        print(f"\nTest 4 (Urgency) - Message: '{payload['message']}'")
        print(f"Result -> Intent: {result['intent']}, Urgency: {result['urgency']}")

if __name__ == '__main__':
    unittest.main()
