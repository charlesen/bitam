# Bitam Core
from src.core.blockchain.block import Block, blockchain

class Network(object):

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
