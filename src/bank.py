"""holds data of integer that is the money and account id in integer if it dosent have any string account owner in string and transaction history in a simple table list with timestamps
what does bank do transaction and withdrawl and deposit money and the transaction is initiated by user
it should refuse inputs which are larger than 1 limit of the day and cant be larger than the money balance you have else you gotta take a loan and strictly integer which is greater than 0 or greater than 200 rupees
if withdrawing money and inputing pin and more than 2 wrong pin or password in one session diffrent type of error and red alert with blocking the card and session is ofcourse over"""

from decimal import Decimal
import hashlib
from datetime import datetime
from typing import Any

class InsufficientFundsError(Exception):
    def __init__(self, balance: Decimal, requested_amount: Decimal):
        self.balance = Decimal(str(balance))
        self.requested_amount = Decimal(str(requested_amount))

        super().__init__(f"Attempted to request {self.requested_amount}, but available balance is only {self.balance}.")
    
class CardBlockError(Exception):
    def __init__(self,account_id: int, reason: str):
        self.account_id = account_id
        self.reason = reason

        super().__init__(f"Account {account_id} has been blocked. Reason: {reason}")
        #super().__init__() passes data up to the parent class

class InvalidPINError(Exception):
    def __init__(self,remaining_attempts: int):
        self.remaining_attempts = remaining_attempts

        super().__init__(
            f"Incorrect PIN. {remaining_attempts} attemp(s) remaining before the card is blocked"
        )

class BankAccount:
    def __init__(self, account_id: int, owner_name: str, initial_balance: Decimal, plaintext_pin: str):
        # Write the lines below using 'self' to store these values. 
        # Remember: Do NOT store the plaintext_pin directly. Hash it first.

        self.account_id = account_id
        self.owner_name = owner_name
        # self.initial_balance = Decimal(str(initial_balance)) this shouldnt change its static
        self.balance = Decimal(str(initial_balance))
        self.hashed_pin = hashlib.sha256(plaintext_pin.encode("utf-8")).hexdigest()

        """.encode("utf-8"): Converts the standard Python string into a bytes-like object, 
        which the hashlib module requires.hashlib.sha256(...): Computes the SHA-256 cryptographic hash of those bytes..
        hexdigest(): Extracts the hash object and returns it as a readable, 64-character hexadecimal string."""

        # self.failed_attempt = failed_attempt
        # self.is_blocked = is_blocked

        # System state tracking attributes
        self.failed_attempt = 0
        self.is_blocked = False
        self.transaction_history: list[dict[str, Any]] = []

    def verify_pin(self, input_pin:str) -> bool:
        hashed_input_pin = hashlib.sha256(
            input_pin.encode("utf-8")
            ).hexdigest()
        
        return hashed_input_pin == self.hashed_pin


    def withdraw(self, amount:Decimal, input_pin: str) -> None: # this function should return Nothing

        if self.is_blocked:
            raise CardBlockError(
                self.account_id, 
                "Card is blocked due to security reasons.")
            

        if not self.verify_pin(input_pin):
            self.failed_attempt += 1

            if self.failed_attempt >= 3:

                self.is_blocked = True
                raise CardBlockError(
                    self.account_id, 
                    "Card is blocked due to security reasons.")
            
            remaining = 3 - self.failed_attempt
            raise InvalidPINError(remaining)
        
            #raise ValueError("PIN Incorrect") # raising a generic ValueError for a security credential mismatch is bad architecture
          
        self.failed_attempt = 0

        if amount < Decimal("200"):
            raise ValueError("Withdrawal amount must be at least ₹200.")
        
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)

        self.balance -= amount

        self.transaction_history.append({
            "type": "WITHDRAW",
            "amount": amount,
            "timestamp": datetime.now()
        })



