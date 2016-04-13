import json
import nltk
import copy
from nltk.stem.wordnet import WordNetLemmatizer
from textblob import TextBlob
lmtzr = WordNetLemmatizer()
f = open("json/72572.json", 'r')
text = json.load(f)
joined_text = ''
for i in range(0, len(text['Reviews'])):
    joined_text = joined_text + ' \\ ' + text['Reviews'][i]['Content']
joined_text_words = nltk.word_tokenize(joined_text)
tagged_words = nltk.pos_tag(joined_text_words)
wanted_structure = []
description = ['','',0]
which_passage = 0
for i in range(0, len(tagged_words) - 2):
    noun_sing = noun_plu = be_sing = be_plu = 0
    noun_sing = (tagged_words[i][1] == 'NN')
    noun_plu = (tagged_words[i][1] == 'NNS')
    be_sing = (tagged_words[i+1][0] == 'is' or tagged_words[i+1][0] == 'was')
    be_plu = (tagged_words[i+1][0] == 'are' or tagged_words[i+1][0] == 'were')
    if (noun_sing and be_sing) or (noun_plu and be_plu):
        if tagged_words[i+2][1] == 'JJ':
            description[0] = lmtzr.lemmatize(tagged_words[i][0].lower())
            description[1] = tagged_words[i+2][0].lower()
            description[2] = copy.deepcopy(which_passage)
            wanted_structure.append(copy.deepcopy(description))
    if tagged_words[i][0] == '\\':
        which_passage += 1
#for i in range(0, len(wanted_structure)):
#    print (wanted_structure[i])

service_aspects = ['room', 'service', 'hotel','location','breakfast','meal','dinner','housekeeping','staff','price','view','bed']
verdict = {}
for i in range(0, len(wanted_structure)):
    if wanted_structure[i][0] in service_aspects:
        if wanted_structure[i][0] not in verdict:
            verdict[wanted_structure[i][0]] = {wanted_structure[i][1]:wanted_structure[i][2]}
        else:
            if wanted_structure[i][1] not in verdict[wanted_structure[i][0]]:
                verdict[wanted_structure[i][0]][wanted_structure[i][1]] = wanted_structure[i][2]
result_file = open('result.csv', 'w')
result_file.write('aspect,adjective,passage,sentiment\n')
for key_1 in verdict:
    for key_2 in verdict[key_1]:
        result_file.write('' + key_1 + ',' + key_2 + ',' + str(verdict[key_1][key_2]) + ',' + str(TextBlob(key_2).sentiment[0]) + '\n')
