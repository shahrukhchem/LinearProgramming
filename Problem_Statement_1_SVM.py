# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 20:13:14 2021

@author: Shahrukh
"""

import pandas as pd
import numpy as np

import docplex
from docplex.mp.model import Model


costmatrix=pd.read_csv('Optimisation Exercise.csv')

cm=np.array(costmatrix.iloc[:,1:len(costmatrix)+1])
cities=costmatrix.iloc[:,0]
N=len(cities)
m=Model(name='Shortest Route',log_output=True)
#binary_varialbe if salesman travel between city i & j 
x=m.binary_var_matrix(keys1=range(1,N+1),keys2=range(1,N+1),name="x_%s_%s")
#dummy Variable to eliminate sub-tour 
u=m.integer_var_list(keys=range(2,N+1),lb=1,ub=N-1,name="u_%s")

# a sales man arrive at a city from exactly one city 
cons1=m.add_constraints(sum(x[i,j]for i in range(1,N+1) if i!=j)==1 for j in range(1,N+1))

# salesman leave to exactly one city from a city
cons2=m.add_constraints(sum(x[i,j]for j in range(1,N+1) if j!=i)==1 for i in range(1,N+1))
# eliminating sub tours 
cons3=m.add_constraints(u[i]-u[j]+N*x[i+1,j+1]<=(N-1) for i in range(0,N-1) for j in range(0,N-1) if i!=j )
# minimize the cost (distance)
m.minimize(m.sum(x[i,j]*cm[i-1,j-1] for i in range(1,N+1) for j in range(1,N+1)) )  
sol=m.solve()
m.print_information()
#m.print_solution(print_zeros=False)

#solution.append(sol.get_value(x[i,j]))
solution=[]
         
for i in range(1,N+1):
    for j in range(1,N+1):
        
           solution.append(sol.get_value(x[i,j]))
           

solution=np.array(solution)
solution=solution.reshape(N,N)   

         
Index=cities[cities=='Berlin'].index[0]   #Getting Index of Barcelona
no_of_visit=0

while no_of_visit<24:
    for i in range(0,N):
     
        if(solution[Index,i]==1):
            print(cities[Index],'  =>  ',cities[i])
            no_of_visit=no_of_visit+1
            Index=i
            #print(Index)
            break;
            
print('Total Distance of Tour:', sol.get_objective_value() )        
          

           
