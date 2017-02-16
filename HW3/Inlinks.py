import pickle
import glob

global_inlink_dict = {}
global_outlink_dict = {}
path = "E:/IR/HW3/hw3-merged-outlinks.txt"
i = 0
inlink_file = open('E:/IR/HW3/merged_inlinks', 'ab+')
outlink_file = open(path, 'r')


def write_inlinks(dict):
    for key in dict.keys():
        inlink_file.write('%s\t' % key)
        #print dict[key]
        if len(dict[key]) > 0:
            for l in dict[key]:
                inlink_file.write('\t%s' % l)
            inlink_file.write('\n')
        else:
            inlink_file.write('\n')


for l in outlink_file.readlines():
    i += 1
    print i
    list = l.split('\t')
    key = list[0]
    list.pop(0)
    values = [x for x in list if x]
    global_outlink_dict[key] = values
    key_list = [key]
    for l in values:
        if not global_inlink_dict.__contains__(l):
            global_inlink_dict[l] = key_list
        elif not global_inlink_dict[l].__contains__(key):
            global_inlink_dict[l] = global_inlink_dict[l] + key_list
        else:
            global_inlink_dict[l] = global_inlink_dict[l] + key_list


write_inlinks(global_inlink_dict)

outlink_pkl = open('outlink.pkl', 'wb')
inlink_pkl = open('inlink.pkl', 'wb')
pickle.dump(global_outlink_dict, outlink_pkl)
pickle.dump(global_inlink_dict, inlink_pkl)
inlink_file.close()
outlink_file.close()
outlink_pkl.close()
inlink_pkl.close()
