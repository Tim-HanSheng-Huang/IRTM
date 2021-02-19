#!/usr/bin/env python
# coding: utf-8

# In[1]:


def GenerateDF(extracted_result):
    unique_result=set(extracted_result) #make every item in the result unique   
    while len(unique_result) != 0:
        new=True
        item=unique_result.pop()
        for i in range (len(dictionary)):
            if dictionary[i][0]==item:
                dictionary[i][1]=dictionary[i][1]+1
                new=False
        if(new):
            term=[item,1]
            dictionary.append(term)


# In[2]:


def ExtractTerms(filenumber):
    # Read the Original file
    filepath="G:/IR/HW2_DL1026/IRTM/"+filenumber+".txt"
    f=open(filepath, mode='r')
    text = f.read()
    #print(text)
    f.close()

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


# In[3]:


import nltk
from pandas import DataFrame
from nltk.stem import PorterStemmer
#read the stopword list
f=open("stopwords.txt", mode='r')
stopwords = f.read()
f.close()

########## MAIN #############
dictionary=[] 

for i in range(1,1096):
    n=str(i)
    extracted_result=ExtractTerms(n)
    GenerateDF(extracted_result)

dictionary.sort(key=lambda k: k[0])

for i in range(len(dictionary)):
    dictionary[i].insert(0,i) #insert index column
    
#write to the file
with open("dictionary.txt", 'w') as output:
    for row in dictionary:
        output.write(str(row) + '\n')
f.close()


# In[4]:


import math

def tfidfgenerate(filenumber):
    TF=[]
    extracted_result=ExtractTerms(filenumber)
    
    for i in range(len(extracted_result)):
        new=True
        for j in range (len(TF)):
            if TF[j][0]==extracted_result[i]:
                TF[j][1]=TF[j][1]+1
                new=False
        if(new):
            term=[extracted_result[i],1]
            TF.append(term)
    
    TF.sort(key=lambda k: k[0])
    
    TFIDF=[]
    for i in range(len(TF)):
        for j in range(len(dictionary)):
            if TF[i][0]==dictionary[j][1]:
                idf=math.log10(1095/int(dictionary[j][2]))
                tfidf=idf*TF[i][1]
                item=[dictionary[j][0],dictionary[j][1],tfidf]
                TFIDF.append(item)

    
    filepath="G:/IR/HW2_DL1026/TFIDF/"+"doc"+filenumber+".txt"
    with open(filepath, 'w') as output:
        for row in TFIDF:
            output.write(str(row) + '\n')
            #output.writelines(str(row))
        
###### MAIN ########    
for i in range(1,1096):
    n=str(i)
    TF=tfidfgenerate(n)


# In[5]:


def cosine(docx,docy):
    filepathX="G:/IR/HW2_DL1026/TFIDF/"+"doc"+str(docx)+".txt"
    filepathY="G:/IR/HW2_DL1026/TFIDF/"+"doc"+str(docy)+".txt"
    X_List=[]
    Y_List=[]
    
    f=open(filepathX,'r')
    nextline=True
    while(nextline):
        read_item=f.readline()
        if(read_item):
            read_item=read_item.replace("[","")
            read_item=read_item.replace("]","")
            read_item=read_item.replace("'","")
            read_item=read_item.split(", ")
            item=[int(read_item[0]),read_item[1],float(read_item[2])]
            X_List.append(item)
        else:
            nextline=False
            
    
    f=open(filepathY,'r')
    nextline=True
    while(nextline):
        read_item=f.readline()
        if(read_item):
            read_item=read_item.replace("[","")
            read_item=read_item.replace("]","")
            read_item=read_item.replace("'","")
            read_item=read_item.split(", ")
            item=[int(read_item[0]),read_item[1],float(read_item[2])]
            Y_List.append(item)
        else:
            nextline=False

    
    X_distance=0
    Y_distance=0
    for i in range(len(X_List)):
        X_distance=X_distance+X_List[i][2]**2
    for i in range(len(Y_List)):
        Y_distance=Y_distance+Y_List[i][2]**2
    
    X_distance=X_distance**(1/2)
    Y_distance=Y_distance**(1/2)
    
    for i in range(len(X_List)):
        X_List[i][2]=X_List[i][2]/X_distance
    for i in range(len(Y_List)):
        Y_List[i][2]=Y_List[i][2]/Y_distance
    
    similarity=0
    for i in range(len(X_List)):
        for j in range(len(Y_List)):
            if X_List[i][0]==Y_List[j][0]:
                similarity=similarity+X_List[i][2]*Y_List[j][2]
                
    return similarity

######### MAIN ############
DocX=1
DocY=2
similarity=cosine(DocX,DocY)
print("Cosine Similarity of Document",DocX,"& Document",DocY,":",similarity)

