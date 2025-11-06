# blockchain1.py
# Original code idea based on: Dr. Ernesto Lee – "Building Your Own Blockchain in Python"
# https://drlee.io/building-your-own-blockchain-in-python-a-step-by-step-guide-ec10ea6c976d
# Modified by [wald328]


import hashlib  # We'll use Python's built-in hashlib library
import json
import time

class Transaction:
    def __init__(self, from_addr: str, to_addr: str, amount: float):
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.amount = amount
    def __repr__(self):
        return f"Transaction(from={self.from_addr}, to={self.to_addr}, amount={self.amount})"
    

class Block:
    def __init__(self,index, timestamp, transactions, prior_hash=''):
        self.index = index # number of block
        self.timestamp = timestamp  # The time when the block was created
        self.transactions = transactions  # The transactions within this block
        self.prior_hash = prior_hash  # The hash of the previous block in the chain
        self.nonce = 0  # Initialize nonce to zero before creating the hash
        self.hash = None

    
    def create_hash(self):
        # Calculate the hash for the block
        block_string = (str(self.index)+str(self.prior_hash) + str(self.timestamp) + 
                        str(self.transactions) + str(self.nonce)).encode()
        # Return the hash of this string using SHA-256
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # Mine the block until the hash starts with a number of zeros equal to difficulty
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.create_hash()
        print(f"Block mined! Index: {self.index}, Nonce: {self.nonce}, Hash: {self.hash}")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Initialize the chain with the genesis block
        self.difficulty = 3  # Set difficulty level
        self.pending_transactions = []  # Store transactions that are yet to be mined
        self.mining_reward = 10  # Set mining reward
    
    def create_genesis_block(self):
        # Create the first block in the blockchain with fixed parameters
        genesisblock = Block(0,time.time(), [], "0")
        genesisblock.hash = genesisblock.create_hash()
        return genesisblock


    def get_last_block(self):
        return self.chain[-1]  # the last Element in the list self.chain

    def mine_pending_transactions(self, mining_reward_address):
        # Create a new block with all pending transactions
        block = Block(self.get_last_block().index +1,time.time(), self.pending_transactions, self.get_last_block().hash)
        block.hash = block.create_hash()#make hash
        
        block.mine_block(self.difficulty)

        # Add the newly mined block to the chain
        self.chain.append(block)

        # Reset the list of pending transactions and add a transaction to reward the miner
        self.pending_transactions = [Transaction(None, mining_reward_address, self.mining_reward)]

    def create_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        

    def get_balance_of_address(self, address):
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.from_addr == address:
                    balance -= transaction.amount
                if transaction.to_addr == address:
                    balance += transaction.amount

        return balance



    def is_bc_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check if the hash of the current block is correct
            if current_block.hash != current_block.create_hash():
                return False
            
            # Check if the current block points to the correct previous block
            if current_block.prior_hash != previous_block.hash:
                return False
            #Check Nonce difficulty
            if not current_block.hash.startswith('0' * self.difficulty):
                return False

        
        return True





def main():
    # Create a new instance of the Blockchain
    test_coin = Blockchain()
    
    # Create some transactions
    test_coin.create_transaction(Transaction('address1', 'address2', 75))
    test_coin.create_transaction(Transaction('address2', 'address1', 25))
    
    
    print("Starting mining process...")
    test_coin.mine_pending_transactions('miner-address')
    
    # Check the balance of the miner
    print(f"Miner balance: {test_coin.get_balance_of_address('miner-address')}")
    
    #Mine again to receive the reward
    print("\n Mining again to receive the reward...")
    test_coin.mine_pending_transactions('miner-address')
    
    # Check the balance of the miner
    print(f"Miner balance: {test_coin.get_balance_of_address('miner-address')}")
    print("")

    # Create some transactions
    test_coin.create_transaction(Transaction('address1', 'address2', 200))

    #Mine again to receive the reward
    print("\n Mining again to receive the reward...")
    test_coin.mine_pending_transactions('miner-address')
    
    # Check the balance of the miner
    print(f"Miner balance: {test_coin.get_balance_of_address('miner-address')}")
    print("")

    
    #print  whole chain 
    print(json.dumps(test_coin.chain, default=lambda o: o.__dict__, indent=4))
    
    #Is chain valid?
    print('Is Chain Valid?', test_coin.is_bc_valid())



if __name__ == "__main__":
    main()


