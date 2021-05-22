# -*- coding: utf-8 -*-
"""
Created on Wed May 19 00:17:36 2021

@author: Shahrukh
"""

import networkx as nx
import matplotlib.pyplot as plt 

import random as r

import numpy as np
import docplex
from docplex.mp.model import Model


def Generate_CM(no_of_nodes):
    '''
    no_of_nodes: Number of nodes in the graph

    '''
    #x=np.random.randint(20,60,size=(no_of_nodes,no_of_nodes))
    #np.fill_diagonal(x, 0)
    x=np.array([[0,23,424,38,692],
                 [423,0,45,65,198],
                 [76,98,0,654,54],
                 [65,87,985,0,293],
                 [64,56,98,23,0]])
    '''
    -The Matrix represent the graph where x(i,j) represent the cost of going from point i to j 
    in the graph 
    -This is example Matrix where x(i, j)  is cost of going from i to j
    -This Matrix represent a bidirectional graph
    '''
    #x[0,4]=290
    return x

sr=Model(name='Shortest Route')
nn=5  #number of nodes
nodes=range(1,nn+1); #range from 1 to nn
x=sr.binary_var_matrix(keys1=nodes,keys2=nodes,name="x_%s_%s")   
# binary variable x if x(i,j) is part of shortest route, else 0
starting_node=1
ln=5
# can go to any point from starting point
start=sr.add_constraint(sum(x[starting_node,i] for i in range(1,nn+1) if i != starting_node)==1)
#can come from any point to the last point  
end=sr.add_constraint(sum(x[i,ln] for i in range(1,nn+1) if i != ln)==1)           
#for all the nodes except start and last node
#there should be incoming as well as outgoing edge
cts=[]
# for i in range(1,nn+1):
#     if (i!= starting_node and i!=ln):
s=sr.add_constraints(-sum(x[j,i] for j in range(1,nn+1))
                    +sum(x[i,j] for j in range(1,nn+1) )==0
                    for i in range(1,nn+1)
                    if (i!= starting_node and i!=ln))
#no_self _connection_possible
q=sr.add_constraints((x[i,i])==0 for i in range(1,nn+1))
# Only single node is connected from any node 
p=sr.add_constraints(sum(x[i,j] for j in range(1,nn+1))<=1 for i in range(1,nn+1))
costs=Generate_CM(nn)             

sr.minimize(sr.sum(x[i,j]*costs[i-1,j-1] for i in range(1,nn+1) for j in range(1,nn+1)))   

sol=sr.solve()


solution=[]
for i in nodes :
    for j in nodes:
        solution.append(sol.get_value(x[i,j]))
solution=np.array(solution)
solution=solution.reshape(nn,nn)

for i in range(0,nn):
    for j in range(0,nn):
        if(solution[i,j]==1):
           print('The following edge (',i+1,',',j+1,') is  connected')