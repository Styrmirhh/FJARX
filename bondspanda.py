import pandas as pd
import numpy as np 



#taka commentið hér út til að sækja gögnin líka
#_________________________________________
#import bondscrapetest 




#N: ClosingPrice = pandain()
#F: ekkert
#E: ClosingPrice inniheldur closing price af allra bréfanna, indexað með dagsetningum

def pandain():
	names = ('19','20','22','25','31')
	names = list(names)
	completedata = {}
	#F: completedata tómt dict
	#E: completedata geymir upplýsingar um hvert bréf í dataframe, lykill bond1 - bond6
	for i in range(1,6):
		fnameb = 'C:\\users\\styrm\\documents\\bondsxdata\\table.' + str(i) +'.dat';
		df = pd.read_csv(fnameb, sep =';', header = 0, skiprows = 0, decimal = ',');
		for col in df:
			#strippum " af str dálkum, annars gerir pandas það sjálft
			if df[col].dtypes == 'object':
				df[col] = df[col].str.strip('"')
			df['Date'] = pd.to_datetime(df['Date'])
		k = {'RIKB' + names[i-1]:df}
		completedata.update(k) 
	df2 = pd.DataFrame()

	for i in completedata:
		k = completedata[i]['Closing price']
		df2[i] = k
	df2['Date'] = completedata['RIKB19']['Date']
	df2= df2.set_index(['Date'])
	close = df2
	return close



#N: returns = pandareturns(df)
#F: df er dataframe með int eða float
#E: dreturns er DataFrame með prósentubreytingu milli lína í df.
def pandareturns(df):
	dreturns = pd.DataFrame()
	for col in df:
		dreturns[col] = df[col].pct_change(1)
	return dreturns

