from __future__ import division
import math
from math import ceil, floor


def float_round(num, places=0, direction=floor):
    return direction(num * (10 ** places)) / float(10 ** places)


precision_dict = {}
recall_dict = {}
r_rank_dict = {}
f1_rank = {}
avg_precision_dict = {}
ndcg_dict = {}
retrieved_dict = {}
relevant_dict = {}
ret_rel_dict = {}
total_dict = {}

global_qrel_dict = {}
qrel_file = open("E:/IR/HW5/merged-assessment.txt", 'r')
# qrel_file = open("E:/IR/Data/AP_DATA/qrels.adhoc.51-100.AP89.txt", 'r')

for line in qrel_file.readlines():
    list = line.split(' ')
    qid = list[0].strip()
    docid = list[2]
    rank = int(list[3].strip('\n'))
    if not global_qrel_dict.__contains__(qid):
        global_qrel_dict[qid] = [(docid, rank)]
    else:
        global_qrel_dict[qid].append((docid, rank))

print len(global_qrel_dict)
global_result_dict = {}
result_file = open('E:/IR/HW5/Rank_list.txt', 'r')
# result_file = open('E:/IR/HW1Results/okapitf_model.txt', 'r')
for ln in result_file.readlines():
    lt = ln.strip('\n').split(' ')
    q = lt[0]
    d = lt[2]
    if not global_result_dict.__contains__(q):
        global_result_dict[q] = [d]
    else:
        global_result_dict[q].append(d)

qrel_file.close()
result_file.close()
print len(global_result_dict)

# for each in global_result_dict:
#     lst = global_result_dict[each]
#     sorted_list = sorted(lst,key=itemgetter(1))
#     global_result_dict = sorted_list

cutoffs = [5, 15, 30, 50, 100, 200]
# cutoffs = [5, 10, 15, 20, 30, 100, 200, 500, 1000]


def float_round(num, places=0, direction=floor):
    return direction(num * (10 ** places)) / float(10 ** places)


def calculate_ndcg(count, tuple_list):
    try:
        i = 2
        j = 2
        dcg_score = 0
        ndcg_score = 0
        dcg_list = tuple_list[0:count]
        sorted_dcg_list = sorted(dcg_list, key=lambda x: x[1], reverse=True)
        first_dcg_tuple = dcg_list[0]
        first_dcg = first_dcg_tuple[1]
        dcg_list = dcg_list[1:]
        first_ndcg_tuple = sorted_dcg_list[0]
        first_ndcg = first_ndcg_tuple[1]
        sorted_dcg_list = sorted_dcg_list[1:]
        dcg_score += first_dcg
        for tup in dcg_list:
            a = tup[1]
            dcg_score += (a / math.log(i, 2))
            i += 1
        ndcg_score += first_ndcg
        for tupl in sorted_dcg_list:
            b = tupl[1]
            ndcg_score += (b / math.log(j, 2))
            j += 1

        score = dcg_score / ndcg_score
    except Exception as e:

        score = 0

    return score


def print_data():
    total_ret = 0
    total_rel = 0
    total_rel_ret = 0
    total_avg_precision = 0
    total_r_precision = 0
    f1 = open('E:/IR/HW5/Result_wed1.txt', 'a')
    for key in precision_dict.keys():
        f1.write('Query ID: %s \n' % key)
        f1.write('Total number of documents \n')
        f1.write('Retrieved: %s \n' % retrieved_dict[key])
        f1.write('Relevant: %s \n' % relevant_dict[key])
        f1.write('Relevant & Retrieved: %s \n' % ret_rel_dict[key])
        f1.write('Precision: \n')
        for item in precision_dict[key]:
            f1.write('At %d docs: %f \n' % (item[0], item[1]))
        f1.write('Recall: \n')
        for item in recall_dict[key]:
            f1.write('At %d docs: %f \n' % (item[0], item[1]))
        f1.write('F1: \n')
        for item in f1_rank[key]:
            f1.write('At %d docs: %f \n' % (item[0], item[1]))
        f1.write('NDCG: \n')
        for item in ndcg_dict[key]:
            f1.write('At %d docs: %f \n' % (item[0], item[1]))
        f1.write('R-Precision: %f \n' % r_rank_dict[key])
        f1.write('Average precision of the query: %f \n' % avg_precision_dict[key])
        f1.write('\n================================================================================ \n')
    f1.write('Total queries: %d \n' % len(precision_dict))
    f1.write('Total number of documents: \n')
    for key in retrieved_dict.keys():
        total_rel += relevant_dict[key]
        total_ret += retrieved_dict[key]
        total_rel_ret += ret_rel_dict[key]
        total_avg_precision += avg_precision_dict[key]
        total_r_precision += r_rank_dict[key]
    f1.write('Retrieved: %s \n' % total_ret)
    f1.write('Relevant: %s \n' % total_rel)
    f1.write('Relevant & Retrieved: %s \n' % total_rel_ret)
    f1.write('Precision: \n')
    sorted_dict = sorted(total_dict.iteritems(), key=lambda x: -x[0], reverse=True)
    for l in sorted_dict:
        f1.write('At %d docs: %f \n' % (l[0], (l[1] / len(precision_dict))))
    f1.write('Total R-Precision: %f \n' % (total_r_precision / len(precision_dict)))
    f1.write('Total Average precision of the query: %f \n' % (total_avg_precision / len(precision_dict)))
    return


for key in global_result_dict.keys():
    retrieved = 0
    ret_and_rel = 0
    relevant = 0
    fp = 0
    r_precision = 0
    total_precision = 0

    if not global_qrel_dict.__contains__(key):
        continue
    else:
        doc_list = global_result_dict[key]
        pair_list = global_qrel_dict[key]

        for pair in pair_list:
            t = pair
            val = t[1]
            if val > 0:
                relevant += 1
        for url in doc_list:
            precision = 0
            recall = 0
            f1 = 0
            ndcg = 0
            retrieved += 1
            tup = [item for item in pair_list if url in item]
            if not tup:
                fp += 1
            else:
                value = tup[0][1]
                if value > 0:
                    ret_and_rel += 1
            try:
                recall = ret_and_rel / relevant
                precision = ret_and_rel / retrieved

            except:
                recall = 0
                precision = 0
            try:
                f1 = (2 * precision * recall) / (precision + recall)
            except:
                f1 = 0

            if tup:
                v = tup[0][1]
                if v > 0:
                    total_precision += precision

            if retrieved in cutoffs:

                ndcg = calculate_ndcg(retrieved, pair_list)

                if not precision_dict.__contains__(key):
                    precision_dict[key] = [(retrieved, precision)]
                else:
                    precision_dict[key].append((retrieved, precision))

                if not recall_dict.__contains__(key):
                    recall_dict[key] = [(retrieved, recall)]
                else:
                    recall_dict[key].append((retrieved, recall))

                if not f1_rank.__contains__(key):
                    f1_rank[key] = [(retrieved, f1)]
                else:
                    f1_rank[key].append((retrieved, f1))

                if not ndcg_dict.__contains__(key):
                    ndcg_dict[key] = [(retrieved, ndcg)]
                else:
                    ndcg_dict[key].append((retrieved, ndcg))

                if not total_dict.__contains__(retrieved):
                    total_dict[retrieved] = precision
                else:
                    total_dict[retrieved] += precision

            if (relevant == retrieved):
                r_precision = precision
                r_rank_dict[key] = r_precision

    average_precision = total_precision / relevant
    avg_precision_dict[key] = average_precision
    relevant_dict[key] = relevant
    retrieved_dict[key] = retrieved
    ret_rel_dict[key] = ret_and_rel

for query in precision_dict.keys():
    if not r_rank_dict.__contains__(query):
        r_rank_dict[query] = 0.0

print_data()
