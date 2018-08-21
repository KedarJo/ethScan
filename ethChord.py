#Read from table and dump transaction chord data to ethChord.js
import sqlite3

askLimit = input("Number of top nodes to analyze: ")
if len(askLimit) < 1: limit = 20
else: limit = int(askLimit)

conn = sqlite3.connect('ethScan.sqlite')
cur = conn.cursor()

cur.execute('''SELECT fromAddr, toAddr, sum(value) FROM Transactions
GROUP BY fromAddr, toAddr ORDER  BY sum(value) DESC LIMIT ?''', (limit,))

uniqueAddr = list()
toList = list()
ethChord = list()
rows = cur.fetchall()

for row in rows:
    if row[0] not in uniqueAddr: uniqueAddr.append(row[0])
    if row[1] not in uniqueAddr: uniqueAddr.append(row[1])

#print("Rows#", len(rows), "uniqueAddr#", len(uniqueAddr))

for item1 in uniqueAddr:
    fromAddr = item1
    toList = list()

    for item2 in uniqueAddr:
        toAddr = item2
        value = 0.0
        for row in rows:
            if row[0] == fromAddr and row[1] == toAddr: value = row[2]
        toList.append(value)
    ethChord.append(toList)

#for item in ethChord: print(item)
#Write to file

fhandle = open("ethChord.js", "w")
fhandle.write("ethChord = [")
for toList in ethChord:
    toStr = str()
    fhandle.write("\n[")
    for item in toList: toStr += (str(item)+", ")
    toStr = toStr[:-2]
    toStr += ("],")
    fhandle.write(toStr)
fhandle.write("\n]")
