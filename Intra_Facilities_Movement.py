# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:36:13 2021

@author: Shahrukh
"""

import pandas as pd
from docplex.mp.model import Model
import numpy as np


def create_dummy_data():
    '''
    cities -> Name of Cities
    cm-> cost of going from City i to City J
    Initial Inventory-> Inventpry avaialbe at city i before Intra-Site Movement
    Required Inventory -> Required Inventory at Site i  after Movement
    
    '''
    cities=['City1','City2','City3','City4','City5','City6']
    cm ={}
    for i in cities:
        for j in cities:
            if (i==j):
                cm[i,j]=0
            elif (j,i) in cm:
                cm[i,j]=cm[j,i]            
            else:
                cm[i,j]=np.random.randint(50,100)
    Initial_Inventory={'City1':np.random.randint(50,60),
                       'City2':np.random.randint(50,60),
                       'City3':np.random.randint(50,60), 
                        'City4':np.random.randint(50,60),
                        'City5':np.random.randint(50,60),
                        'City6':30
                            #np.random.randint(50,60),
                                       }  #City 6 is a Head Quarter
    Required_Inventory={'City1':np.random.randint(70,80),
                       'City2':np.random.randint(20,30),
                       'City3':np.random.randint(70,80), 
                        'City4':np.random.randint(70,80),
                        'City5':np.random.randint(30,40),
                        'City6': 0,
        }
    return cm ,Initial_Inventory,Required_Inventory


def solve_model():
    
    cm,Ic,Rc=create_dummy_data()
    m=Model(name='Intra_Facilities_Movement')
    #Create an Integer MAtrix Variable
    # Amount of Product Moved from City i to City J
    x=m.integer_var_matrix(dict.keys(Ic),dict.keys(Ic),name="x_%s_%s")
    # Final Inventory at City i after Intra site Movement
    
    I=m.integer_var_dict(dict.keys(Ic),name='I_%s')
    #Cons1:  Final Inventory at City I should bemore than or equal to required at city I
    m.add_constraints(I[i]>=Rc[i] for i in dict.keys(Ic))
    #Final Inventory at City i is equal to Invetory avaialble at start +Incoming Inventory- Outgoing Inventory
    m.add_constraints(Ic[i]+
                     sum (x[j,i] for j in dict.keys(Ic))
                     -sum(x[i,j]for j in dict.keys(Ic))
                        ==I[i]for i in dict.keys(Ic))
    m.minimize(m.sum(x[i,j]*cm[i,j] for i in dict.keys(Ic)  for j in dict.keys(Ic)))
    if(m.solve()):
        m.print_solution(print_zeros=False)
    else:
        print('notsolved')
    

















