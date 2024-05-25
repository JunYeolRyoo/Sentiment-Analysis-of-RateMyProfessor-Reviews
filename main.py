import nltk
from nltk import ConditionalFreqDist
from nltk.tokenize import word_tokenize
import math
from collections import defaultdict
from operator import itemgetter

def imp(sentence, trigrams, fds, sumitems):
    initialProb = []
    indexList = []
    for key in sumitems:
        initialProb.append(sumitems[key])
    
    for i in range(5):
        indexList.append(i)
    
    problist = []
    for i in indexList:
        problist.append([i,sumitems[fds[i]]])
        
    for ind in range(len(sentence)-2):
        w1,w2,w3 = sentence[ind],sentence[ind+1],sentence[ind+2]
        context = " ".join([w1,w2])
        for j in range(len(problist)):
            freq = trigrams[problist[j][0]][context].freq(w3)
            if freq > 0:
                problist[j][1] += math.log(freq) * 0.05
            else:
                problist[j][1] += math.log(0.00001) * 0.05  # Give penalty
    
    maxdiff = -9999  # Initialize maxdiff with negative infinity
    max_label = None

    for i in problist:
        if i[1] > maxdiff:
            maxdiff = i[1]
            max_label = fds[i[0]]
    return max_label
    
def trainNB(documents, classes):
    logprior = {}
    loglikelihood = {}
    vocab = set(word for _, doc in documents for word in doc)    # All words from 5 txt files without repetition
    bigdoc = defaultdict(list)
    N_doc = len(documents)
    
    for c in classes:
        N_c = sum(1 for doc_class, _ in documents if doc_class == c)
        logprior[c] = math.log(N_c / N_doc)     # Calculate log prior
        bigdoc[c] = [word for doc_class, doc in documents if doc_class == c for word in doc]    # Store all words occured in the doc c
        denom = sum(bigdoc[c].count(w) + 1 for w in vocab)  # Compute log likelihood for each word in vocabulary given class c

        for word in vocab:
            num = bigdoc[c].count(word) + 1
            loglikelihood[(word, c)] = math.log(num / denom)
    
    return logprior, loglikelihood, vocab

def testNB(testdoc, logprior, loglikelihood, classes, vocab):
    sums = {}
    for c in classes:
        sums[c] = logprior[c]
        for word in testdoc:
            if word in vocab:
                sums[c] += loglikelihood[(word,c)]
    return sorted(sums.items(), key=itemgetter(1), reverse = True)[0][0],sums

files = {"oneRate": open("trainingData/oneRate.txt","r"),
         "twoRate": open("trainingData/twoRate.txt","r"),
         "threeRate": open("trainingData/threeRate.txt","r"),
         "fourRate": open("trainingData/fourRate.txt","r"),
         "fiveRate": open("trainingData/fiveRate.txt","r")
         }
docs =[]

for fd in files:
    for line in files[fd].readlines():
        line = line.lower()
        docs.append((fd,word_tokenize(line)))

trigrams = []
for i in range(5):
    trigrams.append(nltk.ConditionalFreqDist())

fds = ["oneRate","twoRate","threeRate","fourRate","fiveRate"]

for sentence in docs:
    cur = fds.index(sentence[0])
    sentence = sentence[1]
    cond1 = "<s>"
    cond2 = "<s>"
    for word in sentence:
        context = " ".join([cond1,cond2])
        trigrams[cur][context][word] += 1
        cond1 = cond2
        cond2 = word

classes = ['oneRate','twoRate','threeRate','fourRate','fiveRate']

print("----------------------Start training--------------------------------")
priors, likelihood, vocab = trainNB(docs, classes)
print("----------------------Finished training--------------------------------")


testdata ={"oneRate": open("testData/1.txt","r"), 
            "twoRate":open("testData/2.txt","r"),
           "threeRate":open("testData/3.txt","r"), 
           "fourRate":open("testData/4.txt","r"), 
           "fiveRate":open("testData/5.txt","r")} 

overallAccuracy = 0

for fd in testdata:
    correct,incorrect,one,two,three,four,five = 0,0,0,0,0,0,0
    for line in testdata[fd].readlines():
        test = word_tokenize(line.lower())
        label,sumItem = testNB(test, priors, likelihood, classes, vocab)

        label = imp(test,trigrams,fds,sumItem)  # Apply trigram frequency distribution based on predicted label from classifier
        if label == fd:
            correct += 1
        else:
            incorrect += 1
            if label == "oneRate": one += 1
            elif label == "twoRate": two += 1
            elif label == "threeRate": three += 1
            elif label == "fourRate": four += 1
            else: five += 1
    overallAccuracy += correct/(correct+incorrect)
    print("Analysis for {}.txt".format(fd))
    print("Correct Assumption: {}\nIncorrect Assumption: {}".format(correct,incorrect))
    print("Accuracy: {}".format(correct/(correct+incorrect)))
    print("one:{} two:{} three:{} four:{} five:{}".format(one,two,three,four,five))
    print()

print("Overall accuracy of the classifier: {}".format(overallAccuracy/len(testdata.keys())))

for fd in testdata:
    testdata[fd].close()

for fd in files:
    files[fd].close()