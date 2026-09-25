class Bankaccount:
    def __init__(self, account_number, account_holder, account_type, balance, minimum_balance, transaction_history):
        self.account_number = account_number
        self.account_holder = account_holder
        self.account_type = account_type
        self.balance = balance
        self.minimum_balance = minimum_balance
        self.transaction_history = transaction_history

    def deposit(self, amount):
      if(amount > 0):
        self.balance += amount
        self.transaction_history.append(f"Deposited {amount}")
        return self.balance 
      else:
          return f"amount shold greter then 0"

    def withdraw(self, amount):
        if(amount > 0 and self.balance - amount >= self.minimum_balance):
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn {amount}")
            return self.balance
        else:
            return f"not sufficent balence"

    def check_balance(self):
        return self.balance

    def display(self):
        return {
            "account_number": self.account_number,
            "account_holder": self.account_holder,
            "account_type": self.account_type,
            "balance": self.balance,
            "minimum_balance": self.minimum_balance
        }
    def show_transaction_history(self):
        return self.transaction_history


account1 = Bankaccount(101,"Prince Gupta","Savings",10000,2000,[])

print(account1.display())

print(account1.deposit(5000))

print(account1.withdraw(3000))

print(account1.check_balance())

print(account1.show_transaction_history())
