import os

RESULTS_PATH = "e_results/"
RESULT_FILE = "e_results/run.txt"

log_files = os.listdir(RESULTS_PATH)
res_file = open(RESULT_FILE, 'w')
for fl in log_files:
    if not (fl.find("run") == 0 and fl.find("log") > 0):
        continue
    lines = []
    with open(RESULTS_PATH + fl, 'r', encoding='utf-8') as rf:
        lines = rf.readlines()
    print(fl)

    # info = {func: [totalDuration, totalSpace, times, start, space]}
    info = {}
    for i in range(len(lines)):
        lines[i].strip()
        if lines[i].find("#start#") > 0 or lines[i].find("#end#") > 0 or lines[i].find("#End#") > 0:
            func = lines[i].split('#')[1]
            if func not in info:
                info[func] = [0, 0, 0, -1, -1]

            time = int(lines[i].split('#')[0])
            try:   
                s = lines[i].split('#')[4]
            except:
                while(lines[i].find("#Total Alloc:") != 0):
                    i += 1
                s = lines[i].split('#')[1]
                print(s)
            if s.isdigit():
                space = int(s)
            else:
                s = s.split(':')[1]
                _s = ''
                for _ in s:
                    if _.isdigit(): _s += _
                    else: break
                space = int(_s) 
            # print(info[func][3])
            # print(info[func][4])
            if (lines[i].find("#end#") > 0 or lines[i].find("#End#") > 0) and func in info and info[func][3] != -1 and info[func][4] != -1:
                info[func][0] += time - info[func][3]
                info[func][1] += space - info[func][4]
                info[func][2] += 1
                info[func][3] = -1
                info[func][4] = -1
            elif lines[i].find("#start#") > 0:
                info[func][3] = time
                info[func][4] = space
        
    res_file.write(fl + "\n")
    for func in info:
        # print(info[func][2])
        if info[func][2]:
            res_file.write("function:%s#executionTime:%d#spaceUsage:%d\n" % (func, info[func][0] / info[func][2], info[func][1] / info[func][2]))
    res_file.write("\n")

res_file.close()


