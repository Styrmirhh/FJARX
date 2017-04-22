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
 



# syear = str(datetime.datetime.now().year-1)
# sday = str(datetime.datetime.now().day)
# smonth = str(datetime.datetime.now().month)

eyear = str(datetime.datetime.now().year)
eday = str(datetime.datetime.now().day-1)
emonth = str(datetime.datetime.now().month)

syear = str(2015)
smonth = str(1)
sday = str(1)

# eyear = str(2016)
# emonth = str(1)
# eday = str(10)


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


def pandas_date_comp(date):
	pddate = pd.to_datetime(date)
	return pddate
def year_plus(start_date):
	end_date = start_date + datetime.timedelta(days=365)
	return end_date


FX_List = ['USD','GBP','DKK','SEK','CHF','JPY','EUR','HKD']
Bonds_List = ['RIKB19','RIKB20','RIKB22','RIKB25','RIKB31']
dates_fx = dates_input_fx(syear,smonth,sday,eyear,emonth,eday)
FXrates = bondsgengi.gengiin(dates_fx['sday'],dates_fx['smonth'],dates_fx['syear'],dates_fx['eday'],dates_fx['emonth'],dates_fx['eyear'])
dates_bonds = dates_input_bonds(syear,smonth,sday,eyear,emonth,eday)
#bondscrapetest.bondsupdate(dates_bonds['sday'],dates_bonds['smonth'],dates_bonds['syear'],dates_bonds['eday'],dates_bonds['emonth'],dates_bonds['eyear'])

start_date = datetime.datetime(int(dates_fx['syear']),int(dates_fx['smonth']),int(dates_fx['sday']))
pd_start_date = pandas_date_comp(start_date)
pd_end_date = year_plus(start_date)
Close_Prices = bondspanda.pandain()
Price_Data = Close_Prices.join(FXrates)
index = ix.mvokkar(Price_Data[Bonds_List])
Price_Data = Price_Data.join(index)
Price_Data_Returns = bondspanda.pandareturns(Price_Data)
Price_Data_Returns = Price_Data_Returns.drop(Price_Data_Returns.index[[0]], axis = 0)
print(Price_Data_Returns)


# print(Price_Data[Bonds_List])
# print(Price_Data[FX_List])
# print(Price_Data[pd_start_date:pd_end_date])
returns_bonds = Price_Data_Returns[Bonds_List]
returns_bonds = returns_bonds[pd_start_date:pd_end_date]
FXreturns = Price_Data_Returns[FX_List]
FXreturns = FXreturns[pd_start_date:pd_end_date]

index_returns = Price_Data_Returns['Ix']
index_returns = index_returns[pd_start_date:pd_end_date]

indexstd = index_returns.std()*np.sqrt(252)
indexret = index_returns.mean()*252
print(index_returns)



#Finnum fylgni, covariance og return af vísitölu þegar tekið er tillit til gjaldeyris
Panamareturns = pd.DataFrame()
for col in FXreturns:
	k = FXreturns[col].sub(index_returns)
	Panamareturns[col] = k
FXreturns = FXreturns.join(index_returns)

FXreturns_cov = FXreturns.cov()*252
FXreturns_corr = FXreturns.corr()
#FXreturns = FXreturns.drop(FXreturns.columns[0],axis = 1)
print(FXreturns)
print('FXreturns')

fx_indexed = pd.DataFrame(index = [['std','ret']])
for col in Panamareturns:
	fxstd = FXreturns_cov[col][col] + indexstd - 2*FXreturns_cov[col]['Ix']
	fxret = Panamareturns[col].mean()*252
	print(fxstd)
	print(fxret)
	fx_indexed[col]=[fxstd,fxret]

print(fx_indexed)


newreturns = returns_bonds.as_matrix()
return_cov = np.cov(newreturns, rowvar = False)
return_cov = return_cov*252
newreturns = newreturns*252
meanret = np.array(np.mean(newreturns, axis = 0))
print(meanret)
#Framfall 
optret = np.ones(2000)
optstd = np.ones(2000)
optports = np.zeros((2000,5))
for i in range(0,2000):
	opt_port = mv.walloc(meanret, return_cov, i*0.0001)
	optports[i,...] = opt_port
	optret[i] = np.dot(opt_port,meanret)
	optstd[i] = np.sqrt(np.dot(np.dot(opt_port.T,return_cov),opt_port))




#Framfall án skortsölu
#noshortports geymir vigtirnar, og fyrsta lína segir til um hvort lausnin sé gild eða ekki
noshort_ret = np.ones(2000)
noshort_std = np.ones(2000)
k = 0
noshortports = np.zeros((2000,6))
for i in range(0,2000):
	noshort = mv.noshort_alloc(meanret, return_cov, i*0.0001)
	if noshort['status'] == 'optimal':
		noshortports[i,0] = 1.0
		noshort = np.array(noshort['x'])
		noshortports[i,1:6] = noshort.T
		#Til að plotta framfallið
		noshort_ret[k] = np.dot(noshort.T,meanret)
		noshort_std[k] = np.sqrt(np.dot(np.dot(noshort.T,return_cov),noshort))
		k = k + 1



#PORTFOLIOS TO USE
shortallowed = mv.walloc(meanret, return_cov, 0.06)
shortnotallowed = mv.noshort_alloc(meanret, return_cov, 0.05)
shortreturn = np.dot(shortallowed,meanret)
shortstd = np.sqrt(np.dot(np.dot(shortallowed.T,return_cov),shortallowed))
shortnotallowed = np.array(shortnotallowed['x'])
shortnotreturn = np.dot(shortnotallowed.T,meanret)
shortnotstd= np.sqrt(np.dot(np.dot(shortnotallowed.T,return_cov),shortnotallowed))
print('short allowed:')
print('weights:' + str(shortallowed))
print('return:' + str(shortreturn))
print('std:' + str(shortstd))
print('short not allowed:')
print('weights:' + str(shortnotallowed))
print('return:' + str(shortnotreturn))
print('std:' + str(shortnotstd))

var_noshort=VaR.var_cov_var(10000,0.95,shortnotreturn,shortnotstd)
var_short=VaR.var_cov_var(10000,0.95,shortreturn,shortstd)

print("Value-at-Risk for no short portfolio: ", var_noshort[0,0])
print("Value-at-Risk for short portfolio: ", var_short)

# #Söfn með vigtum völdum af handahófi
# n_portfolios = 5000
# means, stds = np.column_stack([
#     pf.random_portfolio(newreturns, return_cov) 
#     for _ in range(n_portfolios)
# ])

noshortexp_ret = np.ones(2000)
noshortexp_std = np.ones(2000)
p = 0
noshortportsexplim = np.zeros((2000,6))
for i in range(0,2000):
	noshortexplim = mv.noshort_exposurelim_alloc(meanret, return_cov, i*0.0001,0.5)
	if noshortexplim['status'] == 'optimal':
		noshortportsexplim[i,0] = 1.0
		noshortexplim = np.array(noshortexplim['x'])
		noshortportsexplim[i,1:6] = noshortexplim.T
		#Til að plotta framfallið
		noshortexp_ret[p] = np.dot(noshortexplim.T,meanret)
		noshortexp_std[p] = np.sqrt(np.dot(np.dot(noshortexplim.T,return_cov),noshortexplim))
		p = p + 1


shortexp_ret = np.ones(2000)
shortexp_std = np.ones(2000)
t = 0
shortportsexplim = np.zeros((2000,6))
for i in range(0,2000):
	shortexplim = mv.short_exposurelim_alloc(meanret, return_cov, i*0.0001,0.5)
	if shortexplim['status'] == 'optimal':
		shortportsexplim[i,0] = 1.0
		shortexplim = np.array(shortexplim['x'])
		shortportsexplim[i,1:6] = shortexplim.T
		#Til að plotta framfallið
		shortexp_ret[t] = np.dot(shortexplim.T,meanret)
		shortexp_std[t] = np.sqrt(np.dot(np.dot(shortexplim.T,return_cov),shortexplim))
		t = t + 1

with open('portfolio.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(shortnotallowed)

sns.set_style('dark')
# sns.plt.plot(stds, means, 'o', markersize=3)
for col in returns_bonds:
	sns.plt.plot(returns_bonds[col].std()*np.sqrt(252), returns_bonds[col].mean()*252,'o',label = str(col))
sns.plt.plot(optstd, optret,markersize = 2, label = 'Short')
sns.plt.plot(noshort_std[:k-1],noshort_ret[:k-1],markersize = 2, label = 'noshort')
sns.plt.plot(noshortexp_std[:p-1],noshortexp_ret[:p-1],markersize = 2, label = 'noshortexp')
sns.plt.plot(shortexp_std[:t-1],shortexp_ret[:t-1],markersize = 3, label = 'shortexp')
sns.plt.plot(indexstd,indexret,'D',label = 'index')

sns.plt.plot(shortstd,shortreturn,'D', label = '6pc short')
sns.plt.plot(shortnotstd,shortnotreturn,'D', label = '6pc no short')

plt.xlabel('std')
plt.ylabel('mean')
plt.legend()
plt.title('Mean and standard deviation of various portfolios')
plt.show()
