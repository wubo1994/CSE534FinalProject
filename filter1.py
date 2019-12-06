import json
import matplotlib.pyplot as plt

outfile = open('outfiletls.json', 'w')

with open('iw-alexa-tls_2019_10_21.json','r') as json_file:
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
infile = open('outfiletls.json', 'r')
line = infile.readline()
outfile = open('outfiletls1.json','w')
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

infile = open('outfiletls1.json','r')
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
print(IWtoNumMap)
num = 0
for key in IWtoNumMap:
    num = num + IWtoNumMap[key]
print('Total number:',num,'\n')
infile.close()
IWlist = [1,2,3,4,5,6,9,10,11,14,16,24,48]
IWnoList = []
for key in IWtoNumMap:
    if key not in IWlist:
        IWnoList.append(key)
for item in IWnoList:
    IWtoNumMap.pop(item)
print(IWtoNumMap)
sorted_dict = {k: IWtoNumMap[k] for k in sorted(IWtoNumMap)}
print(sorted_dict)
plt.bar(range(len(sorted_dict)), list(sorted_dict.values()), align='center')
plt.xticks(range(len(sorted_dict)), list(sorted_dict.keys()))
plt.yscale('log')
plt.show()