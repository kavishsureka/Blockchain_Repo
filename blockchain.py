import hashlib
import datetime
import json

# Initial previous hash for the first block
previous_hash = '000'

class Blockchain:
    def __init__(self):
        self.chain = []  # List to store all blocks

    def add_block(self, data):
        global previous_hash
        # Create a new block with data and previous hash
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'data': data,
            'previous_hash': previous_hash
        }
        # Find a valid nonce for proof of work
        block['nonce'] = self.proof_of_work(block)
        # Calculate the hash for the block
        block['hash'] = self.hash(block)
        previous_hash = block['hash']  # Update previous hash
        self.chain.append(block)  # Add block to chain
        return block

    def hash(self, block):
        # Create a copy of the block without the hash field
        block_copy = {key: value for key, value in block.items() if key != 'hash'}
        # Convert block dictionary to string and encode
        encoded_block = json.dumps(block_copy, sort_keys=True).encode()
        # Return SHA-256 hash
        return hashlib.sha256(encoded_block).hexdigest()

    def proof_of_work(self, block):
        nonce = 1
        nonce_found = False
        # Increment nonce values until hash starts with '00'
        while nonce_found is False :
            block['nonce'] = nonce
            hash = self.hash(block)
            if hash[:2] == '00':
                nonce_found = True
            else:
                nonce += 1
        return nonce

    def is_valid(self):
        block_index = 0
        # Check each block in the chain
        while block_index < len(self.chain):
            current_block = self.chain[block_index]
            if block_index != 0:
                previous_block = self.chain[block_index - 1]
                # Check if previous hash matches
                if previous_block['hash'] != current_block['previous_hash']:
                    return False
            # Check if hash is correct and starts with '00'
            if current_block['hash'] != self.hash(current_block) or current_block['hash'][:2] != '00':
                return False
            block_index += 1
        return True

    def validate_block(self, i):
        # Check if block hash starts with '00'
        if self.chain[i]['hash'][:2] != '00':
            message = f"❌ Block {i+1} hash does not start with two leading zeroes"
            return message
        # Check if block hash matches the calculated hash
        if self.chain[i]['hash'] != self.hash(self.chain[i]):
            message = f"❌ Block {i+1} hash does not match with its expected hash"
            return message
        # For all blocks except the first, check previous hash
        if i != 0:
            if self.chain[i]['previous_hash'] != self.chain[i-1]['hash']:
                message = f"❌ Block {i+1} previous hash does not match with Block {i} hash"
                return message
            else:
                message = f"✅ Block {i+1} hash is valid as well as Block {i+1} previous hash matches with Block {i} hash"
                return message
        message = f"✅ Block {i+1} hash is valid"
        return message

    def update_blockchain(self, chain):
        new_chain = []
        # Recalculate hash for each block and update chain
        for block in chain:
            block['hash'] = self.hash(block)
            new_chain.append(block)
        self.chain = new_chain
