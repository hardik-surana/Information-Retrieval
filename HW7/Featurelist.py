from __future__ import division
import operator

model_file = open("E:/IR/HW7/Part2/model_file.txt", 'r')
spam_file = open("E:/IR/HW7/Part2/spam_list.txt", 'r')
result_file = open("E:/IR/HW7/Part2/feature_list.txt", 'a')

word_dict = {}
feature_dict = {}
feature_list = []
i = 1

for line in spam_file.readlines():
    lst = line.rstrip('\n').split(" : ")
    word = str(lst[1])
    fid = int(lst[0])
    word_dict[fid] = word

for each in model_file.readlines():
    score = float(each.rstrip('\n'))
    term = word_dict[i]
    feature_dict[term] = score
    i += 1

sorted_dict = sorted(feature_dict.items(), key=operator.itemgetter(1), reverse=True)

for key in sorted_dict:
    result_file.write('%s : %f\n' % (key[0], key[1]))
