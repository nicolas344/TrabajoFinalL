class Debt:
    def __init__(self, name, amount, interest, termToPay):
        self.name = name
        self.amount = amount
        self.interest = interest
        self.termToPay = termToPay

    def calculate_monthly_installment(self):
            monthly_interest_rate = self.interest
            monthly_installment = self.amount / self.termToPay
            return monthly_installment + self.amount * monthly_interest_rate
