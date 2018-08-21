# For visualization to work, start local server with python3 -m http.server
# Open http://localhost:8000 (check port on the commandline) to open html

import sqlite3

askLimit = input("Number of top nodes to analyze: ")
if len(askLimit) < 1: limit = 100
else: limit = int(askLimit)

conn = sqlite3.connect('ethScan.sqlite')
cur = conn.cursor()

cur.execute('''SELECT fromAddr, toAddr, sum(value) FROM Transactions
GROUP BY fromAddr, toAddr ORDER  BY sum(value) DESC LIMIT ?''', (limit,))

rows = cur.fetchall()
uniqueAddr = list()

for row in rows:
    if row[0] not in uniqueAddr: uniqueAddr.append(row[0])
    if row[1] not in uniqueAddr: uniqueAddr.append(row[1])

fhandle = open("ethGraph.json","w")
fhandle.write("{\n \"nodes\" : [")
ctr = 1
for item in uniqueAddr:
    fhandle.write("\n\t{\"id\": \"" + item + "\", \"group\": " + str(ctr) + "},")
    ctr += 1
fhandle.write("\n\t{}")
fhandle.write("\n],\n \"links\" : [")

for row in rows:
    value = int(row[2]/100)
    #value = row[2]
    fhandle.write("\n\t{\"source\": \"" + row[0] + "\", \"target\": \"" + row[1] + "\", \"value\": " + str(value) + "},")
fhandle.write("\n\t{}")
fhandle.write("\n\t] \n}")
