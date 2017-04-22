import pandas as pd
import datetime
import time
 

#N: a er fjöldi ára sem á að sækja gögn fyrir 
#inputs á formi (D)D, (M)M, YYYY, i.e. 1. feb er 1 2 en 12 des er 12 12
def gengiin(sday,smonth,syear,eday,emonth,eyear):
 
	gengi = pd.read_html('http://www.sedlabanki.is/default.aspx?PageID=20f749ed-65bd-11e4-93f7-005056bc0bdb&dag1='+sday+'&man1=+'+smonth+'&ar1='+syear+'&dag2='+eday+'&man2='+emonth+'&ar2='+eyear+'&AvgCheck=dags&Midgengi=on&Mynt9=USD&Mynt10=GBP&Mynt11=DKK&Mynt12=SEK&Mynt13=CHF&Mynt14=JPY&Mynt15=EUR&Mynt16=HKD&Lang=is',thousands = '.',decimal = ',',header = 0,skiprows = [1])
	gengi = pd.DataFrame(gengi[0])
	date = pd.read_html('http://www.sedlabanki.is/default.aspx?PageID=20f749ed-65bd-11e4-93f7-005056bc0bdb&dag1='+sday+'&man1=+'+smonth+'&ar1='+syear+'&dag2='+eday+'&man2='+emonth+'&ar2='+eyear+'&AvgCheck=dags&Midgengi=on&Mynt9=USD&Mynt10=GBP&Mynt11=DKK&Mynt12=SEK&Mynt13=CHF&Mynt14=JPY&Mynt15=EUR&Mynt16=HKD&Lang=is',decimal = '0',header = 1)
	date = pd.DataFrame(date[0])
	date['DAGS'] = pd.to_datetime(date['DAGS'], dayfirst = True)
	gengi = gengi.set_index(date['DAGS'])
	del gengi['Unnamed: 0']
	print(gengi)
	return gengi