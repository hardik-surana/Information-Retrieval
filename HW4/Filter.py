import pickle

outlink_file = open('E:/IR/HW4/outlinks.pkl', 'ab+')
inlink_file = open('E:/IR/HW4/inlinks.pkl', 'ab+')
global_inlink_dict = {}
global_outlink_dict = {}


def load_inlinks():
    global global_inlink_dict
    inlink_file = open('E:/IR/HW3/merged_inlinks', 'r')
    for l in inlink_file.readlines():
        list = l.split('\t')
        key = list[0]
        list.pop(0)
        values = [x for x in list if x]
        global_inlink_dict[key] = values


def load_outlinks():
    global global_outlink_dict
    outlink_file = open('E:/IR/HW3/hw3-merged-outlinks.txt', 'r')
    for l in outlink_file.readlines():
        list = l.split('\t')
        key = list[0]
        list.pop(0)
        values = [x for x in list if x]
        global_outlink_dict[key] = values

def get_url(di):
    url_list = []
    for key in di.keys():
        url_list += [key]
    return url_list

load_inlinks()
load_outlinks()
url_list = get_url(global_outlink_dict)
i = 0
j= 0
for il in global_inlink_dict.keys():
    print i
    temp_list = []
    if not url_list.__contains__(il):
        del global_inlink_dict[il]
    else:
        continue
    i += 1
print 'inlinks done'

# for iout in global_outlink_dict.keys():
#     print j
#     for lout in global_outlink_dict[iout]:
#         if url_list.__contains__(lout):
#             temp_list += [lout]
#     global_outlink_dict[iout] = temp_list
#     j += 1
# print 'outlink done'

print len(global_inlink_dict)
print len(global_outlink_dict)

pickle.dump(global_inlink_dict, inlink_file)
pickle.dump(global_outlink_dict, outlink_file)

inlink_file.close()
outlink_file.close()