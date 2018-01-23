# -*- coding: UTF-8 -*-

# Python core
import json
import hashlib as hasher
import datetime as date

# Flask
from flask import Flask, render_template
from flask import request

# Bitam Core
from src.core.blockchain.block import Block, blockchain

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, BTM ! Bit as African Money (1)"


@app.route('/btm', methods=['POST'])
def transaction():
    """ BTM transactions """
    # On each new POST request,
    # we extract the transaction data
    new_btm = request.get_json()
    # Then we add the transaction to our list
    this_nodes_transactions.append(new_btm)
    # Because the transaction was successfully
    # submitted, we log it to our console
    print "New transaction"
    print "FROM: {}".format(new_btm['from'].encode('ascii', 'replace'))
    print "TO: {}".format(new_btm['to'].encode('ascii', 'replace'))
    print "AMOUNT: {}\n".format(new_btm['amount'])
    # Then we let the client know it worked out
    return "Transaction submission successful\n"


@app.route('/blocks', methods=['GET'])
def get_blocks():
    """ Blocks """
    # Convert our blocks into dictionaries
    # so we can send them as json objects later
    for i in range(len(blockchain)):
        block = blockchain[i]
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        blockchain[i] = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    blockchain = json.dumps(blockchain)
    return blockchain


@app.route('/mine', methods=['GET'])
def mine():
    # Get the last proof of work
    last_block = blockchain[len(blockchain) - 1]
    last_proof = last_block.data['pow']
    # Find the proof of work for
    # the current block being mined
    # Note: The program will hang here until a new
    #       proof of work is found
    proof = proof_of_work(last_proof)
    # Once we find a valid proof of work,
    # we know we can mine a block so
    # we reward the miner by adding a transaction
    this_nodes_transactions.append(
        {"from": "network", "to": miner_address, "amount": 1}
    )
    # Now we can gather the data needed
    # to create the new block
    new_block_data = {
        "pow": proof,
        "transactions": list(this_nodes_transactions)
    }
    new_block_index = last_block.index + 1
    new_block_timestamp = this_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # Empty transaction list
    this_nodes_transactions[:] = []
    # Now create the
    # new block!
    mined_block = Block(
        new_block_index,
        new_block_timestamp,
        new_block_data,
        last_block_hash
    )
    blockchain.append(mined_block)
    # Let the client know we mined a block
    return json.dumps({
        "index": new_block_index,
        "timestamp": str(new_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + "\n"


# HTTP Errors

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def not_authorized(error):
    return render_template('403.html'), 403
