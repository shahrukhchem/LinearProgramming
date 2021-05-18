# -*- coding: utf-8 -*-
"""
Created on Fri May  7 19:42:27 2021

@author: Shahrukh
"""

""" descriptive model of the telephone production problem is as follows:

Decision variables:
Number of desk phones produced (DeskProduction)
Number of cellular phones produced (CellProduction)
Objective: Maximize profit
Constraints:
The DeskProduction should be greater than or equal to 100.
The CellProduction should be greater than or equal to 100.
The assembly time for DeskProduction plus the assembly time for CellProduction should not exceed 400 hours.
The painting time for DeskProduction plus the painting time for CellProduction should not exceed 490 hours.
Assembly time for desk production is 0.2 and for cell production it is 0.4
painting time for desk production is 0.5 and for cell it is 0.4

"""
import docplex.mp  #importing cplex library

# first import the Model class from docplex.mp
from docplex.mp.model import Model
m=Model(name="Telephone Production")

#createVariables
no_of_desk=m.continuous_var(name="no of desk phone produced") # DEclaring the Decision Variables
no_of_cell=m.continuous_var(name="no of cell phone produced")
#constraint 1
m.add_constraint(no_of_desk>=100)  #ADding Constraints
m.add_constraint(no_of_cell>=100,ctname='No of Cell phone') #Adding Constraints
m.add_constraint(0.2*no_of_desk+0.4*no_of_cell<=400) # Assembly time Constraint
m.add_constraint(0.5*no_of_desk+0.4*no_of_cell<=490) #Assembly time Constraint
m.maximize(12*no_of_desk+20*no_of_cell)  #Objective Function 
s = m.solve() #Solving the model
[nod,noc]=s.get_value_list([no_of_desk,no_of_cell])  #accessng the variables for further processing
m.solution.get_value(no_of_cell)   #accessing single variable