import sys
import ast
import math, string

prior_neg = 0
prior_pos = 0
prior_fake = 0
prior_true = 0
dict_tokens = dict()
translator = str.maketrans('', '', string.punctuation)

#read nbmodel.txt file
fhand = open("nbmodel.txt",encoding="utf8")
i=0
for line in fhand:
    if i == 0:
        prior_fake = float(line)
        i += 1
    elif i == 1:
        prior_true = float(line)
        i += 1
    elif i == 2:
        prior_pos = float(line)
        i += 1
    elif i == 3:
        prior_neg = float(line)
        i += 4
    else:
        dict_tokens = ast.literal_eval(line)

#read development file
fhand = open(sys.argv[1],encoding="utf8")
fwrite = open("nboutput.txt","w",encoding="utf8")
count = 0
for line in fhand:
    words = line.split()
    con_prob_pos = 0
    con_prob_neg = 0
    con_prob_fake = 0
    con_prob_true = 0
    for i in range(1,len(words)):
        word = words[i].lower().translate(translator).strip()
        if not word == "":
            if word in dict_tokens:
                con_prob_pos += math.log(float(dict_tokens[word]['Pos']))
                con_prob_neg += math.log(float(dict_tokens[word]['Neg']))
                con_prob_fake += math.log(float(dict_tokens[word]['Fake']))
                con_prob_true += math.log(float(dict_tokens[word]['True']))
    con_prob_pos += math.log(prior_pos)
    con_prob_neg += math.log(prior_neg)
    con_prob_fake += math.log(prior_fake)
    con_prob_true += math.log(prior_true)
    if con_prob_pos>con_prob_neg:
        cls1 = "Pos"
    else:
        cls1 = "Neg"
    if con_prob_true>con_prob_fake:
        cls2 = "True"
    else:
        cls2 = "Fake"
    fwrite.write(words[0]+" "+cls2+" "+cls1+"\n")
fwrite.close()
