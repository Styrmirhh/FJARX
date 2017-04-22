import bondspanda
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import markovitzlagrange as mv
import pyfront as pf
import seaborn as sns
import VaR
import mvokkar as ix
import bondsgengi
import pandas as pd
import csv
import bondscrapetest
import datetime
import time
import bondsbalance



#sett upp her til að prófa yfir heilt ár, 1 check í mánuði
#taka út forlykkju og dagsetninga-overwritið til að koma því á daglegt recheck


syear = str(2015)
smonth = str(1)
sday = str(1)

eyear = str(datetime.datetime.now().year)
eday = str(datetime.datetime.now().day-1)
emonth = str(datetime.datetime.now().month)

def year_plus(start_date):
	end_date = start_date + datetime.timedelta(days=365)
	return end_date

def one_day_plus(start_date):
	newstart = start_date+datetime.timedelta(days=1)
	return newstart

def pandas_date_comp(date):
	pddate = pd.to_datetime(date)
	return pddate
#Use to pass in desired dates. Automatically checks for weekends and moves to next business day after weekend
#Needs support to filter out holidays?
#Returns start-date and end-date in the appropriate format for SI
def dates_input_fx(syear,smonth,sday,eyear,emonth,eday):
	weekdaycheck = datetime.datetime(int(syear),int(smonth),int(sday)).weekday()
	if weekdaycheck == 5:
		sday = int(sday) + 2
		sday = str(sday)
	elif weekdaycheck == 6:
		sday = int(sday)+1
		sday = str(sday)
	dates_fx={}
	for i in ('syear','smonth','sday','eyear','emonth','eday'):
		dates_fx[i] = locals()[i]
	return dates_fx

#Same as other date function, except it returns the dates in the appropriate format for NASDAQ OMX
def dates_input_bonds(syear,smonth,sday,eyear,emonth,eday):
	weekdaycheck = datetime.datetime(int(syear),int(smonth),int(sday)).weekday()
	if weekdaycheck == 5:
		sday = int(sday) + 2
		sday = str(sday)
	elif weekdaycheck == 6:
		sday = int(sday)+1
		sday = str(sday)
	if(int(smonth)<10): smonth = '0'+smonth
	if(int(sday)<10): sday = '0'+sday
	if(int(emonth)<10): emonth = '0'+emonth
	if(int(eday)<10): eday = '0'+eday
	dates_bonds={}
	for i in ('syear','smonth','sday','eyear','emonth','eday'):
		dates_bonds[i] = locals()[i]
	return dates_bonds


# sday = str(10)
# eday = str(10)
# syear = str(2015)
# eyear = str(2016)

# smonth = str(i)
# emonth = str(i)


# #óþarfi
# bondscrapetest.bondsupdate(sday,smonth,syear,eday,emonth,eyear)
# FXreturns = bondspanda.pandareturns(FXrates)
# FXreturns = FXreturns.drop(FXreturns.index[[0]], axis = 0)


FX_List = ['USD','GBP','DKK','SEK','CHF','JPY','EUR','HKD']
Bonds_List = ['RIKB19','RIKB20','RIKB22','RIKB25','RIKB31']


dates_fx = dates_input_fx(syear,smonth,sday,eyear,emonth,eday)
start_date = datetime.datetime(int(dates_fx['syear']),int(dates_fx['smonth']),int(dates_fx['sday']))
FXrates = bondsgengi.gengiin(dates_fx['sday'],dates_fx['smonth'],dates_fx['syear'],dates_fx['eday'],dates_fx['emonth'],dates_fx['eyear'])


Close_Prices = bondspanda.pandain()
Price_Data = Close_Prices.join(FXrates)
Price_Data_Returns = bondspanda.pandareturns(Price_Data)
Price_Data_Returns = Price_Data_Returns.drop(Price_Data_Returns.index[[0]], axis = 0)
print(Price_Data_Returns)







#Check for an update each day for a year
for j in range(1,365):
	#Update the date range we are working with (1 year window)
	pd_start_date = pandas_date_comp(start_date)
	pd_end_date = year_plus(start_date)
	returns_bonds = Price_Data_Returns[Bonds_List]
	returns_bonds = returns_bonds[pd_start_date:pd_end_date]
	print(returns_bonds.tail()) #a check
	FXreturns = Price_Data_Returns[FX_List]
	FXreturns = FXreturns[pd_start_date:pd_end_date]

	#formatting of data for the check
	newreturns = returns_bonds.as_matrix()
	return_cov = np.cov(newreturns, rowvar = False)
	return_cov = return_cov*252
	newreturns = newreturns*252
	meanret = np.array(np.mean(newreturns, axis = 0))


	#get our current portfolio
	currentfolio = []
	#if i == 0:
	with open('portfolio.csv', newline='') as f:
	    reader = csv.reader(f)
	    for row in reader:
	        currentfolio.append(row)
	# else:
	# 	with open('portfoliomonth'+str(i-1)+'.csv', newline='') as f:
	# 	    reader = csv.reader(f)
	# 	    for row in reader:
	# 	        currentfolio.append(row)

	currentfolio = np.array(currentfolio)
	currentfolio = currentfolio.astype(float)
	print(pd_end_date)
	print(currentfolio)
	#Get an updated portfolio, might be the same
	newport = bondsbalance.rebalance_check(currentfolio,meanret,return_cov,0.05)

	#Overwrite our old portfolio
	# with open('portfoliomonth'+str(i)+'.csv', 'w', newline='') as f:
	#     writer = csv.writer(f)
	#     writer.writerows(newport)
	with open('portfolio.csv', 'w', newline='') as f:
	    writer = csv.writer(f)
	    writer.writerows(newport)
	start_date = one_day_plus(start_date)


