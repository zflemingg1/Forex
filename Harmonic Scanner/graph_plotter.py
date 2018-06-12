from termcolor import colored # needed for colored print
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
from harmonic_functions import *

class plot_that_graph():
	
	# Initialize class
	def __init__(self,output_file):
		self.output_file = output_file
		print colored(" Testing Graph For :" + self.output_file,'red')
		# import historical data
		data = pd.read_csv(self.output_file)
		data.columns = ['Date','open','high','low','close'] # initialise columns
		data.Date = pd.to_datetime(data.Date,format='%Y-%m-%d %H:%M') # convert to my time format
		data = data.set_index(data.Date) # index by date
		data = data[['open','high','low','close']] # reformat columns to perform data analytics on
		data = data.drop_duplicates(keep=False) # get rid of market downtime, rows where there is no movement
		price = data.close.copy() # close data file after getting all info

		err_allowed = 15.0/100 # variance that ratios of harmonics can be offset by

		# for loop to check for harmonics
		order_number = 1
		for i in range(100,len(price)):
			try:
				current_index,current_pattern,start,end, = peak_detect(price.values[:i],order_number)
				
				XA = current_pattern[1] - current_pattern[0]
				AB = current_pattern[2] - current_pattern[1]
				BC = current_pattern[3] - current_pattern[2]
				CD = current_pattern[4] - current_pattern[3]
					
				moves = [XA,AB,BC,CD]
					
				gartley = is_gartley(moves,err_allowed)
				butterfly = is_butterfly(moves,err_allowed)
				bat = is_bat(moves,err_allowed)
				crab = is_crab(moves,err_allowed)
					
				# Create Label to display to user
				harmonics = np.array([gartley,butterfly,bat,crab])
				labels = ['Gartley', 'Butterfly', 'Bat', 'Crab']
					
				# if bullish or bearish harmonic found
				if np.any(harmonics ==1) or np.any(harmonics == -1):
						
					for j in range(0,len(harmonics)):
						
						if harmonics[j] ==1 or harmonics[j] == -1:
								
							sense = ' Bearish ' if harmonics[j] == -1 else ' Bullish '
							label = output_file[:-10] + sense + labels[j] + ' Found'
							
							plt.title(label)
							# Display to the end plt.plot(np.arange(start,i+(len(price)-i)),price.values[start:i+(len(price)-i)]) # algorithim is not looking ahead buyt the plot grapgh is 
							plt.plot(np.arange(start,i+(len(price)-i)),price.values[start:i+(len(price)-i)])
							plt.plot(current_index,current_pattern,c='r')
							plt.show()
								
				else:
					print "Nothing Found For " + output_file
					print "Incrementing Order Number from " + repr(order_number) + " To ",
					order_number +=1
					print repr(order_number) + " In Graph PLotter"
				
			except Exception as e:
				if "out of bounds for axis" in str(e):
					break
				else:
					print e
					

		
