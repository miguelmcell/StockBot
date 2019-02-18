from selenium import webdriver
from datetime import datetime, date
import pandas as pd
import time
from Robinhood import Robinhood

def init():
	global driver
	global page_date
	global my_trader
	global logged_in

	my_trader = Robinhood()
	logged_in = my_trader.login(username="miguelmcell",password="!Migmen2020!")
	print(my_trader.quote_data("NVIDIA"))
	page_date = 'NULL'
	driver = webdriver.Chrome(r'C:\Users\migue\Desktop\StockBot\chromedriver.exe')
	print('driver initialized')

def navigate():
	global driver
	driver.get('https://tradestockalerts.com/my-account/')
	driver.find_element_by_id('username').send_keys('miguelmendoza1693')
	driver.find_element_by_id('password').send_keys('!migmen2020!')
	driver.find_element_by_name('login').click()
	print('successfuly logged into tradestockalerts')

def extract():
	global driver
	global page_date
	global stock1
	global stock2
	global stock3
	driver.get('https://tradestockalerts.com/penny/')
	print("checking for today\'s stocks(",date.today().strftime("X%m/X%d/%Y").replace("X0","X").replace('X',''),")")
	# print("looking for", date.today().strftime("X%m/X%d/%Y").replace("X0","X").replace('X',''))
	try:
		date_element = driver.find_elements_by_xpath("//*[text()='2/15/2019']")[0]
		# date_element = driver.find_elements_by_xpath("//*[text()=" + "\'" + date.today().strftime("X%m/X%d/%Y").replace("X0","X").replace('X','') + "\'" + "]")[0]
	except:
		return 0
	stock1_element = driver.find_elements_by_xpath('//*[@id="content"]/article/div/div/div/div/section/div/div/div[1]/div/div/div/div/div/div[3]/h1[2]')[0]
	stock2_element = driver.find_elements_by_xpath('//*[@id="content"]/article/div/div/div/div/section/div/div/div[1]/div/div/div/div/div/div[3]/div/div/h1')[0]
	stock3_element = driver.find_elements_by_xpath('//*[@id="content"]/article/div/div/div/div/section/div/div/div[1]/div/div/div/div/div/div[3]/div/div/div/h1')[0]

	page_date = date_element.text
	stock1 = stock1_element.text
	stock2 = stock2_element.text
	stock3 = stock3_element.text

	print('-----------------------------')
	print('date is', page_date)
	print('first stock is', stock1)
	print('second stock is', stock2)
	print('third stock is', stock3)
	print('-----------------------------')

	return 1

def verify():
	global page_date
	global my_trader
	global logged_in
	global stock1
	global stock2
	global stock3
	print('verifying information')
	# make sure that these 3 stocks are not from yesterday
	with open('previous.txt', 'r') as f:
		#get previous stocks
		#if no previous stocks then ignore
		line0 = f.readline().strip()
		line1 = f.readline().strip()
		line2 = f.readline().strip()
		line3 = f.readline().strip()
		#check if the page has been updated
		if(line0 == page_date):
			print("This was already executed once!")
			return -1
		if(line1 != '' and line2 != '' and line3 != ''):
			#now check if any match
			if(line1 == stock1 and line2 == stock2 and line3 == stock3):
				#then this is invalid!
				print("INVALID STOCKS: THESE WERE FROM YESTERDAY!")
				return -1

	#verify that they actually are stocks in robinhood
	try:
		my_trader.instruments(stock1)[0]
	except:
		print("INVALID STOCK", stock1)
		return -1
	try:
		my_trader.instruments(stock2)[0]
	except:
		print("INVALID STOCK", stock2)
		return -1
	try:
		my_trader.instruments(stock3)[0]
	except:
		print("INVALID STOCK", stock3)
		return -1

	#update with today'stocks
	with open('previous.txt', 'w') as f:
		f.write(page_date+'\n')
		f.write(stock1+'\n')
		f.write(stock2+'\n')
		f.write(stock3+'\n')

	return True

def execute_buy():
	global my_trader
	global logged_in
	global stock1
	global stock2
	global stock3
	# do all the nasty math for the 3 stocks
	# 50% go to stock1
	# 25% for the rest
	funds = (my_trader.equity()*0.95) #should probably change that later
	stock_instrument1 = my_trader.instruments(stock1)[0]
	stock_instrument2 = my_trader.instruments(stock2)[0]
	stock_instrument3 = my_trader.instruments(stock3)[0]

	# stock_price1 = 
	# stock_price2 = 
	# stock_price3 = 
	


	buy_order = my_trader.place_buy_order(stock_instrument, 1)
	sell_order = my_trader.place_sell_order(stock_instrument, 1)


def main():
	init()
	navigate()
	while(extract()==0):
		print("stocks not updated, trying again in 5 seconds")
		time.sleep(5)
	print("**Today's stocks have been found**")
	if(verify()==-1):
		print("exiting")
		return -1
	
	print("information verified, executing robinhood buy")
	#execute_buy()

	#codes
	# 0 = retry
	# -1 = something is wrong, examine code
	# 1 = good

main()