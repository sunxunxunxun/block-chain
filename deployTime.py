import os

RESULTS_PATH = "deploy/"
RESULT_FILE = "deploy/e_deploy_time.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'a+')
for nodeFl in log_files:
    if not (nodeFl.find("node_e_evm") == 0 and nodeFl.find("log") > 0):
        continue
    print(nodeFl)
    
    lines = []
    bench = []
    with open(RESULTS_PATH + nodeFl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
    
    pre = ""
    for line in lines:
        if line.find("deploy success, receipt:") > 0 and (len(bench) == 0 or line.split(' ')[1] != bench[-1]):
            bench.append(line.split(' ')[1])
    print(bench)
    runFl = "run_" + "_".join(nodeFl.split("_")[1:])
    print(runFl)
    
    lines = []
    with open(RESULTS_PATH + runFl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()

    res_file.write("_".join(runFl.split('_')[1:]) + "\n")

    deployTime = []
    totalTime = 0    
    start, end = 0, 0
    cnt = 0
    for i in range(len(lines)):
        if lines[i].find("#start#") > 0:
            start = int(lines[i].split('#')[0])
            # print(start)
        elif lines[i].find("#end") > 0 or lines[i].find("#End") > 0 and start:
            end = int(lines[i].split('#')[0])
            # print(end)
            totalTime += end - start
            start = 0
            cnt += 1
            if cnt and (cnt % 102 == 0):
                deployTime.append(totalTime / 102)
                totalTime = 0
    print(cnt)
    if cnt % 102 != 0:
        print("exception: cnt: %d != 100 * len(bench): %d\n" % (cnt, len(bench)))   
    
    for i in range(len(bench)):
        res_file.write("%s: %d\n" % (bench[i], deployTime[i]))
    res_file.write("\n")
                
res_file.close()


