import os

RESULTS_PATH = "e_results/"
RESULT_FILE = "e_results/io.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'w')
for fl in log_files:
    if not (fl.find("io") == 0 and fl.find("log") > 0):
        continue
    lines = []
    print(fl)
    with open(RESULTS_PATH + fl, 'r', encoding="utf-8") as rf:
        lines = rf.readlines()

    totalWrite, totalRead = 0, 0
    id2file = {}
    # {file: [write, read]}
    file2io = {}
    for ll in lines:
        ll = ll.strip()
        if ll.find("total") == 0:
            id2file = {}
            continue

        elif ll.find("coldplay coldplay 64") > 0:
            idx, ff = ll.split(" ")[-3], ll.split(" ")[-1]
            if ff.find("/home/coldplay/ewasm-node/data/geth/") == 0:
                id2file[idx] = ff
                if ff not in file2io:
                    file2io[ff] = [0, 0]
                

        elif ll.find("read#") == 0 or ll.find("write#") == 0:
            length, idx = int(ll.split("#")[1]), ll.split("#")[2]
            if idx in id2file:
                if ll.find("write#") == 0:
                    totalWrite += int(length)
                    file2io[id2file[idx]][0] += length

                elif ll.find("read#") == 0:
                    totalRead += int(length)
                    file2io[id2file[idx]][1] += length
    
    print(totalWrite)
    print(totalRead)
    # print(file2io[f][0])
    # print(file2io[f][1])
    res_file.write("%s\ntotalWrite:%d#totalRead:%d\n" % (fl, totalWrite, totalRead))
    for f in file2io:
        if file2io[f][0] or file2io[f][1]:
            res_file.write("%s#write:%d#read:%d\n" % (f, file2io[f][0], file2io[f][1]))
    res_file.write("\n")

res_file.close()
    


