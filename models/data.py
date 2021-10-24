from hashlib import sha256
from collections import Counter
from models.transaction import Transaction
import json
import time
import string
import random


class Data:

    def __init__(self, previous_hash, transactions, nonce=0):
        self.previous_hash = previous_hash
        self.transactions = None
        self.nonce = nonce
        self.timestamp = time.time()
