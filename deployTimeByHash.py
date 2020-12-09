import os

RESULTS_PATH = "deploy/ewasm_deploy_results/"
RESULT_FILE = "deploy/ewasm_deploy_results/e_deploy_time.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'w')

for nodeFl in log_files:
    if not (nodeFl.find("node_") == 0 and nodeFl.find("log") > 0):
        continue
    print(nodeFl)
    
    # record transactions' hashs
    lines = []
    # {hash1: bench, hash2: bench, ...}
    hash2bench = {}
    with open(RESULTS_PATH + nodeFl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
    
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i].find("deploy success, receipt:") > 0:
            func = lines[i].split(' ')[1]
            while not (lines[i].find("transactionHash: ") > 0):
                i += 1
            hash = lines[i].split('\'')[1]
            hash2bench[hash] = func
    # check if normal
    # print("bench: " + len(bench))
    # for bc in bench:
    #     if len(bench[bc]) != 100:
    #         print("%s don't execute 100 times\n" % bc)

    runFl = "run_" + "_".join(nodeFl.split("_")[1:])
    print(runFl)
    
    lines = []
    with open(RESULTS_PATH + runFl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()

    res_file.write("_".join(runFl.split('_')[1:]) + "\n")

    # deployTime = {bench: [totalTime, count, start]}
    deployTime = {}

    totalTime = 0    
    start, end = 0, 0
    bench = ""
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
        if lines[i].find("#start#") > 0:
            start = int(lines[i].split('#')[0])
            hash = lines[i].split(":")[-1]
            bench = hash2bench[hash]
            print(bench)
            if bench not in deployTime:
                deployTime[bench] = [0, 0, 0]
            deployTime[bench][2] = start
            # print(start)
        elif lines[i].find("#end") > 0 or lines[i].find("#End") > 0:
            end = int(lines[i].split('#')[0])
            # print(end)
            if not (bench and deployTime[bench][2]):
                print("error: no start but end\n")
            deployTime[bench][0] += end - deployTime[bench][2]
            deployTime[bench][1] += 1
            deployTime[bench][2] = 0
            
    for bench in deployTime:
        if deployTime[bench][1]:
            res_file.write("%s: %d\n" % (bench, deployTime[bench][0] / deployTime[bench][1]))
    res_file.write("\n")
                
res_file.close()


