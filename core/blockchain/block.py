# -*- coding: UTF-8 -*-

import hashlib as hasher
import datetime as date

# Docs
"""
Hashlib : https://docs.python.org/2/library/hashlib.html
"""


class Block:
    """  Define what a Bitam block is """

    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + str(self.timestamp) +
                   str(self.data) + str(self.previous_hash))
        return sha.hexdigest()


def create_genesis_block():
    """ Generate genesis block """
    # Quand l'afrique s'éveillera
    first_hash_ever = "88c298803a2731f7ddb8a0f88171c1dcd1e2e8543177fa5d2cc2df64fdb2c03f"
    data_init = {"pow": 0, "transactions": None}
    return Block(0, date.datetime.now(), data_init, first_hash_ever)


# For test only
# TODO : connect with more nodes
miner_address = "88c298803a2731f7ddb8a0f88171c1dcd1e2e8543177fa5d2cc2df64fdb2c03f"
# This node's blockchain copy
blockchain = []
blockchain.append(create_genesis_block())
# Store the transactions that
# this node has in a list
this_nodes_transactions = []
# Store the url data of every
# other node in the network
# so that we can communicate
# with them
peer_nodes = []
# A variable to deciding if we're mining or not
mining = True


def find_new_chains():
    # Get the blockchains of every
    # other node
    other_chains = []
    for node_url in peer_nodes:
        # Get their chains using a GET request
        block = requests.get(node_url + "/blocks").content
        # Convert the JSON object to a Python dictionary
        block = json.loads(block)
        # Add it to our list
        other_chains.append(block)
    return other_chains


def consensus():
    # Get the blocks from other nodes
    other_chains = find_new_chains()
    # If our chain isn't longest,
    # then we store the longest chain
    longest_chain = blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain = chain
    # If the longest chain isn't ours,
    # then we stop mining and set
    # our chain to the longest one
    blockchain = longest_chain


def proof_of_work(last_proof):
    """
    Create a variable that we will use to find
    our next proof of work
    """
    incrementor = last_proof + 1
    # Keep incrementing the incrementor until
    # it's equal to a number divisible by 9
    # and the proof of work of the previous
    # block in the chain
    while not (incrementor % 9 == 0 and incrementor % last_proof == 0):
        incrementor += 1
    # Once that number is found,
    # we can return it as a proof
    # of our work
    return incrementor
