from flask import Flask, request, jsonify
from models.block import Blockchain
from models.transaction import Transaction

import json
import time

app =  Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True

TRANSACTIONS = [
    Transaction(sender="Ollie", recipient="Madzi", amount=5.99)
]

@app.route('/chain', methods=['GET'])
@app.route('/', methods=['GET'])
def get_chain():
    chain = [
        block.to_json() for block in blockchain
    ]
    return jsonify(
        length=blockchain.length,
        chain=chain
    )

blockchain = Blockchain()

for transaction in TRANSACTIONS:
    blockchain.add_new_transaction(transaction)
    new_block = blockchain.mine()

app.run(debug=True, port=5055)
