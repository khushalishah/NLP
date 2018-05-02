import sys, string, ast

translator = str.maketrans('', '', string.punctuation)
dict_features_cls1 = dict()
b_cls1 = 0
dict_features_cls2 = dict()
b_cls2 = 0
dict_words_in_line = dict()

#read model file
def readModel(fileName):
    global dict_features_cls1
    global dict_features_cls2
    fhand = open(fileName,encoding="utf8")
    i=0
    for line in fhand:
        line = line.rstrip('\n')
        if i == 0:
            b_cls1 = float(line)
            i += 1
        elif i == 1:
            dict_features_cls1 = ast.literal_eval(line)
            i += 1
        elif i == 2:
            b_cls2 = float(line)
            i += 1
        else:
            dict_features_cls2 = ast.literal_eval(line)

readModel(sys.argv[1])

#read Test data
def readTestData():
    fhand = open(sys.argv[2],encoding="utf8")
    for line in fhand:
        words = line.split()
        temp = dict()
        for i in range(1,len(words)):
            word = words[i].lower().translate(translator).strip()
            if not word == "":
                if word in dict_features_cls1:
                    if word in temp:
                        temp[word] += 1
                    else:
                        temp[word] = 1
        dict_words_in_line[words[0]] = temp


#classify test data
def classify():
    fwrite = open("percepoutput.txt","w",encoding="utf8")
    for line in dict_words_in_line:
        dict_weight = dict_words_in_line[line]
        sum = b_cls1
        for word in dict_weight:
            sum += (dict_weight[word]*dict_features_cls1[word])
        if(sum<0):
            cls1 = 'Fake'
        else:
            cls1 = 'True'
        #classify for other class
        sum = b_cls2
        for word in dict_weight:
            sum += (dict_weight[word]*dict_features_cls2[word])
        if(sum<0):
            cls2 = 'Neg'
        else:
            cls2 = 'Pos'
        fwrite.write(line + " "+cls1+" "+cls2+"\n")
    fwrite.close()

readTestData()
classify()
