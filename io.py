import os

RESULTS_PATH = "p_results/"
RESULT_FILE = "p_results/io.txt"

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
    # {id: file}
    id2file = {}
    # {file: [write, read]}
    file2io = {}
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i].find("openat#") == 0:
            id2file = {}

        if lines[i].find("/home/coldplay/platon-node/data/") > 0:
            if lines[i].find("openat#") == 0:
                idx, ff = lines[i+1].strip().split("#")[-1], lines[i].split("#")[1]
                id2file[idx] = ff
                print(idx, ff)
                if ff not in file2io:
                    file2io[ff] = [0, 0]

            elif lines[i].find("coldplay coldplay 64") > 0:
                idx, ff = lines[i].split(" ")[-3], lines[i].split(" ")[-1]
                if ff.find("/home/coldplay/platon-node/data//") == 0:
                    id2file[idx] = ff
                    if ff not in file2io:
                        file2io[ff] = [0, 0]
                
        elif lines[i].find("read#") == 0 or lines[i].find("write#") == 0:
            length, idx = int(lines[i].split("#")[1]), lines[i].split("#")[2]
            if idx in id2file:
                if lines[i].find("write#") == 0:
                    totalWrite += int(length)
                    file2io[id2file[idx]][0] += length

                elif lines[i].find("read#") == 0:
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
    


