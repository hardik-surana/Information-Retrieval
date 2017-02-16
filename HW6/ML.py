from __future__ import division

global_qrel_dict = {}
global_doc_list = []
qrel_file = open("E:/IR/Data/AP_DATA/qrels.adhoc.51-100.AP89.txt", 'r')
global_oakapi = {}
global_tfidf = {}
global_bm25 = {}
global_laplase = {}
global_jm = {}
training_set_dict = {}
test_set_dict = {}
okapi_file = open('E:/IR/HW1Results/okapitf_model.txt', 'r')
tfidf_file = open('E:/IR/HW1Results/tfidf_model.txt', 'r')
bm25_file = open('E:/IR/HW1Results/okapi_bm25_model.txt', 'r')
laplase_file = open('E:/IR/HW1Results/laplase_model.txt', 'r')
jm_file = open('E:/IR/HW1Results/jm_model.txt', 'r')
catalog = open('E:/IR/HW6/testing_catalog.txt', 'a')
matrix_file = open('E:/IR/HW6/testing_matrix.txt', 'a')
line_number = 1


def print_matrix(okapi, bm, tfidf, laplace, jm, doctuple, qid):
    global line_number
    matrix_file.write('%s ' % doctuple[1])
    if okapi > 0:
        matrix_file.write('1:%s ' % okapi)
    if bm > 0:
        matrix_file.write('2:%s ' % bm)
    if tfidf > 0:
        matrix_file.write('3:%s ' % tfidf)
    if laplace > 0:
        matrix_file.write('4:%s ' % laplace)
    if jm > 0:
        matrix_file.write('5:%s' % jm)
    matrix_file.write('\n')
    catalog.write('%d %s %s\n' % (line_number, qid, doctuple[0]))
    line_number += 1


for line in qrel_file.readlines():
    list = line.split(' ')
    qid = list[0].strip()
    docid = list[2]
    rank = int(list[3].strip('\n'))
    if not global_doc_list.__contains__(docid):
        global_doc_list.append(docid)
    if not global_qrel_dict.__contains__(qid):
        global_qrel_dict[qid] = [(docid, rank)]
    else:
        global_qrel_dict[qid].append((docid, rank))

for okapi in okapi_file.readlines():
    ol = okapi.strip('\n').split(' ')
    a = ol[0]
    b = ol[2]
    c = ol[4]
    if global_doc_list.__contains__(b):
        if not global_oakapi.__contains__(a):
            global_oakapi[a] = [(b, c)]
        else:
            global_oakapi[a].append((b, c))

for tfdf in tfidf_file.readlines():
    tf = tfdf.strip('\n').split(' ')
    d = tf[0]
    e = tf[2]
    f = tf[4]
    if global_doc_list.__contains__(e):
        if not global_tfidf.__contains__(d):
            global_tfidf[d] = [(e, f)]
        else:
            global_tfidf[d].append((e, f))

for bm25 in bm25_file.readlines():
    bm = bm25.strip('\n').split(' ')
    g = bm[0]
    h = bm[2]
    i = bm[4]
    if global_doc_list.__contains__(h):
        if not global_bm25.__contains__(g):
            global_bm25[g] = [(h, i)]
        else:
            global_bm25[g].append((h, i))

for laplase in laplase_file.readlines():
    lp = laplase.strip('\n').split(' ')
    j = lp[0]
    k = lp[2]
    l = lp[4]
    if global_doc_list.__contains__(k):
        if not global_laplase.__contains__(j):
            global_laplase[j] = [(k, l)]
        else:
            global_laplase[j].append((k, l))

for jms in jm_file.readlines():
    jm = jms.strip('\n').split(' ')
    m = jm[0]
    n = jm[2]
    o = jm[4]
    if global_doc_list.__contains__(n):
        if not global_jm.__contains__(m):
            global_jm[m] = [(n, o)]
        else:
            global_jm[m].append((n, o))

testing_queries = ['54', '63', '80', '89', '97']

for key in global_oakapi.keys():
    if key in testing_queries:
        okapilist = global_oakapi[key]
        bmlist = global_bm25[key]
        tflist = global_tfidf[key]
        laplacelist = global_laplase[key]
        jmlist = global_jm[key]
        for item in global_qrel_dict[key]:
            okp = [okpdoc for okpdoc in okapilist if item[0] in okpdoc]
            if okp:
                okapi_score = okp[0][1]
            else:
                okapi_score = okapilist[-1][1]
            bm = [bmdoc for bmdoc in bmlist if item[0] in bmdoc]
            if bm:
                bm25_score = bm[0][1]
            else:
                bm25_score = bmlist[-1][1]
            tf = [tfdoc for tfdoc in tflist if item[0] in tfdoc]
            if tf:
                tf_score = tf[0][1]
            else:
                tf_score = tflist[-1][1]
            lap = [lapdoc for lapdoc in laplacelist if item[0] in lapdoc]
            if lap:
                laplace_score = lap[0][1]
            else:
                laplace_score = laplacelist[-1][1]
            jm = [jmdoc for jmdoc in jmlist if item[0] in jmdoc]
            if jm:
                jm_score = jm[0][1]
            else:
                jm_score = jmlist[-1][1]
            # if (okapi_score > 0 or bm25_score > 0 or tf_score > 0 or laplace_score > 0 or jm_score > 0):
            print_matrix(okapi_score, bm25_score, tf_score, laplace_score, jm_score, item, key)
catalog.close()
matrix_file.close()
