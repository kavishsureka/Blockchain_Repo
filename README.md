#  Simple Blockchain in Python
This project implements a basic blockchain from scratch using Python. It demonstrates the fundamental components of blockchain technology, including block creation, hashing, proof-of-work, and chain validation.

## Deployment Link

**https://kavishblockchain.streamlit.app/**

## Steps to Install:
```
 uv pip install streamlit
```
 
##  Block Structure

Each block in this blockchain contains the following fields:

```python
block = {
    'index':           # Position of the block in the chain
    'timestamp':       # Date and time when the block was created
    'data':            # The actual data stored (can be any string)
    'previous_hash':   # Hash of the previous block 
    'nonce':           # Proof-of-work value 
    'hash':            # Current block’s SHA-256 hash
}
```
## Validation Logic
### is_valid() function
This checks the entire blockchain to ensure:
<br>
* Each Block's hash starts with "00" (required by Proof-Of-Work).
* Each Block's hash is correct as calculated based on its contents.
* Each block’s previous_hash matches the actual hash of the previous block.

## Proof-of-Work Approach
A basic proof-of-work algorithm is implemented which works as follows:
<br>
* A block’s hash must start with "00" to be considered valid.
* The proof_of_work() function keeps incrementing the value of nonce (starting from one) until the value of hash satisfies this condition.






