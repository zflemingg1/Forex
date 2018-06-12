from termcolor import colored # needed for colored print
import requests
import urllib
import ssl
import csv
import pandas as pd
import sys
import operator
from graph_plotter import *

class Get_Latest_Data():
	
	currencies = ['EURUSD','USDJPY','GBPJPY','GBPUSD','USDCHF','GBPAUD','EURNZD','GBPJPY','EURAUD','GBPCHF','EURJPY','EURCAD','AUDJPY','NZDJPY','AUDCHF','USDCAD'] # list of target currency pairs
	
	# Initialize class
	def __init__(self,time_interval):
		self.time_interval = time_interval
		# Loop Through All The Currencies
		for currency_pair in self.currencies:

			# Test Each Currency Pair
			print colored ("Testing Currency Pair: " + currency_pair + "[*]", 'yellow',attrs=['bold'])
			try:
				
				# Call relevant functions
				output_file = self.download_chart(currency_pair,) # Call function to loop through currnecy list and download chart for each pair
				self.format_csv_file(output_file) # call function to format the csv file
				self.graph_plotter(output_file) # function to call the graph plotter function
			except Exception as e:
				print e
				continue

	#function to loop through currnecy list and download chart for each pair
	def download_chart(self, currency_pair):
		
		#Download CSV For That Currency Pair
		try:
			# Download Chart For That Currency Pair
			url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=" + currency_pair + "&interval=" + self.time_interval + "&outputsize=full&apikey=NTJZEAIUSAHYZCLJ&datatype=csv"
			context = ssl._create_unverified_context() # dont verify ssl cert
			csv = urllib.urlopen(url, context=context).read() # returns type 'str'
			output_file = currency_pair + "_" + self.time_interval + ".csv"
				
			# Write To CSV FIle
			with open(output_file, 'w') as fx: # str, hence mode 'w'
				fx.write(csv)
					
			return output_file
				
		except Exception as e:
			print e
		
	def format_csv_file(self,output_file):
		#Remove The Useless Column 
		result_file = output_file + "_" + self.time_interval + ".csv"
		# Remove Useless Column
		f=pd.read_csv(output_file)
		keep_col = ['timestamp','open','high','low','close']
		new_f = f[keep_col]
		new_f.to_csv(output_file, index=False)

		#Sort the csv file in order of oldest to newest based on the timestamp
		data = csv.reader(open(output_file),delimiter=',')
		sortedlist = sorted(data, key=operator.itemgetter(0)) # 0 specifies according to first column we want to sort
		index = sortedlist[-1]
		sortedlist = sortedlist[:-1]
		sortedlist = [index] + sortedlist
		
		#now write the sort result into new CSV file
		with open(output_file, "wb") as f:
			fileWriter = csv.writer(f, delimiter=',')
			for row in sortedlist:
				fileWriter.writerow(row)
				
	def graph_plotter(self,output_file):
		plot_that_graph(output_file)
		
		
def main():
	# Info about program --> Display to the user
	print colored (30 * "-", 'cyan')
	print colored("\nHarmonic Scanner", 'cyan',  attrs=['bold'])
	print colored (30 * "-", 'cyan')
	print colored("Author: Zach Fleming", 'yellow')
	print colored("Date: 09/04/18", 'green')
	print colored("\nDescription: Checks to see if a harmonic pattern is present for that chosen currency pair within the chosen time interval",'cyan')
	print colored("Will Test The Following Currencies;\n",'cyan')
	
	# Display Currency Pairs to the user
	currencies = ['EURUSD','USDJPY','GBPJPY','GBPUSD','USDCHF','GBPAUD','EURNZD','GBPJPY','EURAUD','GBPCHF','EURJPY','EURCAD','AUDJPY','NZDJPY','AUDCHF','USDCAD']
	for element in currencies:
		print colored(element + " ",'green',attrs=['bold']),
			
	# Ask user for Currency Pairs
	print colored ("\n\nPlease Select One Of The Following Time Intervals",'yellow',attrs=['bold'])
	print colored("1. 1 Min",'cyan',attrs=['bold'])
	print colored("2. 5 Min",'cyan',attrs=['bold'])
	print colored("3. 15 Min",'cyan',attrs=['bold'])
	print colored("4. 30 Min",'cyan',attrs=['bold'])
	print colored("5. 60 Min",'cyan',attrs=['bold'])
	
	# Basic loop with error checking
	while True:
		time_interval = raw_input("Select Option: ") # get user choice
		if time_interval == "1":
			Get_Latest_Data("1min")
			break
		elif time_interval == "2":
			Get_Latest_Data("5min")
			break
		elif time_interval == "3":
			Get_Latest_Data("15min")
			break
		elif time_interval == "4":
			Get_Latest_Data("30min")
		elif time_interval == "5":
			Get_Latest_Data("60min")
		else:
			print colored("Error Invalid Option!",'red',attrs=['bold'])
if __name__== "__main__":
  main()
		
		
			
