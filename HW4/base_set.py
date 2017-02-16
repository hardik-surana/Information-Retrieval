import pickle

root_set_file = open('E:/IR/HW4/okapi_bm25_model.txt', 'r')
outlink_file = open('E:/IR/HW4/outlinks.pkl', 'r')
inlink_file = open('E:/IR/HW4/inlinks.pkl', 'r')
outlinks = pickle.load(outlink_file)
inlinks = pickle.load(inlink_file)

def load_links():
    link_list = []
    for l in root_set_file.readlines():
        lin = l.rstrip('\n')
        link_list.append(lin)
    return link_list

base_set = load_links()
add_set = []
print len(base_set)

for l in base_set:
    if inlinks.__contains__(l):
        inlist = inlinks[l]
        if len(inlist) > 50:
            in_list = inlist[0:49]
            add_set += in_list
        else:
            add_set += inlist
    if outlinks.__contains__(l):
        outlist = outlinks[l]
        add_set += outlist

print len(add_set)
final_set = base_set + add_set
fin = []
for i in final_set:
    if not fin.__contains__(i):
        fin.append(i)

print len(set(fin))

# base_list_file = open('E:/IR/HW4/Base_set.txt', 'ab+')
# for b in fin:
#     base_list_file.write('%s' % b)
#     base_list_file.write('\n')



