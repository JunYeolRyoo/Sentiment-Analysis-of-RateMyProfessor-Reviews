import nltk
from nltk import ConditionalFreqDist
from nltk.tokenize import word_tokenize
import random

tri = nltk.ConditionalFreqDist()

docs =[]
originalList = []
indexList = []

fd = open("1.txt","r+")

numofNocom = 0
for line in fd.readlines():
    if line == "No Comments\n":
        numofNocom += 1
        continue
    originalList.append(line)   # Append original string to list
    line = line.strip().lower()
    docs.append(word_tokenize(line))    # Append lowered string to docs

fd.seek(0)

for sentence in docs:
    cond1 = "<s>"
    cond2 = "<s>"
    for word in sentence:
        context = " ".join([cond1,cond2])
        tri[context][word] += 1
        cond1 = cond2
        cond2 = word
    
totalcount = 0
score = 0
prolist = []
sentInd = 0
MaxScore = 0
for sentence in docs:
    if len(sentence) in [0,1,2]:
        sentInd += 1
        continue
    for ind in range(len(sentence)-2):
        try:
            w1,w2,w3 = sentence[ind],sentence[ind+1],sentence[ind+2]
            context = " ".join([w1,w2])
            result = tri[context].most_common()

            for wordTuple in result:
                if wordTuple[0] == w3:
                    score += wordTuple[1]
                    break                    
        except:
            break

    scoreperlength = score / len(sentence)
    if MaxScore < scoreperlength: MaxScore = scoreperlength

    if (scoreperlength > 20.2928 and scoreperlength < 36.2928) :
        indexList.append(sentInd)
        totalcount += 1
    if score != 0:      
        prolist.append((score,len(sentence),score/len(sentence)))
    sentInd += 1
    score = 0
        
total_score = 0
for i in prolist:
    total_score += i[2]
print(total_score/len(prolist))

fd.close()

### fd2 = open("TrainingDataV2/oneRate.txt","w")
### fd3 = open("collectedData/1_1.txt","w")
### fd = open("1.txt","w")
### num,num2,curInd = 0,0,0

### for sent in originalList:
###     if curInd in indexList and num < 5000:
###         fd2.write(sent)
###         num += 1
###     elif num2 < 500:
###         if random.randint(1,3) > 2:
###             fd.write(sent)
###             num2 += 1
###     else:
###         fd3.write(sent)
###     curInd += 1

### fd2.close()
### fd3.close()
### fd.close()
