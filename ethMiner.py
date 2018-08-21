import sqlite3

askLimit = input("Number of top miners to analyze: ")
if len(askLimit) < 1: limit = 10
else: limit = int(askLimit)

conn = sqlite3.connect('ethScan.sqlite')
cur = conn.cursor()

cur.execute('''SELECT miner, sum(minerReward) FROM Blocks GROUP BY miner
ORDER BY sum(minerReward) DESC LIMIT ?''', (limit,))

rows = cur.fetchall()
fHandle = open("ethMiner.js", "w")
fHandle.write("ethMiner = [")
minerReward = dict()
totalR = 0.0
for row in rows:
    totalR += row[1]
    minerReward[row[0]] = row[1]

for miner in minerReward:
    value = int(minerReward[miner] * 100 / totalR)
    fHandle.write("\n\t{\"name\": \"" + miner + "\", \"value\":" + str(value) + "},")

fHandle.write("\n]")
