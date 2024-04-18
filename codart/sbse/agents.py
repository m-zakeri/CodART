import random

class GamblerAgent:
    def __init__(self, initial_amount, win_probability):
        self.amount = initial_amount
        self.win_probability = win_probability

    def play(self):
        if self.amount <= 0:
            return False

        bet_amount = 1
        if random.random() < self.win_probability:
            self.amount += bet_amount
        else:
            self.amount -= bet_amount

        return True

class AccountantAgent:
    def __init__(self, initial_amount, win_probability):
        self.amount = initial_amount
        self.win_probability = win_probability

    def play(self):
        if self.amount <= 0:
            return False

        bet_amount = min(1, self.amount)
        if random.random() < self.win_probability:
            self.amount += bet_amount
        else:
            self.amount -= bet_amount

        return True

# Example usage
initial_amount = 10
win_probability = 0.5

gambler = GamblerAgent(initial_amount, win_probability)
accountant = AccountantAgent(initial_amount, win_probability)

num_rounds = 10
for _ in range(num_rounds):
    print("Gambler: Amount =", gambler.amount, "Playing...")
    gambler.play()
    print("Accountant: Amount =", accountant.amount, "Playing...")
    accountant.play()
    print()

print("Final amounts:")
print("Gambler:", gambler.amount)
print("Accountant:", accountant.amount)