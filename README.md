A fun ETH Scan with Web3
========================

This is a simple Python3 utility that connects with Infura remote node via API and downloads the specified number of latest blocks. This is meant to get a recent slice of ETH blockchain data.

1. Run ethScan first to access Eth and dump data to sqlite
```
$ python3 ethScan.py
```

---
2. Display D3 graph visualization
```
$ python3 ethGraph.py
```
This creates a ethGraph.json file required by D3 visualizer

3. Serve ethGraph.htm via local http server
```
$ python3 -m http.server
```
Sample:
![Sample Graph](https://github.com/KedarJo/ethScan/blob/master/ethGraph.png)

---
4. Miner distribution D3 pie chart
```
$ python3 ethMiner.py
```

5. Serve ethMiner.htm via local http server
```
$ python3 -m http.server
```

Sample
![Sample Miner distribution](https://github.com/KedarJo/ethScan/blob/master/ethMiner.png)

---
**Note:** The data produced is with just ~20mb download done sporadically over a period of time and by means is a representation of entire ETH history.

___
