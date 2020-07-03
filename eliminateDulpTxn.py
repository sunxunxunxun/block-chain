import os

CONTRACT_TXN_PATH = './contractTxn/'

txn_files = os.listdir(CONTRACT_TXN_PATH)
for txn_file in txn_files:
    with open(CONTRACT_TXN_PATH + txn_file, 'r', encoding = 'utf-8') as rf:
        txn_lines = rf.readlines()
    len_before = len(txn_lines)
    txns_unique = set()
    cnt1, cnt2 = 0, 0
    del_lines = []
    for line in txn_lines:
        line_tail = line.split('#', 1)[1].strip()    #默认是-1，分割所有
        if line_tail in txns_unique:   
            del_lines.append(line)
            # txn_lines.remove(line)    不能遍历的时候删
        else:
            txns_unique.add(line_tail)
    for line in del_lines:
        txn_lines.remove(line)
    if len(txn_lines)<len_before:
        with open(CONTRACT_TXN_PATH + txn_file, 'w', encoding = 'utf-8') as wf:
            wf.write(''.join(txn_lines))