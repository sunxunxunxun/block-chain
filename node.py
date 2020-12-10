import os, re

RESULTS_PATH = "../logs/e_results/"
RESULT_FILE = "../results/e_func_gas_executionTime.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'w')
for nodeFl in log_files:
    if not (nodeFl.find("node") == 0 and nodeFl.find("log") > 0):
        continue
    lines = []
    with open(RESULTS_PATH + nodeFl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
    print(nodeFl)
    deployGas, deployCnt = 0, 0
    #{func: [totalGasUsed, totalTime, gasCount, exeCount]}
    funcInfo = {}
    function = []

    # calculate gasUsed of function
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
            if func not in funcInfo:
                funcInfo[func] = [0, 0, 0, 0]
                function.append(func)
            funcInfo[func][0] += gas
            funcInfo[func][2] += 1
    
    print(function)
    # calculate execution time of func
    if len(function):
        runFl = "run_" + "_".join(nodeFl.split('_')[1:])
        print(runFl)
        lines = []
        with open(RESULTS_PATH + runFl, 'r', encoding='utf-8') as rf:
            lines = rf.readlines()
        
        start, end = 0, 0
        funcId = 0
        cnt = 0
        for line in lines:
            # for openethereum
            if line.find("#execute#start#") > 0:
            # for platon
            # if line.find("#start#") > 0:
                if cnt == 0:
                    cnt += 1
                    continue
                start = int(line.split('#')[0])
                cnt = (cnt + 1) % 101
            #for openethereum
            if (line.find("#execute#end#") > 0 or line.find("#execute#End#") > 0) and start:
            # for platon
            # if (line.find("#end#") > 0 or line.find("#End#") > 0) and start:
                end = int(line.split('#')[0])
                func = function[funcId]
                funcInfo[func][1] += end - start
                funcId = (funcId + 1) % len(function)
                funcInfo[func][3] += 1
                start = 0

    if deployCnt:
        res_file.write("%s\ndeployGas: %d\n" % ("_".join(nodeFl.split('_')[1:]), deployGas / deployCnt))
    for func in funcInfo:
        if funcInfo[func][2]:
            res_file.write("function: %s#gasUsed: %d" % (func, funcInfo[func][0] / funcInfo[func][2]))
        if funcInfo[func][3]:
            res_file.write("#execution time: %d" % (funcInfo[func][1] / funcInfo[func][3]))
        res_file.write("\n")
    res_file.write("\n")