from operator import itemgetter
import operator

inlink_file = open('E:/IR/HW3/merged_inlinks', 'r')
i = 0
global_inlink_dict = {}
page_rank_file = open('E:/IR/HW4/page_rank', 'wb')

for l in inlink_file.readlines():
    i += 1
    print i
    list = l.split('\t')
    key = list[0]
    list.pop(0)
    values = [x for x in list if x]
    global_inlink_dict[key] = values

temp_dict = {}

for key in global_inlink_dict.keys():
    temp_dict[key] = len(global_inlink_dict[key])

sorted_dict = sorted(temp_dict.items(), key=lambda x:x[1], reverse=True)[:500]
for (k, v) in sorted_dict:
    page_rank_file.write('%s\n' % k)