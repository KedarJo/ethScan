import json
import web3
import sqlite3

from web3 import Web3, HTTPProvider, IPCProvider
try:
    #w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/dPotOByPqLlLN3nx14Pq"))
    #w3 = Web3(Web3.HTTPProvider("http://localhost:8545"))
    #print('w3 HTTPProvider success')
    w3 = Web3(Web3.IPCProvider('/Volumes/MyPassportForMac/Ethereum/geth.ipc'))
    print('w3 IPCProvider success')
except:
    print('w3 HTTPProvider failure. Shutting down...')
    quit()

def dumpTxnData(txnHash, blockNumber):
    txn = w3.eth.getTransaction(txnHash)
    wei = txn["value"]
    value = w3.fromWei(wei, 'ether')
    txnHashStr = str(txnHash)
    fromAddr = str(txn["from"])
    toAddr = str(txn["to"])
    fvalue = float(value)
    #print ("Inserting", txnHashStr, blockNumber, fromAddr, toAddr, fvalue)
    cur.execute('''INSERT OR IGNORE INTO Transactions (txnID, blockNumber, fromAddr, toAddr, value)
    VALUES (?, ?, ?, ?, ?)''', (txnHashStr, blockNumber, fromAddr, toAddr, fvalue))
    #conn.commit()
    #print(txn["from"], txn["to"], value)

def dumpBlockData(blockNumber):
    #If block already dumped, skip processing
    cur.execute("SELECT * FROM Blocks WHERE blockNumber= ?", (blockNumber, ))
    try:
        data = cur.fetchone()[0]
        print("Block already processed, skipping...", data)
    except:
        block = w3.eth.getBlock(blockNumber)
        print("Working on block: ", block["number"])
        uncles = block["uncles"]
        #print("Number of Uncles:", len(uncles))
        minerReward = 3.0
        for uncle in uncles:
            uBlock = w3.eth.getBlock(uncle)
            minerReward += (uBlock["number"] + 8 - blockNumber) * 3 / 8
            #print("Miner Reward: ", minerReward)
        txnCount = w3.eth.getBlockTransactionCount(blockNumber)
        print("transaction Count", txnCount)
        if txnCount == None:
            print("Empty block, no transactions processed", blockNumber)
        else:
            txnHashes = block["transactions"]
            #Add Gas Fees to minerReward
            lastTxnHash = txnHashes[txnCount - 1]
            cumTotal = 0.0
            lastTxnR = w3.eth.getTransactionReceipt(lastTxnHash)
            if lastTxnR != None:
                cumTotal = lastTxnR["cumulativeGasUsed"]
                gwei = w3.toWei(cumTotal, 'gwei')
                cumTotal = w3.fromWei(gwei, 'ether')
                minerReward += float(cumTotal)
                #print("Miner Reward: ", minerReward)
                miner = str(block["miner"])

            for txnHash in txnHashes: dumpTxnData(txnHash, blockNumber)

        cur.execute('''INSERT OR IGNORE INTO Blocks (blockNumber, miner, minerReward)
        VALUES (?, ?, ?)''', (blockNumber, miner, minerReward))
        conn.commit()


# Main Starts here ***

conn = sqlite3.connect('ethScan.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Blocks (blockNumber INTEGER UNIQUE, miner TEXT, minerReward REAL)''')

cur.execute('''
CREATE TABLE IF NOT EXISTS Transactions (txnID TEXT UNIQUE, blockNumber INTEGER, fromAddr TEXT, toAddr TEXT, value REAL)''')

blocksTotal = input("Number of latest blocks to explore: ")
if len(blocksTotal) < 1:
    print("No input received, default 10 considered")
    blocksToExplore = 10
else: blocksToExplore = int(blocksTotal)

try:
    block = w3.eth.getBlock('latest')
    print(block)
    blockNumber = block["number"]
except:
    print(w3.eth.getBlock('latest'))
    print("Something went wrong when retrieving latest block. Try again")
    quit()

ctr = 0
while ctr < blocksToExplore:
    dumpBlockData(blockNumber)
    blockNumber -= 1
    ctr += 1

cur.close()

#SELECT miner, sum(minerReward) FROM Blocks GROUP BY miner
#ORDER BY sum(minerReward) DESC

#SELECT fromAddr, toAddr, sum(value) FROM Transactions
#GROUP BY fromAddr, toAddr ORDER  BY sum(value) DESC;
