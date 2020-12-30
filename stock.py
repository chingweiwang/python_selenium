
import sys
import configparser

from tabulate import tabulate
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

config = configparser.ConfigParser()
config.read('stockConfig.ini')    

opts = Options()
opts.headless = True    

PERatio = eval(sys.argv[2])

stockLocation = '{0}{1}'.format(config['Web']['web_stock'], sys.argv[1])
browser = webdriver.Chrome(
			options=opts,
			executable_path=config['Location']['webdriver']
		)
            
browser.get(stockLocation)
browser.find_element_by_id(config['Web']['web_asset_liabiliry_tab']).click()
browser.find_element_by_id(config['Web']['web_year_report']).click()

print()

yearStr = browser.find_element_by_xpath(config['Web']['web_year']).text
yearList = yearStr.split(' ')
#print('Years:', yearList)

assetStr = browser.find_element_by_xpath(config['Web']['web_asset']).text
assetStr = assetStr.replace(',', '')
assets = assetStr.split(' ')
assetList = []
for asset in assets:
    if '%' not in asset:
        assetList += [asset]
#print('Assets(M) NTD:', assetList)

liabilityStr = browser.find_element_by_xpath(config['Web']['web_liability']).text
liabilityStr = liabilityStr.replace(',', '')
liabilities = liabilityStr.split(' ')
liabilityList = []
for liability in liabilities:
    if '%' not in liability:
        liabilityList += [liability]
#print('Liabilities(M) NTD:', liabilityList)

capitalStockStr = browser.find_element_by_xpath(config['Web']['web_capital_stock']).text
capitalStockStr = capitalStockStr.replace(',', '')
capitalStocks = capitalStockStr.split(' ')
capitalStockList = []
for capitalStock in capitalStocks:
    if '%' not in capitalStock:
        capitalStockList += [capitalStock]
#print('Capital Stock(M) NTD:', capitalStockList)        

browser.find_element_by_id(config['Web']['web_income_statement']).click()

EPSStr = browser.find_element_by_xpath(config['Web']['web_eps']).text
EPSList = EPSStr.split(' ')
#EPSList = list(filter(None, EPSStr.split('-')))
for _ in range(EPSList.count('-')):
    EPSList.remove('-')
#print('EPSs: NTD', EPSList)

print()

ROEList = []
ROETotal = 0
for index in range(len(yearList)):
    navPerShare = ((eval(assetList[index]) - eval(liabilityList[index])) / eval(capitalStockList[index])) * 10
    r = eval(format((eval(EPSList[index]) / navPerShare) * 100, '.3f'))
    ROETotal += r
    ROEList += [r]
#print('ROE(%):', ROEList)
#print('ROE Average(%):', format(ROETotal / len(yearList), '.3f'))
ROEFuture = int(ROETotal / len(yearList))
#print('ROE in future(%):', ROEFuture)                         

browser.find_element_by_id(config['Web']['web_asset_liabiliry_tab']).click()
browser.find_element_by_id(config['Web']['web_simple_report']).click()
recAssetStr = browser.find_element_by_xpath(config['Web']['web_rec_asset']).text
recAsset = recAssetStr.replace(',', '')
recLiabilityStr = browser.find_element_by_xpath(config['Web']['web_rec_liability']).text
recLiability = recLiabilityStr.replace(',', '')
recCapitalStockStr = browser.find_element_by_xpath(config['Web']['web_rec_capital_stock']).text
recCapitalStock = recCapitalStockStr.replace(',', '')
recNAVPerShare = ((eval(recAsset) - eval(recLiability)) / eval(recCapitalStock)) * 10
#print('Recent Net Asset Value per Share: NTD', format(recNAVPerShare, '.3f'))
EPSFuture = (ROEFuture / 100) * recNAVPerShare
stockPrice = EPSFuture * PERatio
#print('Stock cheap price: NTD', format(stockPrice, '.3f'))

tableData = {
        'Year': yearList, 
        'Asset': assetList, 
        'Liabiliry': liabilityList,
        'Capital Stock': capitalStockList,
        'EPS': EPSList,
        'ROE': ROEList    
    }
print('Currency: NTD, Unit: Millinon')
print(tabulate(tableData, headers='keys', tablefmt='fancy_grid'))
print('P/E Ratio: {0}, Stock cheap price: NTD {1}'.format(PERatio, format(stockPrice, '.3f')))
print('ROE = EPS / Net Asset Value per Share')
print('Net Asset Value per Share = ((Asset - Liability) / Capital Stock) X 10')

