import hashlib
import datetime
import json
import streamlit as st

previous_hash='000'

class Blockchain():
    

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
                message=f"❌ Block {i+1} previous hash does not match with Block{i} hash"
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

    
st.set_page_config(page_title="Blockchain App",layout="wide")
st.title("⛓️ Blockchain Interaction App")
st.markdown("---")

if 'blockchain' not in st.session_state:
    st.session_state.blockchain=Blockchain()

blockchain = st.session_state.blockchain

st.header("⛏️ Mine a New Block")
data = st.text_input("Enter data for the new block")


if st.button("Mine New Block"):
    if data=="":
        st.error("Please enter data")

    else:
        with st.spinner("Mining in progress..."):
            block=blockchain.add_block(data)

        st.success("🎉 Congratulations, you just mined a block!")
        st.json(block)
    

st.markdown("---")
st.header("🔗 View Full Blockchain")

if st.button("Show Blockchain"):
    chain_data = blockchain.chain
    chain_length = len(blockchain.chain)
    st.write(f"**Number of blocks:** {chain_length}")
    st.write("**Current Chain:**")
    for i, block in enumerate(chain_data):
        with st.expander(f"Block {block['index']}", expanded=False):
          st.json(block)
         
        

st.markdown("---")
st.header("🛡️ Validate Blockchain")

if st.button("Check Validity"):
    is_chain_valid_status = blockchain.is_valid()
    if is_chain_valid_status:
        st.success("✅ All good. The Blockchain is valid.")
    else:
        st.error("❌ The Blockchain is not valid.")

    for index in range (len(blockchain.chain)):
        st.write(blockchain.validate_block(index))

st.markdown("---")
st.header("View/Edit Blockchain")
chain_data = blockchain.chain
chain_length = len(blockchain.chain)
if chain_length == 0: 
    st.error("❌ Blockchain is currently empty.")
else: 
    chain_data_new = st.data_editor(chain_data)
    blockchain.update_blockchain(chain_data_new)
    if chain_data_new!=chain_data:
        st.rerun()




st.markdown("---")
st.sidebar.info(
    """
    **How to Use:**
    1.  **Mine New Block:** Click to add a new block to the chain.
    2.  **Show Blockchain:** Click to display all blocks currently in the chain.
    3.  **Check Validity:** Click to verify the integrity of the entire blockchain.
    """
)
