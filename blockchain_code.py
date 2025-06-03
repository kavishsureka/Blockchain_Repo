import hashlib
import datetime
import json

previous_hash='000'

class Blockchain:
    
    def __init__(self):
        self.chain=[]

    def add_block(self,data):    
        global previous_hash
        
        block ={'index': len(self.chain)+1,
                'timestamp':str(datetime.datetime.now()),
                'data':data,
                'previous_hash':previous_hash}
        
        block['nonce']=self.proof_of_work(block)
        block['hash']=self.hash(block)
        previous_hash=block['hash']
        self.chain.append(block)
        return block
        
    def hash(self,block):
        block_copy={key:value for key,value in block.items()if key!='hash'}
        encoded_block=json.dumps(block_copy,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def proof_of_work(self,block):
        nonce=1
        nonce_found=False
        while nonce_found is False:
            block['nonce']=nonce
            hash=self.hash(block)
            if hash[:2]=='00':
                nonce_found=True
            else:
                nonce +=1
        return nonce        

    def is_valid(self):
        block_index=0
        while block_index<len(self.chain):
            current_block=self.chain[block_index]
            if block_index!=0:
                previous_block=self.chain[block_index-1]
                if previous_block['hash']!=current_block['previous_hash']:
                    return False
            if current_block['hash']!=self.hash(current_block) or current_block['hash'][:2]!='00':
                return False
            block_index+=1
        return True  
    
    def validate_block(self,i):
        if self.chain[i]['hash'][:2]!='00':
            message = f"❌ Block {i+1} hash does not start with two leading zeroes"
            return message
        if self.chain[i]['hash']!=self.hash(self.chain[i]):
            message=f"❌ Block {i+1} hash does not match with its expected hash"
            return message
        if i!=0:
            if self.chain[i]['previous_hash']!=self.chain[i-1]['hash']:
                message=f"❌ Block {i+1} previous hash does not match with Block {i} hash"
                return message
            else :
                 message= f"✅ Block {i+1} hash is valid as well as Block {i+1} previous hash matches with Block {i} hash"
                 return message

        message= f"✅ Block {i+1} hash is valid"
        return message

    def update_blockchain(self,chain):
        new_chain=[]

        for block in chain:
            block['hash']=self.hash(block)
            new_chain.append(block)
        self.chain =new_chain
