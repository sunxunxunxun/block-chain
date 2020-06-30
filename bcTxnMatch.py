import os

# BC_DIR = './deploycode/'
# TXN_DIR = './contractTxn/'
# MATCH_FILE = './contractwithTxnBc'

# if not os.path.exists(MATCH_FILE):
#     fp = open(MATCH_FILE, 'w')
#     fp.close()

# match_file = open(MATCH_FILE, 'a')
# txn_files = os.listdir(TXN_DIR)
# bc_files = os.listdir(BC_DIR)
# cnt = 0
# for txn_file in txn_files:
#     if txn_file in bc_files:
#         match_file.write(txn_file + '\n')
#     cnt+=1
#     print("%d/%d\n" % (cnt, len(txn_files)))

# match_file.close()

bc_files = dict(zip(os.listdir('./deploycode/'), range(len(os.listdir('./deploycode/')))))
open('./contractWithTxnBc', 'w').write('\n'.join([txn_file for txn_file in os.listdir('./contractTxn/') if txn_file in bc_files]))