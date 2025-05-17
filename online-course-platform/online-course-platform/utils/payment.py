# utils/payment.py
class PaymentProcessor:
    def __init__(self):
        self.transactions = []

    def process_payment(self, user_email, amount):
        self.transactions.append({"user": user_email, "amount": amount})
        return True
