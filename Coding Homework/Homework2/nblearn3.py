import sys, string

#define all variables here
dict_tokens = dict()
total_pos = 0
total_neg = 0
total_fake = 0
total_true = 0
total_true_words = 0
total_fake_words = 0
total_pos_words = 0
total_neg_words = 0
count = 0
list_stopwords = list()
translator = str.maketrans('', '', string.punctuation)

#read stopwords file
fhand = open('stopwords.txt',encoding="utf8")
for line in fhand:
    list_stopwords.append(line.rstrip('\n'))

#read file
fhand = open(sys.argv[1],encoding="utf8")
for line in fhand:
    words = line.split()
    cls1 = words[1]
    if cls1 == 'Fake':
        total_fake += 1
    else:
        total_true += 1
    cls2 = words[2]
    if cls2 == 'Pos':
        total_pos += 1
    else:
        total_neg += 1
    #parse all words
    for i in range(3,len(words)):
        word = words[i].lower().translate(translator).strip()
        if not word == "":
            if word.isalpha():
                if not word in list_stopwords:
                    if word in dict_tokens:
                        dict_class = dict_tokens[word]
                    else:
                        dict_class = dict()
                        dict_class['Fake'] = 1
                        dict_class['True'] = 1
                        dict_class['Pos'] = 1
                        dict_class['Neg'] = 1
                    dict_class[cls1] += 1
                    dict_class[cls2] += 1
                    if cls1 == 'Fake':
                        total_fake_words += 1
                    else:
                        total_true_words += 1
                    if cls2 == 'Pos':
                        total_pos_words += 1
                    else:
                        total_neg_words += 1
                    dict_tokens[word] = dict_class
    count = count + 1

#prior probabilities
prior_pos = total_pos/(total_pos+total_neg)
prior_neg = total_neg/(total_pos+total_neg)
prior_fake = total_fake/(total_fake+total_true)
prior_true = total_true/(total_fake+total_true)

total_words = total_neg + total_pos

dict_temp = dict_tokens.copy()
#remove low frequency tokens
for token in dict_temp:
    sum = dict_tokens[token]['Fake'] + dict_tokens[token]['True'] + dict_tokens[token]['Pos'] + dict_tokens[token]['Neg']
    if sum <= 5:
        total_fake_words -= dict_tokens[token]['Fake']
        total_true_words -= dict_tokens[token]['True']
        total_pos_words -= dict_tokens[token]['Pos']
        total_neg_words -= dict_tokens[token]['Neg']
        del dict_tokens[token]

#probabilities of tokens
for token in dict_tokens:
    dict_class = dict_tokens[token]
    dict_class['True'] /= (total_true_words + len(dict_tokens))
    dict_class['Fake'] /= (total_fake_words + len(dict_tokens))
    dict_class['Pos'] /= (total_pos_words + len(dict_tokens))
    dict_class['Neg'] /= (total_neg_words + len(dict_tokens))
    dict_tokens[token] = dict_class

#write data to file
f = open("nbmodel.txt","w",encoding="utf8")
f.write(str(prior_fake)+"\n")
f.write(str(prior_true)+"\n")
f.write(str(prior_pos)+"\n")
f.write(str(prior_neg)+"\n")
f.write(str(dict_tokens))

print("Total Pos: "+str(total_pos))
print("Total Neg: "+str(total_neg))
print("Total Fake: "+str(total_fake))
print("Total True: "+str(total_true))
print("Total Words: "+str(len(dict_tokens)))
