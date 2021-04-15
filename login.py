#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
from multiprocessing.pool import ThreadPool, Pool
from threading import *
import time
import json
import re
import requests,urllib,sys,threading,time

class LinkCrawler:


	def __init__(self, url):
		self.url 		= url
		self.driver 	= webdriver.Chrome(executable_path=r"/home/dhanasekaran/dhana/practice/link_crawler/chromedriver")
		self.domain_name= ""
		self.LoginButtonsName =['Login','Sign in']
		self.start_scraping()

	def validate_domain(self):

		try:
			response=urllib.request.urlopen(self.url).getcode()
			if response == 200:
				print("domain valid")
				return response
			else:
				print("domain invalid")
				return 400
		except Exception as e:
			print("Error" + str(e))
			return 400

	def start_scraping(self):
		m = re.search('https?://([A-Za-z_0-9.-]+).*', self.url)
		self.domain_name = m.group(1)
		response = self.validate_domain()
		if response == 200:
			print("start scraping")
			self.driver.get(self.url)
			webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
			time.sleep(5)
			self.driver.find_elements_by_xpath("//*[contains(text(), "+ [str(x) for x in self.LoginButtonsName] +")]").click()


url= sys.argv[1]
if url:
	LinkCrawler(url)