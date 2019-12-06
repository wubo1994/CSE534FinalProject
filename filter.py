import json
import matplotlib.pyplot as plt
import numpy as np

outfile = open('outfile.json', 'w')

with open('iw-alexa-http_2019_10_28.json','r') as json_file:
    #data = json.load(json_file)
    #print(data)
    line = json_file.readline()
    while line:
        #data = json.load(line)
        data = json.loads(line)
        if 'rep_mss' in data:
            if data['success'] == 1 and data['rep_mss'] == 64:
                json.dump(data, outfile)
                outfile.write('\n')
        line = json_file.readline()

json_file.close()
outfile.close()

IWtoNumMap = {}
filterMap = {}
infile = open('outfile.json', 'r')
line = infile.readline()
outfile = open('outfile1.json','w')
while line:
    data = json.loads(line)
    if data['saddr'] in filterMap:
        line = infile.readline()
        continue
    else:
        filterMap[data['saddr']] = 1
        line = infile.readline()
        json.dump(data, outfile)
        outfile.write('\n')
infile.close()
outfile.close()

infile = open('outfile1.json','r')
line = infile.readline()
while line:
    data = json.loads(line)
    #print(data)
    if 'packets' in data:
        IW = data['packets']
    else:
        line = infile.readline()
        continue
    if IW in IWtoNumMap:
        IWtoNumMap[IW] = IWtoNumMap[IW]+1
    else:
        IWtoNumMap[IW] = 1
    line = infile.readline()
num = 0
for key in IWtoNumMap:
    num = num + IWtoNumMap[key]
print('Total number:',num,'\n')
print(IWtoNumMap)
infile.close()
IWlist = [1,2,3,4,5,6,9,10,11,14,16,24,48]
IWnoList = []
for key in IWtoNumMap:
    if key not in IWlist:
        IWnoList.append(key)
for item in IWnoList:
    IWtoNumMap.pop(item)
sorted_dict = {k: IWtoNumMap[k] for k in sorted(IWtoNumMap)}
print(sorted_dict)
#plt.bar(range(len(sorted_dict)), list(sorted_dict.values()), align='center')
#plt.xticks(range(len(sorted_dict)), list(sorted_dict.keys()))
#plt.yscale('log')
#plt.show()
x = [1,2,3,4,5,6,9,10,11,14,16,24,48]
y1 = [223, 1351, 44, 1948, 250, 49, 935, 202232, 218, 6, 32, 15, 328]
y2 = [383, 1221, 93, 2299, 275, 93, 139, 224846, 92, 5, 128, 80, 728]
print('HTTP IW 1 percentage: ',223/num)
print('TLS IW 1 percentage: ',383/231730)
X = np.arange(13)
plt.xticks(range(len(sorted_dict)), list(sorted_dict.keys()))
plt.bar(X + 0.00, y1, color = 'b', width = 0.25, label='HTTP')
plt.bar(X + 0.25, y2, color = 'g', width = 0.25, label='TLS')
plt.yscale('log')
plt.xlabel('Initial Window Size')
plt.ylabel('# of hosts')
plt.legend()
plt.show()