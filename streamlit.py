import streamlit as st
from blockchain import Blockchain

# Set up the Streamlit page
st.set_page_config(page_title="Blockchain App", layout="wide")
st.write("Developed by : Kavish Sureka")
st.title("⛓️ Blockchain Interaction App")
st.markdown("---")

# Initialize blockchain in session state if not already present
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = Blockchain()

blockchain = st.session_state.blockchain

st.header("⛏️ Mine a New Block")
# Input for new block data
data = st.text_input("Enter data for the new block")

# Button to mine a new block
if st.button("Mine New Block"):
    if data == "":
        st.error("Please enter data")
    else:
        with st.spinner("Mining in progress..."):
            block = blockchain.add_block(data)
        st.success("🎉 Congratulations, you just mined a block!")
        st.json(block)

st.markdown("---")
st.header("🔗 View Full Blockchain")

# Button to show the blockchain
if st.button("Show Blockchain"):
    chain_data = blockchain.chain
    chain_length = len(blockchain.chain)
    st.write(f"**Number of blocks:** {chain_length}")
    st.write("**Current Chain:**")
    # Display each block in an expander
    for i, block in enumerate(chain_data):
        with st.expander(f"Block {block['index']}", expanded=False):
            st.json(block)

st.markdown("---")
st.header("🛡️ Validate Blockchain")

# Button to check blockchain validity
if st.button("Check Validity"):
    is_chain_valid_status = blockchain.is_valid()
    if is_chain_valid_status:
        st.success("✅ All good. The Blockchain is valid.")
    else:
        st.error("❌ The Blockchain is not valid.")
    # Show validation for each block
    for index in range(len(blockchain.chain)):
        st.write(blockchain.validate_block(index))

st.markdown("---")
st.header("View/Edit Blockchain")
chain_data = blockchain.chain
chain_length = len(blockchain.chain)
# Allow editing if blockchain is not empty
if chain_length == 0:
    st.error("❌ Blockchain is currently empty.")
else:
    chain_data_new = st.data_editor(chain_data)
    blockchain.update_blockchain(chain_data_new)
    if chain_data_new != chain_data:
        st.rerun()

st.markdown("---")
# Sidebar instructions
st.sidebar.info(
    """
    **How to Use:**
    1.  **Mine New Block:** Click to add a new block to the chain.
    2.  **Show Blockchain:** Click to display all blocks currently in the chain.
    3.  **Check Validity:** Click to verify the integrity of the entire blockchain.
    4.  **View/Edit Blockchain:** Tamper any block field to test the blockchain validity.
    """
)

# Footer and links
st.markdown("Developed for KodeinKGP Blockchain Team Sophomore Selection Task Round",)
st.markdown(
    """
    <div style='text-align: center;'>
        <a href="https://github.com/kavishsureka" target="_blank" style="margin-right: 20px;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="40"/>
        </a>
        <a href="https://www.linkedin.com/in/kavish-sureka-bb2b4731a/" target="_blank">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="40"/>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
