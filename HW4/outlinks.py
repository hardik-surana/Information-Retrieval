import pickle

global_inlink_dict = {}
global_outlink_dict = {}
path = "E:/IR/HW4/wt2g_inlinks.txt"
i = 0
outlink_pickle = open('E:/IR/HW4/wt2g_outlinks.pkl', 'ab+')
inlink_pickle = open('E:/IR/HW4/wt2g_inlinks.pkl', 'ab+')
inlink_file = open(path, 'r')

for l in inlink_file.readlines():
    i += 1
    print i
    list = l.split(' ')
    key = list[0]
    list.pop(0)
    list.remove('\n')
    values = [x for x in list if x]
    global_inlink_dict[key] = values
    key_list = [key]
    for l in values:
        if not global_outlink_dict.__contains__(l):
            global_outlink_dict[l] = key_list
        elif not global_outlink_dict[l].__contains__(key):
            global_outlink_dict[l] = global_outlink_dict[l] + key_list
        else:
            global_outlink_dict[l] = global_outlink_dict[l] + key_list


pickle.dump(global_outlink_dict, outlink_pickle)
pickle.dump(global_inlink_dict, inlink_pickle)
inlink_file.close()
outlink_pickle.close()
inlink_pickle.close()