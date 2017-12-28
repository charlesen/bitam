# -*- coding: UTF-8 -*-

# Core Python
import hashlib
import time

# Block class. Used to create blocks. Blocks are then added to the blockchain.

class Block:

    def __init__(self, index, difficulty, nonce, previousHash, timestamp, data, currentHash):
        self.index = index
        self.difficulty = difficulty
        self.nonce = nonce
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.currentHash = currentHash

# Used to create the genesis block and verify following blocks.


def getGenesisBlock():
    return Block(0, 0, 0, '0', '1496518102.896031', "My very first block :)", '0q23nfa0se8fhPH234hnjldapjfasdfansdf23')

# Creates the 'chain' with the genesis block.
blockchain = [getGenesisBlock()]

# Calculates the hash of the block contents.


def calculateHash(index, difficulty, nonce, previousHash, timestamp, data):
    value = str(index) + str(difficulty) + str(nonce) + \
        str(previousHash) + str(timestamp) + str(data)
    sha = hashlib.sha256(value.encode('utf-8'))
    return str(sha.hexdigest())


def mineBlock(index, difficulty, nonce, previousHash, timestamp, data):
    print("Mining new block...")

    difficultyString = "" + ("0" * difficulty)

    while (True):
        value = str(index) + str(difficulty) + str(nonce) + \
            str(previousHash) + str(timestamp) + str(data)

        sha = hashlib.sha256(value.encode('utf-8'))

        checkStr = str(sha.hexdigest())[:difficulty]

        if (checkStr == difficultyString) or (difficulty == 0):
            print("Found hash: " + str(sha.hexdigest()))
            return Block(index, difficulty, nonce, previousHash, timestamp, data, str(sha.hexdigest()))
        else:
            nonce += 1
        str(sha.hexdigest())


def calculateHashForBlock(block):
    return calculateHash(block.index, block.difficulty, block.nonce, block.previousHash, block.timestamp, block.data)


def getLatestBlock():
    return blockchain[len(blockchain) - 1]


def generateNextBlock(blockData):
    previousBlock = getLatestBlock()
    nextIndex = previousBlock.index + 1
    nextDifficulty = previousBlock.difficulty
    nextTimestamp = str(time.time())

    blockTime = 0.5

    if (abs(float(previousBlock.timestamp) - float(nextTimestamp)) < blockTime):
        print("UPDATING DIFFICULTY")
        nextDifficulty += 1

    # if (float(previousBlock.timestamp) - float(nextTimestamp)) < 1.0:
    #    print("UPDATING DIFFICULTY")
    #    nextDifficulty += 1

    nextNonce = 0

    newBlock = mineBlock(nextIndex, nextDifficulty, nextNonce,
                         previousBlock.currentHash, nextTimestamp, blockData)

    return newBlock


def isSameBlock(block1, block2):
    if block1.index != block2.index:
        return False
    if block1.difficulty != block2.difficulty:
        return False
    if block1.nonce != block2.nonce:
        return False
    elif block1.previousHash != block2.previousHash:
        return False
    elif block1.timestamp != block2.timestamp:
        return False
    elif block1.data != block2.data:
        return False
    elif block1.currentHash != block2.currentHash:
        return False
    return True

# Add in check for time created


def isValidNewBlock(newBlock, previousBlock):
    if previousBlock.index + 1 != newBlock.index:
        print('Indices Do Not Match Up')
        return False
    elif previousBlock.currentHash != newBlock.previousHash:
        print("Previous hash does not match")
        return False
    elif calculateHashForBlock(newBlock) != newBlock.currentHash:
        print("Hash is invalid")
        return False
    return True

# Validates chain. Checks through each block in the chain to make sure
# they are all valid.


def isValidChain(bcToValidate):
    if not isSameBlock(bcToValidate[0], getGenesisBlock()):
        print('Genesis Block Incorrect')
        return False

    tempBlocks = [bcToValidate[0]]
    for i in range(1, len(bcToValidate)):
        if isValidNewBlock(bcToValidate[i], tempBlocks[i - 1]):
            tempBlocks.append(bcToValidate[i])
        else:
            return False
    return True


def main():
    while (isValidChain(blockchain)):
        print("--------------")
        print("Latest Bock")
        print("--------------")
        print("Block Height: ", getLatestBlock().index)
        print("Difficulty: ", getLatestBlock().difficulty)
        print("Nonce: ", getLatestBlock().nonce)
        print("Previous Hash: ", getLatestBlock().previousHash)
        print("Timestamp: ", getLatestBlock().timestamp)
        print("Data: ", getLatestBlock().data)
        print("Current Hash: ", getLatestBlock().currentHash)
        print("--------------")
        blockchain.append(generateNextBlock("Next Block In The Chain!!!"))

        # time.sleep(1)

if __name__ == "__main__":
    main()
