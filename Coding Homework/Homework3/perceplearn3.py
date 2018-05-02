import sys, string, math
import operator

list_stopwords = list()
dict_features = dict()
list_words_in_line = list()
translator = str.maketrans('', '', string.punctuation)
b = 0

#read stopwords file
def readStopWords():
    fhand = open('stopwords.txt',encoding="utf8")
    for line in fhand:
        list_stopwords.append(line.rstrip('\n'))

readStopWords()

#read file
def removeLowFrequencyWords():
    dict_total_words = dict()
    fhand = open(sys.argv[1],encoding="utf8")
    for line in fhand:
        temp = dict()
        words = line.split()
        for i in range(3,len(words)):
            word = words[i].lower().translate(translator).strip()
            if not word == "":
                if word.isalpha():
                    if not word in list_stopwords:
                        if word in dict_total_words:
                            dict_total_words[word] += 1
                        else:
                            dict_total_words[word] = 1
    count_of_words = math.ceil(len(dict_total_words)*0.1)
    newA = dict(sorted(dict_total_words.items(), key=operator.itemgetter(1), reverse=False)[:count_of_words])
    list_stopwords.extend(list(newA))
    newB = dict(sorted(dict_total_words.items(), key=operator.itemgetter(1), reverse=True)[:50])
    list_stopwords.extend(list(newB))

removeLowFrequencyWords()


#read training data
def readTrainingData():
    fhand = open(sys.argv[1],encoding="utf8")
    for line in fhand:
        temp = dict()
        words = line.split()
        for i in range(3,len(words)):
            word = words[i].lower().translate(translator).strip()
            if not word == "":
                if word.isalpha():
                    if not word in list_stopwords:
                        if word in temp:
                            temp[word] += 1
                        else:
                            temp[word] = 1
                        if not word in dict_features:
                            dict_features[word] = 0
        if words[1] == "Fake":
            temp['cls1'] = -1
        else:
            temp['cls1'] = 1
        if words[2] == 'Pos':
            temp['cls2'] = 1
        else:
            temp['cls2'] = -1
        list_words_in_line.append(temp)

readTrainingData()

#train vanilla model
def trainCLass(className):
    global b
    for i in range(0,29):
        for words_in_line in list_words_in_line:
            y = words_in_line[className]
            a = 0
            for word in words_in_line:
                if not (word == 'cls1' or word == 'cls2'):
                    a += (words_in_line[word] * dict_features[word])
            if (y*a) <= 0:
                #update weights and bias
                for word in words_in_line:
                    if not (word == 'cls1' or word == 'cls2'):
                        dict_features[word] = dict_features[word] + (y*words_in_line[word])
                b += y

def resetFeatures():
    global b
    b = 0
    #reset all weights to 0
    for word in dict_features:
        dict_features[word] = 0

#write model to file
def writeModel(fdict,mode,fileName):
    f = open(fileName,mode,encoding="utf8")
    f.write(str(b)+'\n')
    f.write(str(fdict)+'\n')
    f.close()

trainCLass('cls1')
writeModel(dict_features,"w","vanillamodel.txt")
resetFeatures()
trainCLass('cls2')
writeModel(dict_features,"a+","vanillamodel.txt")
resetFeatures()


#train average model data
def trainAvgModel(className):
    dict_cached_features = dict_features.copy()
    beta = 0
    c = 1
    global b
    for i in range(0,29):
        for words_in_line in list_words_in_line:
            y = words_in_line[className]
            a = 0
            for word in words_in_line:
                if not (word == 'cls1' or word == 'cls2'):
                    a += (words_in_line[word] * dict_features[word])
            if (y*a) <= 0:
                #update weights and bias
                for word in words_in_line:
                    if not (word == 'cls1' or word == 'cls2'):
                        dict_features[word] += (y*words_in_line[word])
                        dict_cached_features[word] += (y*c*words_in_line[word])
                b += y
                beta += (y*c)
            c += 1
    b -= (beta/c)
    for word in dict_features:
        dict_features[word] -= (dict_cached_features[word]/c)

trainAvgModel('cls1')
writeModel(dict_features,"w","averagedmodel.txt")
resetFeatures()
trainAvgModel('cls2')
writeModel(dict_features,"a+","averagedmodel.txt")

print(len(dict_features))
