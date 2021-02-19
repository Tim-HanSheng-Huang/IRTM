#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


import numpy as np

N=1096 #should be 1096
C=np.zeros((N,N))

for n in range(1,N):
    for i in range(1,N):
        C[n,i]=cosine(n,i)
    print(n)


# In[3]:


def HAC(N,cluster_num,C):
    I=np.ones(N)
    I[0]=0
    c=np.copy(C)
    i=0
    m=0
    A=[]
    A.append([-1,-1])
    
    for k in range(1,N-cluster_num):
        current_max=0
        for p in range(1,N): 
            for q in range(1,N): 
                if(p!=q and I[p]==1 and I[q]==1 and c[p,q]>current_max):
                    i=p
                    m=q
                    current_max=c[p,q]
        item=[i,m]
        A.append(item)
        for j in range(1,N): 
            updatevalue=min(c[i,j],c[m,j])
            c[i,j]=updatevalue
            c[j,i]=updatevalue
        I[m]=0

    cluster=[]
    cluster.append(set())

    for i in range(1,N):
        temp_set=set()
        temp_set.add(i)
        cluster.append(temp_set)

    for i in range(1,N-cluster_num):
        small=A[i][0]
        big=A[i][1]
        cluster[small]=cluster[small].union(cluster[big])
        cluster[big]=set()

    returncluster=[]
    for i in range(len(I)):
        if(I[i]==1):
            cluster[i]=sorted(cluster[i], key=int)
            returncluster.append(cluster[i])
    
    return returncluster


# In[4]:


##### MAIN #####
c_8=np.copy(C)
c_13=np.copy(C)
c_20=np.copy(C)

cluster_num=8
eight_cluster=HAC(N,cluster_num,c_8)
print(eight_cluster)
with open("8.txt", 'w') as output:
    for i in range(len(eight_cluster)):
        for j in range(len(eight_cluster[i])):
            output.write(str(eight_cluster[i][j]) + '\n')
        output.write('\n')

cluster_num=13
thirteen_cluster=HAC(N,cluster_num,c_13)
print(thirteen_cluster)
with open("13.txt", 'w') as output:
    for i in range(len(thirteen_cluster)):
        for j in range(len(thirteen_cluster[i])):
            output.write(str(thirteen_cluster[i][j]) + '\n')
        output.write('\n')

cluster_num=20
twenty_cluster=HAC(N,cluster_num,c_20)
print(twenty_cluster)
with open("20.txt", 'w') as output:
    for i in range(len(twenty_cluster)):
        for j in range(len(twenty_cluster[i])):
            output.write(str(twenty_cluster[i][j]) + '\n')
        output.write('\n')

