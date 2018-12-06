#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 16:35:08 2018

@author: joeldavidson
"""

import random
import matplotlib.pyplot as plt
from collections import defaultdict as dic

#create a dictionary as the adjacency list
G = dic(list)

'''
BFS is a function that takes adjacency list G and vertices s and t
and returns pair d (distance s to t), and k (number of nodes popped off)
'''

#4.a

def BFS(G,s,t):
    Q = [] # queue of vertices
    Q.append(s)
    
    #create a list of length of all elements and keys in G
    visited = [0] * (sum([len(v)+1 for k, v in G.items()]))
    #visited[s] = 1
    k = 0
    
    dist = [0] * len(visited)
    if s == t:
        return(0,0)
    while Q:
        s = Q.pop(0)
        k +=1
        
        for i in G[s]:
            if visited[i] == 0:
                dist[i] = dist[s] + 1
                Q.append(i)
                visited[i] = 1
                if i == t:
                    return(dist[i],k)
    return(0,0)







#4.b

def BiBFS(G,s,t):
    Q_s = [] # queue of vertices
    Q_s.append(s)
    Q_t = [] 
    Q_t.append(t)
    
    #create two lists of length of all elements and keys in G + 10 so it is long enough
    visited_s = [False] * (sum([len(v)+1 for k, v in G.items()])+10)
    visited_s[s] = True
    visited_t = [False] * (sum([len(v)+1 for k, v in G.items()])+10)
    visited_t[t] = True
    k = 0
    
    
    dist_s = [0] * len(visited_s)
    dist_t = [0] * len(visited_t)
    if s == t:
        return(0,0)
    
    while Q_s and Q_t:
        if Q_s:
            
            s = Q_s.pop(0)
            k +=1
        
            #check all the vertices connected to s
            for i in G[s]:
                if visited_s[i] == False:
                    dist_s[i] = dist_s[s] + 1
                    Q_s.append(i)
                    visited_s[i] = True
                
                    #if the current vertex has been visited by the BFS from t, there is a path from s to t
                    if visited_t[i] == True:
                        return(dist_s[i]+dist_t[i],k)
        
        if Q_t:
            
            t = Q_t.pop(0)
            k += 1
        
            for j in G[t]:
                if visited_t[j] == False:
                    dist_t[j] = dist_t[t] + 1
                    Q_t.append(j)
                    visited_t[j] = True
                
                    if visited_s[j] == True:
                        return(dist_s[j]+dist_t[j],k)
    #print("no path")
    return(0,0)


#input for testing
G[1].append(2)
G[2].append(1)
G[1].append(3)
G[3].append(1)
G[2].append(4)
G[4].append(2)
G[2].append(5)
G[5].append(2)
G[3].append(6)
G[6].append(3)
G[3].append(7)
G[7].append(3)
G[7].append(8)
G[8].append(7)

print("BFS test: ", BFS(G,1,8))
print("BiBFS test: ",BiBFS(G,1,8))




#4.c.ii

#function to create a binary tree of height n
def BinTreeBuilder(n):
    nodes = (2**(n-1))-1
    BT = dic(list)
    for i in range(1,nodes+1):
        #add the connection to the graph in both directions so it is an undirected graph
        BT[i].append(i*2)
        BT[i*2].append(i)
        BT[i].append((i*2)+1)
        BT[(i*2)+1].append(i)
    return BT





K1List = []
D1List = []
K2List = []
D2List = []
nList = []
for i in range(3,16):
    BT = BinTreeBuilder(i)
    
    x,y = BFS(BT,1,len(BT))
    nList.append(i)
    D1List.append(x)
    K1List.append(y)
    
    q,r = BiBFS(BT,1,len(BT))
    D2List.append(q)
    K2List.append(r)
          
            
'''         
print("This is k1", K1List)
print("This is d1", D1List)
print("This is k2", K2List)
print("This is d2", D2List)
'''



ax = plt.subplot()
ax.set(xlabel='n', ylabel='k', title='Binary Tree')
plt.plot(nList, K1List)
plt.plot(nList, K2List)
plt.show()


#4.c.iii
def RandGraphBuilder(n):
    #create a 2d list to keep track of vertices already visited
    Rvisited = [0] * n
    for i in range(n):
        Rvisited[i] = [0] * n
    #G is the dictionary that is the adjacency list
    G = dic(list)
    for i in range (0,n):
        for j in range (0,n):
            if not Rvisited[i][j] and not Rvisited[j][i]:
                Rvisited[i][j] = 1
                Rvisited[j][i] = 1
                e = random.randint(0, 1)
                if e:
                    G[i].append(j)
                    G[j].append(i)
    return G
    
print("This is the d and k value for BFS on the random graph w/ n = 20", RandGraphBuilder(20))
print(BFS(RandGraphBuilder(20),1,2))

print("This is the d and k value for Bi-directional BFS on the random graph w/ n = 20")
print(BiBFS(RandGraphBuilder(20),1,2))


RandK1 = []
RandK2 = []
RandD1 = []
RandD2 = []
Randn = []

#run the test n = {3,4...20} 50 times and take the average k results
for n in range(3,20):
    xavg = 0
    yavg = 0
    qavg = 0
    ravg = 0
    Randn.append(n)
    for i in range(0,50):
        RG = RandGraphBuilder(n)
        x,y = BFS(RG,1,2)
        
        q,r = BiBFS(RG,1,2)
        
        xavg += x
        yavg += y
        qavg += q
        ravg += r
        
    RandD1.append(xavg/50)
    RandK1.append(yavg/50)
    RandD2.append(qavg/50)
    RandK2.append(ravg/50)

ax = plt.subplot()
ax.set(xlabel='n', ylabel='k', title='Random Graph')
plt.plot(Randn, RandK1)
plt.plot(Randn, RandK2)
plt.show()


