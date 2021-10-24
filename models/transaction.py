from hashlib import sha256
from collections import Counter
import json
import time
import string
import random

class Transaction:

    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def __repr__(self):
        return self.__dict__

    def to_string(self):
        return self.__dict__

    @classmethod
    def generate_transaction(cls, size=6, chars=string.ascii_uppercase + string.digits):
        return cls(*("".join(random.choice(chars) for _ in range(size)),)*3)