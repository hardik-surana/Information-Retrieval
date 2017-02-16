from itertools import izip
import operator

output_file = open("E:/IR/HW7/Part2/ranklist_test.txt", 'a')
output_dict = {}
i = 1

with open("E:/IR/HW7/Part2/result_test.txt", 'r') as textfile1, open("E:/IR/HW7/Part2/test_catalog.txt", 'r') as textfile2:
    for x, y in izip(textfile1, textfile2):
        lx = x.strip('\n').split(' ')
        ly = y.strip('\n').split(' ')
        docid = ly[1]
        score = float(lx[2])
        output_dict[docid] = score

sorted_dict = sorted(output_dict.items(), key=operator.itemgetter(1), reverse=True)[:1000]

for key in sorted_dict:
    output_file.write('%s %f\n' % (key[0], key[1]))
