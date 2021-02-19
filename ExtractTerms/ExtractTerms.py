#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Read the Original file

f=open("text.txt", mode='r')
text = f.read()
print(text)
f.close()


# In[2]:


#lowercasing

lowertext=text.lower()
print(lowertext)


# In[3]:


#tokenization

pun_marks="~!@#$%^&*(-_+=){[]}|\:;''"",.<>?/"

for i in range(len(pun_marks)):
    lowertext=lowertext.replace(pun_marks[i]," ")

splitlowertext=lowertext.split()
print(splitlowertext)


# In[4]:


#Porter Stemming

import nltk
from nltk.stem import PorterStemmer
pstem=PorterStemmer()

def porterstemming(text):
    for i in range (len(text)):
        text[i]=pstem.stem(text[i])
    return text

stemsplitlowertext=porterstemming(splitlowertext)
print(stemsplitlowertext)


# In[5]:


#read the stopword list

f=open("stopwords.txt", mode='r')
stopwords = f.read()
#print(stopwords)
f.close()


# In[6]:


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
print(result)


# In[7]:


f = open('result.txt','w')
print(result, file = f)
f.close()

