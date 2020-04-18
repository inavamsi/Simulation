import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
import copy
import Grid

class Simulate():
	def __init__(self, p_infection, p_recovery, p_unimmunisation, individual_types,initial_pop, grid_size):
		self.individual_types=individual_types
		self.grid=Grid.Grid(grid_size,individual_types,initial_pop)
		self.p_infection=p_infection
		self.p_recovery=p_recovery
		self.p_unimmunisation=p_unimmunisation
		self.day=0

	def simulate_day(self):
		grid=self.grid
		new_grid=copy.deepcopy(grid)

		for i in range(grid.grid_size):
			for j in range(grid.grid_size):
				cur_type=grid.number_to_type[new_grid.grid[i][j]]
				if cur_type=='Infected':
					r=random.random()
					if r<self.p_recovery(self.day,self.grid.current_types_pop):
						grid.convert_type(i,j,'Immune')

				elif cur_type=='Immune':
					r=random.random()
					if r<self.p_unimmunisation(self.day,self.grid.current_types_pop):
						grid.convert_type(i,j,'Susceptible')

				elif cur_type=='Susceptible':
					neighbour_list=new_grid.neighbours(i,j)
					no_infected=neighbour_list[grid.type_to_number['Infected']]
					p_infection_from_nbrs=1 - (1-self.p_infection(self.day,self.grid.current_types_pop))**no_infected
					r=random.random()
					if r<p_infection_from_nbrs:
						grid.convert_type(i,j,'Infected')

				else:
					print('Error: Invalid type!')
					return None
		self.day+=1
		grid.update_timeseries()

	def simulate_days(self,n):
		for i in range(n):
			self.simulate_day()

def scenario1():
	#Standard spread
	def p_infection(day,cur_type_pop):
		return 0.3
	def p_recovery(day,cur_type_pop):
		return 0.2
	def p_unimmunisation(day,cur_type_pop):
		return 0
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']
	grid_size=50
	initial_pop=[2450,50,0]
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(50)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

def scenario2():
	#Hammer-Dance with Turing Pattern
	def p_infection(day,cur_type_pop):
		return 0.4
	def p_recovery(day,cur_type_pop):
		return 0.2
	def p_unimmunisation(day,cur_type_pop):
		return 0.05
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']
	grid_size=50
	initial_pop=[2450,50,0]
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(100)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

def scenario3():
	#Increased social Distancing as time increases 
	def p_infection(day,cur_type_pop):
		if day<25:
			return 0.3 - day/120
		else:
			return 0.3 -(50-day)/120
	def p_recovery(day,cur_type_pop):
		return 0.2
	def p_unimmunisation(day,cur_type_pop):
		return 0
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']
	grid_size=50
	initial_pop=[2450,50,0]
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(50)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

def scenario4():
	#Lockdown followd by full open and then lockdown 
	def p_infection(day,cur_type_pop):
		if day>5 and day <15:
			return 0.01
		if day>20 and day <30:
			return 0.01
		return 0.3 
	def p_recovery(day,cur_type_pop):
		return 0.2
	def p_unimmunisation(day,cur_type_pop):
		return 0
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']
	grid_size=50
	initial_pop=[2450,50,0]
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(50)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

def scenario5():
	#Fear proportional to number of reported cases leading to staying at
	def p_infection(day,cur_type_pop):
		return 0.3*(1-min(cur_type_pop['Infected']/500,1))
	def p_recovery(day,cur_type_pop):
		return 0.2
	def p_unimmunisation(day,cur_type_pop):
		return 0
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']
	grid_size=50
	initial_pop=[2450,50,0]
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(50)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

def scenario6():
	#Alternate day lockdowns
	def p_infection(day,cur_type_pop):# probability of infectiong neighbour
		if day%2==0:
			return 0.01
		return 0.3
	def p_recovery(day,cur_type_pop):#probability of recovering from infection
		return 0.2
	def p_unimmunisation(day,cur_type_pop):#probability of going from immune to susceptible.
		return 0
	individual_types=['Susceptible','Infected','Immune']
	color_list=['white', 'black','red']

	grid_size=50
	initial_pop=[2450,50,0]
	
	sim_obj= Simulate(p_infection, p_recovery, p_unimmunisation,individual_types,initial_pop,grid_size)
	sim_obj.simulate_days(100)
	sim_obj.grid.animate(False,color_list,0.01)
	sim_obj.grid.plot_time_series()

scenario1()  #Standard spread
#scenario4()  #Lockdown-open-Lockdown
#scenario6()  #Alternate day lockdowns


#scenario2()  #Hammer-Dance with Turing Pattern
#scenario3()  #Increased social Distancing as time increases
#scenario5()  #Fear leads to staying at home

















