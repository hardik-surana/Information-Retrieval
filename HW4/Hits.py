from __future__ import division
import math
from math import modf
import pickle

base_set_file = open('E:/IR/HW4/Base_set.txt', 'r')
outlink_file = open('E:/IR/HW4/outlinks.pkl', 'r')
inlink_file = open('E:/IR/HW4/inlinks.pkl', 'r')
outlinks_dict = pickle.load(outlink_file)
inlinks_dict = pickle.load(inlink_file)
base_set = []
auth_dict = {}
hub_dict = {}


def load_links():
    link_list = []
    for l in base_set_file.readlines():
        lin = l.rstrip('\n')
        if lin != '':
            link_list.append(lin)
    return link_list


base_set = load_links()

print len(base_set)

for b in base_set:
    auth_dict[b] = 1
    hub_dict[b] = 1


def normalizing_value(dict):
    n_score = 0
    for key in dict.keys():
        n_score += math.pow(dict[key], 2)
    n_score = math.sqrt(n_score)
    return n_score


def calculate_auth(l):
    score = 0
    if inlinks_dict.__contains__(l):
        inlinks = inlinks_dict[l]
        for li in inlinks:
            if hub_dict.__contains__(li):
                score += hub_dict[li]
    else:
        score += 1
    return score


def update_dict(dict):
    norm = normalizing_value(dict)
    for key in dict.keys():
        dict[key] = dict[key] / norm


def calculate_hub(l):
    score = 0
    if outlinks_dict.__contains__(l):
        outlinks = outlinks_dict[l]
        for li in outlinks:
            if auth_dict.__contains__(li):
                score += auth_dict[li]
    else:
        score += 1
    return score


def calculate_convergance(dict):
    convergance = 0
    sum = 0
    for key in dict.keys():
        print dict[key]
        sum += dict[key] * math.log(dict[key], 2)
    convergance += math.pow(2, (sum * -1))
    return convergance


def get_unit_value(num):
    b, a = modf(num)
    return a % 10

def isnotconverged(dict, prev_dict):
    flag = False
    if not prev_dict:
        return True
    else:
        for key in dict.keys():
            if key != '':
                if prev_dict[key] - dict[key] <= 0.001:
                    flag = False
                else:
                    print "yellow"
                    flag = True
                    break
    return flag


def print_auth(dict):
    dict_sorted = (sorted(dict.iteritems(), key=lambda x: -x[1])[:500])
    f1 = open('E:/IR/HW4/HITS_auth.txt', 'a')
    for (rank, row) in enumerate(dict_sorted):
        f1.write('%s\t%f\n' % (row[0], row[1]))

def print_hub(dict):
    dict_sorted = (sorted(dict.iteritems(), key=lambda x: -x[1])[:500])
    f1 = open('E:/IR/HW4/HITS_hubs.txt', 'a')
    for (rank, row) in enumerate(dict_sorted):
        f1.write('%s\t%f\n' % (row[0], row[1]))


converged = True
# old_hub_convergance = calculate_convergance(hub_dict)
# old_auth_convergance = calculate_convergance(auth_dict)
# new_hub_convergance = 1
# new_auth_convergance = 1
flag = 0

while flag <= 4:
    new_auth = {}
    new_hub = {}
    for p in base_set:
        new_auth[p] = calculate_auth(p)
    update_dict(new_auth)

    for pa in base_set:
        new_hub[pa] = calculate_hub(pa)
    update_dict(new_hub)

    if converged == False:
        flag += 1
    else :
        flag = 0
    converged = (isnotconverged(new_auth, auth_dict)) or (isnotconverged(new_hub, hub_dict))
    auth_dict = new_auth
    hub_dict = new_hub



print_auth(auth_dict)
print_hub(hub_dict)



    # new_auth_convergance = calculate_convergance(new_auth)
    # new_hub_convergance = calculate_convergance(new_hub)
    # auth_dict = dict(new_auth)
    # hub_dict = dict(hub_dict)
    # print new_hub_convergance
    # print new_auth_convergance
    # if get_unit_value(old_auth_convergance) == get_unit_value(new_auth_convergance) and \
    #                 get_unit_value(old_hub_convergance) == get_unit_value(new_hub_convergance):
    #     flag += 1
    #     old_auth_convergance = new_auth_convergance
    #     old_hub_convergance = new_hub_convergance
    #     if flag == 4:
    #         converged = True
    #         print_auth(new_auth)
    #         print_hub(new_hub)
    # else:
    #     flag = 0
    #     old_auth_convergance = new_auth_convergance
    #     old_hub_convergance = new_hub_convergance
