import os, re

RESULTS_PATH = "o_results/"
RESULT_FILE = "o_results/node.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'w')
for fl in log_files:
    if not (fl.find("node") == 0 and fl.find("log") > 0):
        continue
    lines = []
    with open(RESULTS_PATH + fl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
    print(fl)
    deployGas, deployCnt = 0, 0
    #{func: [totalGasUsed, times]}
    gasUsed = {}

    for i in range(len(lines)):
        if lines[i].find("contract deploy success, receipt:") == 0:
            while(1):
                i += 1
                if(lines[i].find("}") == 0):
                    break
                if(lines[i].find("gasUsed: ") > 0):
                    deployGas += int(re.sub("\D", "", lines[i]).strip(",\n"))
                    deployCnt += 1
                    break
        if lines[i].find("success") > 0 and lines[i].find("status: true") > 0:
            func = lines[i].split(" ")[0]
            gas = int(lines[i].split(" ")[-1].strip())
            if func not in gasUsed:
                gasUsed[func] = [0, 0]
            gasUsed[func][0] += gas
            gasUsed[func][1] += 1
    
    if deployCnt:
        res_file.write("%s\ndeployGas: %d\n" % (fl, deployGas / deployCnt))
    for func in gasUsed:
        if gasUsed[func][1]:
            res_file.write("function: %s gasUsed: %d\n" % (func, gasUsed[func][0] / gasUsed[func][1]))
    if deployCnt:
        res_file.write("\n")



    