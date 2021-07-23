# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 12:16:17 2021

@author: Shahrukh
"""

import numpy as np
import pandas as pd
from docplex.mp.model import Model

#2_warehouses
#5_Supermarkets

cost_matrix=pd.read_csv('cost_matrix.csv')

#demand_of_apples_at_Super_market

# Super Market-1: 500
# Super Market-2: 900
# Super Market-3: 1800
# Super Market-4: 200
# Super Market-5: 700


Demand={'SM1': 500,
        'SM2': 900,
        'SM3': 1800,
        'SM4': 200,
        'SM5': 700}

Inventory={'W1':1000,
           'W2':4000}

cm={('W1','SM1'):2000,('W1','SM2'):4000,('W1','SM3'):5000,('W1','SM4'):2000,('W1','SM5'):1000,
    ('W2','SM1'):3000,('W2','SM2'):1000,('W2','SM3'):3000,('W2','SM4'):2000,('W2','SM5'):3000}



m=Model(name='Apple_Operations',log_output=True)

#amount of apple supplied form warehouse to supermarket
x=m.integer_var_matrix(dict.keys(Inventory),dict.keys(Demand),name="x_%s_%s")
#final inventory at super market after movement of apples from warehouse
I=m.integer_var_dict(dict.keys(Demand),name='I_%s')
#final Inventory at super-Market should be greater than or equal to the required
m.add_constraints(I[i]>=Demand[i] for i in dict.keys(Demand))
#final inventory at super market is equal to the apples supplied form both w1 & w2
m.add_constraints(sum (x[i,j] for i in dict.keys(Inventory))==I[j]for j in dict.keys(Demand))
# warehouse cannot supply more than available at the warehouse 
m.add_constraints(sum(x[i,j] for j in dict.keys(Demand))<=Inventory[i] for i in dict.keys(Inventory))

m.minimize(m.sum(x[i,j]*cm[i,j] for i in dict.keys(Inventory)  for j in dict.keys(Demand)))
   


if(m.solve()):
        m.print_information()
        m.print_solution(print_zeros=False)
else:
        print('notsolved')

