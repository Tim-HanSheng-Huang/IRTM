#!/usr/bin/env python
# coding: utf-8

# In[1]:


class1=[11, 19, 29, 113, 115, 169, 278, 301, 316, 317, 321, 324, 325, 338, 341]
class2=[1,2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16 ]
class3=[813, 817, 818, 819, 820, 821, 822, 824, 825, 826, 828, 829, 830, 832, 833]
class4=[635, 680, 683, 702, 704, 705, 706, 708, 709, 719, 720, 722, 723, 724, 726]
class5=[646, 751, 781, 794, 798, 799, 801, 812, 815, 823, 831, 839, 840, 841, 842]
class6=[995, 998, 999, 1003, 1005, 1006, 1007, 1009, 1011, 1012, 1013, 1014, 1015, 1016, 1019]
class7=[700, 730, 731, 732, 733, 735, 740, 744, 752, 754, 755, 756, 757, 759, 760]
class8=[262, 296, 304, 308, 337, 397, 401, 443, 445, 450, 466, 480, 513, 533, 534]
class9=[130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 145]
class10=[31, 44, 70, 83, 86, 92, 100, 102, 305, 309, 315, 320, 326, 327, 328,]
class11=[240, 241, 243, 244, 245, 248, 250, 254, 255, 256, 258, 260, 275, 279, 295]
class12=[535, 542, 571, 573, 574, 575, 576, 578, 581, 582, 583, 584, 585, 586, 588]
class13=[485, 520, 523, 526, 527, 529, 530, 531, 532, 536, 537, 538, 539, 540, 541]

allclass=[]
allclass.append(class1)
allclass.append(class2)
allclass.append(class3)
allclass.append(class4)
allclass.append(class5)
allclass.append(class6)
allclass.append(class7)
allclass.append(class8)
allclass.append(class9)
allclass.append(class10)
allclass.append(class11)
allclass.append(class12)
allclass.append(class13)


# In[2]:


f=open("dictionary.txt", mode='r')
dictionary_list=[]

nextline=True
while(nextline):
    read_item=f.readline()
    if(read_item):
        read_item=read_item.split("'")
        item=read_item[1]
        dictionary_list.append(item)
    else:
        nextline=False

#print(dictionary_list)


# In[3]:


import math
llrlist_classifier=[]

for current_classifier in range(1,14):
    #classXX classifier
    llr_list=[]
    for term in range(len(dictionary_list)):

        n11=0
        n10=0
        n01=0
        n00=0

        for i in range(1,14):
            if(i==current_classifier):
                #on topic
                for j in range(1,16):
                    filepath="G:/IR/HW3_DL1214/TFIDF/"+"doc"+str(allclass[i-1][j-1])+".txt"
                    f=open(filepath,'r')
                    content=f.read()
                    if dictionary_list[term] in content:
                        n11=n11+1
                    else:
                        n10=n10+1      
            else:
                #off topic
                for j in range(1,16):
                    filepath="G:/IR/HW3_DL1214/TFIDF/"+"doc"+str(allclass[i-1][j-1])+".txt"
                    f=open(filepath,'r')
                    content=f.read()
                    if dictionary_list[term] in content:
                        n01=n01+1
                    else:
                        n00=n00+1           

        N=n11+n10+n01+n00
        LH1=math.pow(((n11+n01)/N),n11)*math.pow((1-((n11+n01)/N)),n10)*math.pow(((n11+n01)/N),n01)*math.pow((1-((n11+n01)/N)),n00)
        LH2=math.pow((n11/(n11+n10)),n11)*math.pow((1-(n11/(n11+n10))),n10)*math.pow((n01/(n01+n00)),n01)*math.pow((1-(n01/(n01+n00))),n00)
        llr=(-2)*math.log(LH1/LH2)
        llr_list.append(llr)
        #print("TERM:",dictionary_list[term],"N11=",n11,"N10=",n10,"N01=",n01,"N00=",n00,"LLR=",llr)

    #print("classifier",current_classifier+1,"llr list:\n",llr_list)
    llrlist_classifier.append(llr_list)
    
    filepath="G:/IR/HW3_DL1214/"+"classifier"+str(current_classifier)+"llr"+".txt"
    with open(filepath, 'w') as output:
        for item in llr_list:
            output.write(str(item) + '\n')


# In[4]:


llrlist_classifier_sum=llrlist_classifier[0]

for i in range(1,14):
    for j in range(len(dictionary_list)):
        llrlist_classifier_sum[j]=llrlist_classifier_sum[j]+llrlist_classifier[i][j]

max500_index=[]
for i in range(500):
    index=llrlist_classifier_sum.index(max(llrlist_classifier_sum))
    max500_index.append(index)
    llrlist_classifier_sum[index]=0
    
print(max500_index)

classification_term=[]
for i in range(500):
    classification_term.append(dictionary_list[max500_index[i]])


# In[5]:


new500_dictionary_likelihood=sorted(classification_term)
new500_dictionary_likelihood

#write to the file
with open("new500_dictionary_likelihood.txt", 'w') as output:
    for row in new500_dictionary_likelihood:
        output.write(str(row) + '\n')
f.close()

count=0
#write to the file
with open("new500_likelihood_likelihood(with index)_dictionary.txt", 'w') as output:
    for row in new500_dictionary_likelihood:
        output.write(str(count)+'\t'+str(row) + '\n')
        count=count+1
f.close()


# In[6]:


f=open("new500_dictionary_likelihood.txt", mode='r')
new500_dictionary_likelihood=[]

nextline=True
while(nextline):
    read_item=f.readline()
    if(read_item):
        read_item=read_item.split("\n")
        item=read_item[0]
        new500_dictionary_likelihood.append(item)
    else:
        nextline=False

new500_dictionary_likelihood


# In[7]:


import nltk
from pandas import DataFrame
from nltk.stem import PorterStemmer
#read the stopword list
f=open("stopwords.txt", mode='r')
stopwords = f.read()
f.close()

def ExtractTerms(content):
    text = content

    #lowercasing
    lowertext=text.lower()
    #print(lowertext)

    #tokenization
    removed_marks="~!@#$%^&*(-_+=){[]}|\:;`\'\",.<>?/1234567890"
    for i in range(len(removed_marks)):
        lowertext=lowertext.replace(removed_marks[i]," ")
    splitlowertext=lowertext.split()
    #print(splitlowertext)

    #Porter Stemming
    pstem=PorterStemmer()
    def porterstemming(text):
        for i in range (len(text)):
            text[i]=pstem.stem(text[i])
        return text
    stemsplitlowertext=porterstemming(splitlowertext)
    #print(stemsplitlowertext)

    #stopwords removal
    def removestopwords(text):
        i=0
        while i!=(len(text)-1):
            if text[i] in stopwords:
                text.remove(text[i])
            else:
                i=i+1
        return text
    result=removestopwords(stemsplitlowertext)
    #print("\n",result)
    return result


# In[8]:


condprob_tc_allclass=[]

for i in range(1,14):#should be (1,14)
    condprob_tc=[]
    total_T_ct=0
    for t in range(len(new500_dictionary_likelihood)):#should be len(new500_dictionary_likelihood)
        T_ct=0
        for j in range(1,16):
            filepath="G:/IR/HW3_DL1214/IRTM/"+str(allclass[i-1][j-1])+".txt"
            f=open(filepath,'r')
            content=f.read()
            extracted_content=ExtractTerms(content)
            T_ct=T_ct+extracted_content.count(new500_dictionary_likelihood[t])
        total_T_ct=total_T_ct+T_ct
        condprob_tc.append(T_ct)
    for t in range(len(new500_dictionary_likelihood)):
        condprob_tc[t]=(condprob_tc[t]+1)/(total_T_ct+500)
    print(condprob_tc[1])
    condprob_tc_allclass.append(condprob_tc)


# In[9]:


test_doc=[]
for i in range(1,1096):
    test_doc.append(i)
       
test_doc=list(set(test_doc)-set(class1))
test_doc=list(set(test_doc)-set(class2))
test_doc=list(set(test_doc)-set(class3))
test_doc=list(set(test_doc)-set(class4))
test_doc=list(set(test_doc)-set(class5))
test_doc=list(set(test_doc)-set(class6))
test_doc=list(set(test_doc)-set(class7))
test_doc=list(set(test_doc)-set(class8))
test_doc=list(set(test_doc)-set(class9))
test_doc=list(set(test_doc)-set(class10))
test_doc=list(set(test_doc)-set(class11))
test_doc=list(set(test_doc)-set(class12))
test_doc=list(set(test_doc)-set(class13))

test_doc=sorted(test_doc)


# In[10]:


predict_alldoc=[]

for i in range(len(test_doc)):#should be len(test_doc)
    score_class=[]
    filepath="G:/IR/HW3_DL1214/IRTM/"+str(test_doc[i])+".txt" #這是第test_doc[i]的預測
    f=open(filepath,'r')
    content=f.read()
    extracted_content=ExtractTerms(content)
    for c in range(1,14):
        score=math.log(1/13)
        for t in range(len(new500_dictionary_likelihood)):
            score=score+extracted_content.count(new500_dictionary_likelihood[t])*math.log(condprob_tc_allclass[c-1][t])
        score_class.append(score)
    predicted_class=score_class.index(max(score_class))+1
    predict_alldoc.append(predicted_class)


# In[11]:


#write to the file
with open("prediction_likelihood.txt", 'w') as output:
    for row in predict_alldoc:
        output.write(str(row) + '\n')
f.close()

