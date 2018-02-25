import sys
import ast

count = 0
dict_trans = dict()
dict_emmi = dict()
dict_start = dict()
dict_total_tag_cnt = dict()
tag_high = list()
list_sentences = list()
#function to get highest starting tag
def getHighestTagList():
    if len(tag_high)==0:
        #put 5 highest used tag in list
        dict_temp = dict_total_tag_cnt.copy()
        n=0
        while n<2:
            #get highest used tag from list
            max = 0
            final_tag = ""
            for tag in dict_temp:
                compare = int(str(dict_temp[tag]))
                if max<compare:
                    max = dict_temp[tag]
                    final_tag = tag
            tag_high.append(final_tag)
            del dict_temp[final_tag]
            n += 1
    return tag_high
#read all probabilties from hmmmodel file
fhand = open('hmmmodel.txt',encoding="utf8")
i=1
for line in fhand:
    if i==1:
        dict_trans = ast.literal_eval(line)
        i += 1
    elif i==2:
        dict_emmi = ast.literal_eval(line)
        i += 1
    elif i==3:
        dict_start = ast.literal_eval(line)
        i += 1
    else:
        dict_total_tag_cnt = ast.literal_eval(line)

fhand = open(sys.argv[1],encoding="utf8")
for line in fhand:
    count += 1
    if count == 10:
        break
    list_hmmmodel = []
    #get words list
    words = line.split()
    for i in range(len(words)):
        word = words[i]
        dict_temp = dict()
        if not word in dict_emmi:
            tags = getHighestTagList()
            print("Unseen word: "+word)
            #handle unseen data
            if i==0:
                #handle if unknown word is in starting
                for t in tags:
                    if not t in dict_start:
                        dict_start[t] = 1/dict_start['totalCnt']
                    start_prob = dict_start[t]
                    dict_temp1 = dict()
                    dict_temp1['prob'] = start_prob
                    dict_temp1['prev'] = 'q0'
                    dict_temp[t] = dict_temp1
            else:
                for t in tags:
                    prev_tags = list_hmmmodel[i-1];
                    max_prob = 0
                    dict_temp1 = dict()
                    for prev_state in prev_tags:
                        dict_trans_tag = dict_trans[prev_state]
                        if not t in dict_trans_tag:
                            dict_trans_tag[t] = 1/dict_trans_tag['totalCnt']
                        prob = prev_tags[prev_state]['prob'] * dict_trans_tag[t]
                        if max_prob<prob:
                            max_prob = prob
                            dict_temp1['prob'] = prob
                            dict_temp1['prev'] = prev_state
                        dict_trans[prev_state] = dict_trans_tag
                    dict_temp[t] = dict_temp1

        else:
            tags = dict_emmi[word]
            #print("TAGS : "+str(tags))
            #for start probabilties
            if i==0:
                for t in tags:
                    if not t in dict_start:
                        dict_start[t] = 1/dict_start['totalCnt']
                    start_prob = dict_start[t] * tags[t]
                    dict_temp1 = dict()
                    dict_temp1['prob'] = start_prob
                    dict_temp1['prev'] = 'q0'
                    dict_temp[t] = dict_temp1
            else:
                for state in tags:
                    prev_tags = list_hmmmodel[i-1];
                    max_prob = 0
                    dict_temp1 = dict()
                    for prev_state in prev_tags:
                        dict_trans_tag = dict_trans[prev_state]
                        if not state in dict_trans_tag:
                            dict_trans_tag[state] = 1/dict_trans_tag['totalCnt']
                        prob = prev_tags[prev_state]['prob'] * tags[state] * dict_trans_tag[state]
                        if max_prob<prob:
                            max_prob = prob
                            dict_temp1['prob'] = prob
                            dict_temp1['prev'] = prev_state
                        dict_trans[prev_state] = dict_trans_tag
                    dict_temp[state] = dict_temp1

        list_hmmmodel.append(dict_temp)
        #print(list_hmmmodel)
        #trace path
    prev_state = ""
    for j, e in reversed(list(enumerate(list_hmmmodel))):

        current_state = ""
        if j == len(list_hmmmodel)-1:
            #find max probabilty
            max_prob = 0
            for t in e:
                if e[t]['prob']>max_prob:
                    max_prob = e[t]['prob']
                    prev_state = e[t]['prev']
                    current_state = t
        else:
            current_state = prev_state
            prev_state = e[prev_state]['prev']
        words[j] += "/"+current_state
    #make a sentence
    sentence = ""
    for word in words:
        sentence += word + " "
    list_sentences.append(sentence.strip())
#write sentences to file
f = open("hmmoutput.txt","w",encoding="utf8")
for sen in list_sentences:
    f.write(sen+"\n")
f.close()
