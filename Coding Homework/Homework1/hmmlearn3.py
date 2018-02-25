import sys
fhand = open(sys.argv[1],encoding="utf8")
count = 0
dict_trans = dict()
dict_emmi = dict()
dict_start = dict()
dict_total_tag_cnt = dict()
for line in fhand:
    count = count + 1
    words = line.split()
    ##count starting probabilties
    start_tag = words[0].rsplit('/', 1)[-1];
    if start_tag in dict_start:
        dict_start[start_tag] += 1
    else:
        dict_start[start_tag] = 1
    for i in range(len(words)):
        w = words[i].rsplit('/', 1);
        word = w[0];
        tag = w[1];
        #add transion probabilties
        if i<len(words)-1:
            next_tag = words[i+1].rsplit('/',1)[1];
            if tag in dict_trans:
                dict_tag = dict_trans[tag]
            else:
                dict_tag = dict()
            if next_tag in dict_tag:
                dict_tag[next_tag] += 1
            else:
                dict_tag[next_tag] = 1
            if 'totalCnt' in dict_tag:
                dict_tag['totalCnt'] += 1
            else:
                dict_tag['totalCnt'] = 1
            dict_trans[tag] = dict_tag
            #add emission probabilties
            if word in dict_emmi:
                dict_word = dict_emmi[word]
            else:
                dict_word = dict()
            if tag in dict_word:
                dict_word[tag] += 1
            else:
                dict_word[tag] = 1
            if tag in dict_total_tag_cnt:
                dict_total_tag_cnt[tag] += 1
            else:
                dict_total_tag_cnt[tag] = 1
            dict_emmi[word] = dict_word
#divide emission probabilties with total count
for w in dict_emmi:
    dict_temp = dict_emmi[w]
    for t in dict_temp:
        dict_temp[t] = dict_temp[t]/dict_total_tag_cnt[t]
    dict_emmi[w] = dict_temp
#add-one smoothing in transition probabilties
total_tags = len(dict_total_tag_cnt)
for t in dict_trans:
    dict_temp = dict_trans[t]
    if not len(dict_temp)==total_tags+1:
        dict_temp['totalCnt'] += total_tags
        for t2 in dict_temp:
            if not t2 == 'totalCnt':
                dict_temp[t2] = (dict_temp[t2]+1)/dict_temp['totalCnt']
    dict_trans[t] = dict_temp

#add-one smoothing on starting probabilties
dict_start['totalCnt'] = count
if not len(dict_start)==total_tags+1:
    dict_start['totalCnt'] += total_tags
    for t2 in dict_start:
        if not t2 == 'totalCnt':
            dict_start[t2] = (dict_start[t2]+1)/dict_start['totalCnt']

#write dict to file
f = open("hmmmodel.txt","w",encoding="utf8")
f.write(str(dict_trans))
f.write("\n")
f.write(str(dict_emmi))
f.write("\n")
f.write(str(dict_start))
f.write("\n")
f.write(str(dict_total_tag_cnt))
f.close()
