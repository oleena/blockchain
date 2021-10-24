from hashlib import sha256
from collections import Counter
from models.transaction import Transaction
from models.data import Data
import json
import time
import string
import random
import datetime


class Block:

    counter = 1

    def __init__(self, prev_hash: str, transactions: [Transaction], index: int=None, nonce: int=0):
        self.index = index
        self.prev_hash = prev_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = None
        self.next = None

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4)

    @property
    def timestamp(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def to_json(self):
        return {
            "index": self.index,
            "hash": self.hash,
            "prev_hash": self.prev_hash,
            "transactions": self.transactions,
            "timestamp": self.timestamp,
        }

    def generate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "prev_hash": self.prev_hash,
            "transaction": self.transactions,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()


class Blockchain:

    difficulty = 2

    def __init__(self):
        self.pending_transactions = [] # type: List[Transaction]
        # Genesic Block
        genesis = Block(index=0, prev_hash="0", transactions=[], nonce=0)
        genesis.hash = genesis.generate_hash()
        self.genesis = genesis

    def __repr__(self):
        block = self.genesis
        blocks = []
        while block is not None:
            blocks.append(block.hash)
            block = block.next
        return json.dumps(blocks, indent=4)
        # return " -> " .join(blocks)

    def __iter__(self):
        block = self.genesis
        while block is not None:
            yield block
            block = block.next

    @property
    def length(self):
        length = 0
        block = self.genesis
        while block is not None:
            length =+ 1
            block = block.next
        return length

    @property
    def last_block(self):
        if self.genesis is None:
            self.genesis = block
            return
        for block in self:
            pass
        return block

    def add_block(self, block: Block, proof: str):
        if block.prev_hash != self.last_block.hash:
            return False
        if not self.validate_proof(block, proof):
            return False

        block.hash = proof
        block.index = self.last_block.index + 1
        self.validate_proof(block, proof)
        self._add(block)

    def _add(self, block: Block):
        if self.genesis is None:
            self.genesis = block
            return
        for _block in self:
            pass
        _block.next = block


    def new_block(self, transactions):
        return Block(
            transactions=transactions,
            prev_hash=self.last_block.hash,
            nonce=0
        )

    def proof_of_work(self, block: Block):
        """
        The proof-of-work system requires scanning for a value that starts with a certain number of zero bits
        when hashed. This value is known as a nonce value. The number of leading zero bits is known as the difficulty.
        :param block: Block
        :return:
        """
        block.nonce = 0
        computed_hash = block.generate_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.generate_hash()
        return computed_hash



    def validate_proof(self, block, proof):
        block_hash = block.generate_hash()
        return (proof.startswith('0' * Blockchain.difficulty) and
                proof == block_hash)


    def mine(self):
        # New block with transactions to ADD to blockchain
        new_block = self.new_block(self.pending_transactions)
        # New generated hash (proof) of block - yet to confirmed
        proof = self.proof_of_work(new_block)

        self.add_block(new_block, proof)
        # print(json.dumps(new_block.__dict__, indent=4))
        self.pending_transactions = []
        return new_block

    def add_new_transaction(self, transaction: Transaction):
        self.pending_transactions.append(transaction.to_string())