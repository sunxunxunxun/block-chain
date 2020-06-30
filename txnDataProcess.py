import os, json
from io import open

BYTE_PATH = './deploycode/'
TXNOUT_PATH = './contractTxn/'
EXTXN_PATH = './contractsExTxs/'
INXN_PATH = './contractsInTxs/'
txnInfo_file = './txInfo'
getted_txn_file = './gettedTxn'

txns = []
exTxn, inTxn = 0, 0
getted_txn = {}

if not os.path.exists(BYTE_PATH):
    os.system('mkdir ' + BYTE_PATH)
if not os.path.exists(TXNOUT_PATH):
    os.system('mkdir ' + TXNOUT_PATH)
if not os.path.exists(getted_txn_file):
    fp = open(getted_txn_file, 'w')
    fp.close()

#记录txnInfo文件中已经处理过的合约交易
with open(getted_txn_file, 'r', encoding = 'utf-8') as rf:
    for line in rf.readlines():
        getted_txn[line.strip()] = 1

with open(txnInfo_file, 'r', encoding = 'utf-8') as rf:
    for line in rf.readlines():
        line = line.strip('\n')
        txns.append(line)

for txn in txns:
    if txn.split('#')[0] in getted_txn:
        continue
    txn = txn.split('#')
    contract, exTxn, inTxn = txn[0], int(txn[1]), int(txn[2])
    print(contract)
    if not exTxn:
        print("with no external transaction")
        continue
    txn_output = open(TXNOUT_PATH + contract, 'a')

    #判断第一行交易的input是否是contract的deploy code
    with open(EXTXN_PATH + contract, 'r', encoding = 'utf-8') as rf:
        txn_contents = eval(rf.readline().strip())  #list
    if txn_contents[0]['from'] != contract and txn_contents[0]['to']=='': 
        with open(BYTE_PATH + contract, 'w', encoding = 'utf-8') as wf:
            wf.write(txn_contents[0]['input'])
        del txn_contents[0]
    #提取一个contract的全部外部交易和内部交易存到以合约名命名的文件中，位于TXNOUT_PATH
    #内部交易的input有问题，所以先没存内部交易信息
    for info in txn_contents:
        if info['txreceipt_status'] == '0':
            continue
        txn_output.write(info['hash'] + '#' + info['from'] + '#' + info['to'] + '#' + info['value'] + '#' + info['input'] + '\n')
    txn_output.close()

    with open(getted_txn_file, 'a', encoding = 'utf-8') as af:
        af.write(contract + '\n')

