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
from selenium.common.exceptions import NoSuchElementException

class LinkCrawler:


	def __init__(self, url):
		self.url 				= url
		self.driver 			= webdriver.Chrome(executable_path=r"/home/dhanasekaran/dhana/practice/link_crawler/chromedriver")
		self.domain_name		= ""
		self.LoginButtonsName 	=['Login','Sign in']
		self.formTypes			= ['text','password','email']
		self.btnActionsNames 	= ['submit','button']
		self.elem_txt_action 	= None
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

	def check_exists_by_xpath(self,xpath):
		try:
			elem = self.driver.find_element_by_xpath(xpath)
			if len(elem) > 0:
				return True
			else:
				return False
		except NoSuchElementException:
			return False
		return True

	def check_exists_by_text(self,text):
		try:
			elem = self.driver.find_elements_by_link_text(text)
			if len(elem) > 0:
				self.elem_txt_action = elem
				return True
			else:
				return False
		except NoSuchElementException:
			return False
		return True

	def start_scraping(self):
		m = re.search('https?://([A-Za-z_0-9.-]+).*', self.url)
		self.domain_name = m.group(1)
		response = self.validate_domain()
		if response == 200:
			print("start scraping")
			self.driver.get(self.url)
			webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
			time.sleep(5)
			#Login button checks if available or not
			for item in self.LoginButtonsName:
				_txt_available = self.check_exists_by_text(item)
				if _txt_available == True:
					#move further
					print("yes")
					if self.elem_txt_action != None:
						self.elem_txt_action[0].click()
				else:
					print("Add login name in array : " + item)
			time.sleep(3)


url= sys.argv[1]
if url:
	LinkCrawler(url)