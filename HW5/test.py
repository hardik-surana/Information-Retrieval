from __future__ import division

global_qrel_dict = {}
qrel_file = open("E:/IR/HW5/merged-assessment.txt", 'r')
okapi_file = open('E:/IR/HW5/Rank_list.txt', 'a')

for line in qrel_file.readlines():
    list = line.split(' ')
    qid = list[0].strip()
    docid = list[2]
    rank = int(list[3].strip('\n'))
    if not global_qrel_dict.__contains__(qid):
        global_qrel_dict[qid] = [docid]
    else:
        global_qrel_dict[qid].append(docid)

sorted_dict = {}

for k in global_qrel_dict.keys():
    lst = global_qrel_dict[k]
    truncate_list = lst[0:100]
    sorted_dict[k] = truncate_list

# sorted_rank_dict = sorted(sorted_dict.iteritems(), key=lambda x: -x[0], reverse=True)

for tup in sorted_dict:
    docs = sorted_dict[tup]
    Q0num = tup
    i = 1
    for d in docs:
        okapi_file.write('%s Q0 %s %d %f Exp \n' % (Q0num, d,i , i))
        i += 1
