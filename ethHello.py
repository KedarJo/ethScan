#First attempt to connect to ethereum mainnet via Infura API
import json
import web3

from web3 import Web3, HTTPProvider
try:
   w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/dPotOByPqLlLN3nx14Pq"))
   print('w3 HTTPProvider call success')
except: print('w3 HTTPProvider call failure')

block = w3.eth.getBlock('latest')
uncles = block["uncles"]

#for element in block: print(element, block[element])
blockNumber = block["number"]
txnCount = w3.eth.getBlockTransactionCount(blockNumber)
print("Block:", blockNumber, " Number of transactions:", txnCount, "Miner: ", block["miner"])
print("Number of Uncles:", len(uncles))
minerReward = 3.0
uncleList = list()
for uncle in uncles:
    #print("uncle:", w3.toHex(uncle))
    uBlock = w3.eth.getBlock(uncle)
    minerReward += (uBlock["number"] + 8 - blockNumber) * 3 / 8
print("Miner Reward: ", minerReward)

txnHashes = block["transactions"]

# Extract cumulativeGasUsed from last transaction in the block
lastTxnHash = txnHashes[txnCount - 1]
cumTotal = 0.0
lastTxnR = w3.eth.getTransactionReceipt(lastTxnHash)
if lastTxnR != None:
    cumTotal = lastTxnR["cumulativeGasUsed"]
    gwei = w3.toWei(cumTotal, 'gwei')
    cumTotal = w3.fromWei(gwei, 'ether')
print("Total Gas Consumed", cumTotal)
minerReward += float(cumTotal)
print("Miner Reward: ", minerReward)

#for txnHash in txnHashes:
#    txn = w3.eth.getTransaction(txnHash)
#    wei = txn["value"]
#    value = w3.fromWei(wei, 'ether')
#    print(txn["from"], txn["to"], value)
