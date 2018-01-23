# -*- coding: UTF-8 -*-
import os
import hashlib as hasher
import datetime as date

# Docs
"""
Hashlib : https://docs.python.org/2/library/hashlib.html

https://bigishdata.com/2017/10/17/write-your-own-blockchain-part-1-creating-storing-syncing-displaying-mining-and-proving-work/

"""

# Data dir
BTM_DATA_DIR = 'btm_data'

# Nonce
NUM_ZEROS = 7


class Block(object):
    """  Define what a Bitam block is """

    def __init__(self, block_data):
        """
        Init Block class

        Args:
            index (int)         : Block index
            timestamp (datetime): current time
            data (dict)         : Block data {'trx_pow': proof of work,
                                              'trx_meta': Data,
                                              'trx_smc': Smart contract
                                              'trx_notes': notes}
            previous_hash (str) : The previous block hash
            hash (str)          : current block hash
        """
        for k, v in block_data.items():
            setattr(self, k, v)
        # in creating the first block, needs to be removed in future
        if not hasattr(self, 'hash'):
            self.hash = self.hash_block()

        self.nonce = 'None'

        # Init block
        self.init_block()

    def __dict__(self):
        block_data = {}
        block_data['index'] = str(self.index)
        block_data['timestamp'] = str(self.timestamp)
        block_data['data'] = str(self.data)
        block_data['previous_hash'] = str(self.previous_hash)
        block_data['hash'] = str(self.hash)
        return block_data

    def __str__(self):
        return "Block<previous_hash: %s,hash: %s>" % (self.previous_hash, self.hash)

    def __eq__(self, other):
        return (self.index == other.index and
                self.timestamp == other.timestamp and
                self.prev_hash == other.prev_hash and
                self.hash == other.hash and
                self.data == other.data and
                self.nonce == other.nonce)

    def __ne__(self, other):
        return not self.__eq__(other)

    def create_genesis_block(self):
        """ Generate genesis block """
        block_data = {'index': 0,
                      'timestamp': date.datetime.now(),
                      'previous_hash': None,
                      'hash': '88c298803a2731f7ddb8a0f88171c1dcd1e2e8543177fa5d2cc2df64fdb2c03f',
                      'data': {'trx_pow': 0,
                               'trx_meta': None,
                               'trx_smc': None,  # Smart contract
                               'trx_notes': "Quand l'afrique s'éveillera"}
                     }
        block = Block(block_data)
        return block

    def init_block(self):
        """ Init blockchain """
        # check if chaindata folder exists.
        if not os.path.exists(BTM_DATA_DIR):
            # make chaindata dir
            os.mkdir(BTM_DATA_DIR)
            # check if dir is empty from just creation, or empty before
        if os.listdir(BTM_DATA_DIR) == []:
            # create first block
            first_block = self.create_genesis_block()
            self.save_block(first_block)

    def hash_block(self):
        """ Hash a block """
        return self.hash_data(str(self.index) + str(self.timestamp) +
                              str(self.data) + str(self.previous_hash))

    def hash_data(self, data):
        """ Hash any data """
        sha = hasher.sha256()
        sha.update(str(data))
        return sha.hexdigest()

    def is_block_valid(self):
        """
          Current validity is only that the hash begins with at least NUM_ZEROS
        """
        # self.update_self_hash()
        if str(self.hash[0:NUM_ZEROS]) == '0' * NUM_ZEROS:
          return True
        else:
          return False

    def save_block(self, block):
        """ Save a block """
        filename = '%s/block_%s.json' % (BTM_DATA_DIR, block.index)
        with open(filename, 'w') as block_file:
            print block.__dict__()
            json.dump(block.__dict__(), block_file

    def sync_blockhain():
        """ Synchronize blocks """
        # We're assuming that the folder and at least initial block exists
        node_blocks=[]

        # Init block first
        self.init_block()

        if os.path.exists(BTM_DATA_DIR):
            for filename in os.listdir(BTM_DATA_DIR):
                if filename.endswith('.json'):
                    filepath='%s/%s' % (BTM_DATA_DIR, filename)
                    with open(filepath, 'r') as block_file:
                        block_info=json.load(block_file)
                        # since we can init a Block object with just a dict
                        block_object=Block(block_info)
                        node_blocks.append(block_object)
        return node_blocks


    def mine(last_block):
        """ Mine block """
        index=int(last_block.index) + 1
        timestamp=date.datetime.now()
        data="I block #%s" % (int(last_block.index) + 1)
        previous_hash=last_block.hash
        block_hash=self.hash_data(str(index) + str(timestamp) +
                              str(data) + str(previous_hash))
        while str(block_hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
            nonce += 1
            block_hash=self.hash_data(str(index) + str(timestamp) +
                                  str(data) + str(previous_hash) +
                                  str(nonce))
        block_data={}
        block_data['index']=int(last_block.index) + 1
        block_data['timestamp']=date.datetime.now()
        block_data['data']={'trx_pow': nonce,
                            'trx_meta': None,
                            'trx_smc': None,  # Smart contract
                            'trx_notes': "New block at #%s index" % last_block.index}
        block_data['previous_hash']=last_block.hash
        block_data['hash']=block_hash
        return Block(block_data)

    @staticmethod
    def get_blockchain(self):
        """ Get the blockchain """
        node_blocks=self.sync_blockhain()  # regrab the nodes if they've changed
        # Convert our blocks into dictionaries
        # so we can send them as json objects later
        l_blocks=[]
        for block in node_blocks:
            l_blocks.append(block.__dict__())
        json_blocks=json.dumps(l_blocks)
        return json_blocks


blockchain=Block.get_blockchain()


def find_new_chains():
    # Get the blockchains of every
    # other node
    other_chains=[]
    for node_url in peer_nodes:
            # Get their chains using a GET request
        block=requests.get(node_url + "/blocks").content
        # Convert the JSON object to a Python dictionary
        block=json.loads(block)
        # Add it to our list
        other_chains.append(block)
    return other_chains


def consensus():
    # Get the blocks from other nodes
    other_chains=find_new_chains()
    # If our chain isn't longest,
    # then we store the longest chain
    longest_chain=blockchain
    for chain in other_chains:
        if len(longest_chain) < len(chain):
            longest_chain=chain
    # If the longest chain isn't ours,
    # then we stop mining and set
    # our chain to the longest one
    blockchain=longest_chain


def proof_of_work(last_proof):
    """
    Create a variable that we will use to find
    our next proof of work
    """
    incrementor=last_proof + 1
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
