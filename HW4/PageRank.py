from __future__ import division
import math
from math import modf
import pickle

global_outlink_dict = {}
outlink_pickle = open('E:/IR/HW4/outlinks.pkl', 'r')
inlink_pickle = open('E:/IR/HW4/inlinks.pkl', 'r')
global_inlink_dict = pickle.load(inlink_pickle)
global_outlink_dict = pickle.load(outlink_pickle)
outlink_pickle.close()
inlink_pickle.close()


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


def get_unit_value(num):
    b, a = modf(num)
    return a % 10


def print_PR(dict):
    pagerank_dict_sorted = (sorted(dict.iteritems(), key=lambda x: -x[1])[:500])
    f1 = open('E:/IR/HW4/Page_Rank.txt', 'a')
    for (rank, row) in enumerate(pagerank_dict_sorted):
        f1.write('%s\n' % row[0])


def calculate_convergance(pagerank_dict):
    convergance = 0
    sum = 0
    for key in pagerank_dict.keys():
        sum += pagerank_dict[key] * math.log(pagerank_dict[key], 2)
    convergance += math.pow(2, (sum * -1))
    return convergance


# load_inlinks()
# load_outlinks()
pagerank_dict = {}
N = len(global_outlink_dict)
d = 0.85
sinkPages = []
for key in global_outlink_dict.keys():
    if key == "":
        continue
    pagerank_dict[key] = 1 / N
    if not global_outlink_dict[key]:
        sinkPages = sinkPages + [key]

converged = False
old_convergance = 0
new_convergance = 1
flag = 1
print len(global_inlink_dict)
print len(global_outlink_dict)

while not converged:
    newPR = {}
    sinkPR = 0
    for p in sinkPages:
        sinkPR += pagerank_dict[p]
    for key in pagerank_dict.keys():
        newPR[key] = 0.15 / N
        newPR[key] += d * sinkPR / N
        if global_inlink_dict.__contains__(key):
            for link in global_inlink_dict[key]:
                if global_outlink_dict.__contains__(link) and len(global_outlink_dict[link]) > 0:
                    newPR[key] += d * pagerank_dict[link] / len(global_outlink_dict[link])
    new_convergance = calculate_convergance(newPR)
    pagerank_dict = dict(newPR)
    print new_convergance
    if get_unit_value(old_convergance) == get_unit_value(new_convergance):
        flag += 1
        old_convergance = new_convergance
        if flag == 4:
            converged = True
            print_PR(newPR)
    else:
        flag = 1
        old_convergance = new_convergance
