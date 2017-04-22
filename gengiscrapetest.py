#============================================================================================================================
# python script that uses the selenium package to automatically brows http://www.nasdaqomxnordic.com/aktier/historiskakurser
# in order to download and store historical data on the Stockholm stock-exchange.
#============================================================================================================================
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import subprocess
import shutil
import distutils.core
import datetime
import time
 
#====================
# User defined input:
#====================
 
OSX = False # Set to true if you are working on your mac at home.
 
# #====================================================================================================
# # Here the user specifies the download location of the stockmarket data files and where to save them:
# # Observe that you need to use double back-slash (\\) also in the end of the locations if you are 
# # using a windows system, and a single slash (/) in the end of the locations otherwise.
# #====================================================================================================
if OSX:
    DOWNLOADLOCATION = "/Users/petros/Downloads/"
    SAVELOCATION = "/Users/petros/AKTIER/DATA/"
else:
    DOWNLOADLOCATION = "\\Users\\styrm\\Downloads\\"
    SAVELOCATION = "C:\\Users\\styrm\\Documents\\gengidata\\"
 
#========================================================================================================
# Here the user fills in the start date defining how long back in history we should try and download data
#========================================================================================================
syear = str(datetime.datetime.now().year-1)
sday = str(datetime.datetime.now().day)
smonth = str(datetime.datetime.now().month)
 
 
if datetime.datetime.now().day-1 < 10: sday='0'+sday
if datetime.datetime.now().month < 10: smonth ='0'+smonth
 
 
#==========================
# END of user defined input
#==========================
 
#=================================================
# Clean the csv -files from the download directory:
#=================================================
if OSX:
    command = 'rm '+DOWNLOADLOCATION+'*.csv'
    os.system(command)
else:
    command = 'DEL '+DOWNLOADLOCATION+'ExcelExport.xls'
    os.system(command)
 
 
 
mydriver = webdriver.Chrome()
 
fxname = []
xpaths = []
 
if OSX:
    tempfile = SAVELOCATION+'listofstocks.dat'
    outfile = open(tempfile,'w')
else:
    tempfile = SAVELOCATION+'listofcurrency.dat'
    outfile = open(tempfile,'w')
#========================================================================
# The list of large companies on the Stockholm stock-market:
#========================================================================
fxname.append("USD")
fxname.append("GBP")
fxname.append("DKK")
fxname.append("SEK")
fxname.append("CHF")
fxname.append("JPY")
fxname.append("HKD")
fxname.append("EUR")




 
 
 
 
# Here we get the date of today
eyear = str(datetime.datetime.now().year)
eday = str(datetime.datetime.now().day-1)
emonth = str(datetime.datetime.now().month)
 
if datetime.datetime.now().day-1 < 10: eday='0'+eday
if datetime.datetime.now().month < 10: emonth ='0'+emonth
 
 
 
 
xpaths.append('//*[@id="ctl00_ctl34_ddlDays_From"]')
xpaths.append('//*[@id="ctl00_ctl34_ddlMonths_From"]')
xpaths.append('//*[@id="ctl00_ctl34_ddlYears_From"]')
xpaths.append('//*[@id="ctl00_ctl34_ddlDays_To"]')
xpaths.append('//*[@id="ctl00_ctl34_ddlMonths_To"]')
xpaths.append('//*[@id="ctl00_ctl34_ddlYears_To"]')
xpaths.append('//*[@id="ctl00_ctl34_MyntUSD"]')
 
xpaths.append('//*[@id="exportExcel"]')
 
 
i = 0
actions = ActionChains(mydriver)
actions.send_keys(Keys.SPACE)
#================================================================================================================
# Loop over all big and medium sized companies at the Stockholm stock-market. Downloading historical data of the 
# stock from a date specified by the user to today.
#================================================================================================================
 
mydriver.get('http://www.sedlabanki.is/?PageId=3ea6d66d-e51e-4c7b-bb0d-bedc5377e014')
time.sleep(2)



# mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlDays_From"]').send_keys(sday)
# time.sleep(1)
# mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlMonths_From"]').send_keys(smonth)
# time.sleep(1)
mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlYears_From"]').send_keys(syear)
time.sleep(1)
# mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlDays_To"]').send_keys(eday)
# time.sleep(1)
# mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlMonths_To"]').send_keys(emonth)
# time.sleep(1)

mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_ddlYears_To"]').send_keys(eyear)
time.sleep(1)
mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_cbKaupgengi"]').send_keys(Keys.SPACE)
time.sleep(1)
mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_cbSolugengi"]').send_keys(Keys.SPACE)
time.sleep(1)
for name in fxname:
    mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_Mynt'+name+'"]').send_keys(Keys.SPACE)
    time.sleep(1)
mydriver.find_element_by_xpath('//*[@id="ctl00_ctl34_btnSelect"]').send_keys(Keys.SPACE)
time.sleep(1)



 
if OSX:
    savefile = SAVELOCATION+'table.'+index
    savefile = savefile+'.dat'
else:
    savefile = SAVELOCATION+'gengisi.xls'
         
k = 0
time.sleep(2)
if OSX:
    command = 'ls '+DOWNLOADLOCATION+'*.csv > TEMP'
    os.system(command)
else:
    command = 'DIR /b '+DOWNLOADLOCATION+'ExcelExport.xls > TEMP'
    os.system(command)
 
with open('TEMP') as f:
    for line in f:
        if k == 0: downloadfile= line
        k = k + 1
downloadfile = downloadfile.strip('\n')
 
print(downloadfile)
if OSX:
    os.system("rm TEMP")
    time.sleep(1.0)
else:
    os.system("DEL TEMP")
    time.sleep(1.0)

 
if OSX:
    subprocess.call(["mv",downloadfile,savefile])
else:
    downl = DOWNLOADLOCATION+downloadfile
    shutil.move(downl, savefile)
 
aktier = str(i)+' '+str(name)+'\n'
outfile.write(aktier)
i = i + 1
 
# Here we close the driver after all the data has been downloaded
mydriver.close()
# outfile.close()