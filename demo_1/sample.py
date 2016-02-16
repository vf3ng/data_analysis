import sys
import random

data_list = list()
for line in sys.stdin:
    line = line[:-1]
    data_list.append(line)

sample_count = int(sys.argv[1])
sample_list = list()

if sample_count >= len(data_list):
    sample_list = data_list
else:
    sample_list = random.sample(data_list,sample_count)


for line in sample_list:
    print line

