import hashlib
import json
from time import time

class Blockchain:
    def _init_(self):
        self.chain = []
        self.current_transactions = []
        self.create_block(proof=100, previous_hash='1')  # Genesis block

    def create_block(self, proof, previous_hash=None):
        """
        Create a new block in the blockchain

        :param proof: <int> The proof of work
        :param previous_hash: (Optional) <str> Hash of the previous block
        :return: <dict> New block
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined block

        :param sender: <str> Address of the sender
        :param recipient: <str> Address of the recipient
        :param amount: <int> Amount
        :return: <int> The index of the block that will hold this transaction
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a block

        :param block: <dict> Block
        :return: <str>
        """
        # We must make sure that the dictionary is ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns the last block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Simple proof of work algorithm:
        - Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous proof
        - p is the previous proof, and p' is the new proof

        :param last_proof: <int> Previous proof
        :return: <int> New proof
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous proof
        :param proof: <int> Current proof
        :return: <bool> True if correct, False if not.
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Example usage
if _name_ == "_main_":
    # Create a new Blockchain
    blockchain = Blockchain()

    # Add a sample transaction
    blockchain.new_transaction(sender="Alice", recipient="Bob", amount=1)

    # Mine a new block
    last_proof = blockchain.last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Reward the miner for finding the proof
    blockchain.new_transaction(sender="0", recipient="Miner", amount=1)

    # Add the new block to the chain
    previous_hash = blockchain.hash(blockchain.last_block)
    block = blockchain.create_block(proof, previous_hash)

    # Print the blockchain
    print(json.dumps(blockchain.chain, indent=4))