from itertools import izip

cataloge_file = open('E:/IR/HW6/testing_catalog.txt', 'r')
prediction_file = open('E:/IR/HW6/Test_out.txt', 'r')
output_file = open('E:/IR/HW6/RankList_testing.txt', 'a')

# for line, ln in cataloge_file.readlines(), prediction_file.readlines():
#     list = line.strip('\n').split(' ')
#     serial = list[0]
#     qid = list[1]
#     docid = list[2]
#     lt = ln.strip('\n').split(' ')
#     score = lt[2]

with cataloge_file as f1, prediction_file as f2:
    for x, y in zip(f1, f2):
        list1 = x.strip('\n').split(' ')
        list2 = y.strip('\n').split(' ')
        serial = int(list1[0])
        qid = str(list1[1])
        docid = str(list1[2])
        score = float(list2[2])
        output_file.write('%s Q0 %s %d %f Exp \n' % (qid, docid, serial, score))