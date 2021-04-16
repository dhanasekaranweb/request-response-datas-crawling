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
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LinkCrawler:


	def __init__(self, url):
		self.url 				= url
		self.driver 			= webdriver.Chrome(executable_path=r"/home/dhanasekaran/dhana/practice/link_crawler/chromedriver")
		self.domain_name		= ""
		self.LoginButtonsName 	= ['Login','Sign in']
		self.formTypes			= ['text','password','email']
		self.twoPageBtns 		= ['Continue']
		self.btnActionsNames 	= "submit"
		self.placeholders 		= ['Enter Email/Mobile number']
		self.profile_header_keys= ['']
		self.username 			= "dfdf@gmail.com"
		self.password 			= "2332"
		self.email_phone_x_path	= ""
		self.password_x_path	= ""
		self.elem_txt_action 	= None
		self.LoginElemForm 		= None
		self.keyElem 			= None
		self.LoginKey			= None
		self.LoggedUserName 	= "Dhanasekaran"
		self.is_password_field_hide = False
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
			elem = self.driver.find_elements_by_xpath(xpath)
			if len(elem) > 0:
				return True
			else:
				return False
		except NoSuchElementException:
			return False
		return True

	def check_exists_by_link_text(self,text):
		try:
			elem 	= self.driver.find_elements_by_link_text(text)
			if len(elem) > 0:
				self.elem_txt_action = elem
				return True
			else:
				return False
		except NoSuchElementException:
			return False
		return True

	def is_check_password_element(self,xpath):
		try:
			elem 	= self.driver.find_elements_by_xpath( "//input[contains(@type,'password') and contains(@class,'hide')]")
			if len(elem) > 0:
				self.elem_txt_action = elem
				return True
			else:
				return False
		except NoSuchElementException:
			return False
		return True

	def find_div_elements(self, xpath):
		try:
			self.LoginElemForm	= self.driver.find_element_by_xpath(xpath)
			return True
		except NoSuchElementException:
			return False

	def send_keys_to_elements(self,key):
		try:
			self.keyElem = self.LoginElemForm.send_keys(key)
			return True
		except NoSuchElementException:
			return False

	def login(self):
		try:
			_email_or_phone = self.driver.find_element_by_xpath("//span[contains(.,'Enter Email/Mobile number')]//preceding::input[1]")
			_email_or_phone.send_keys(self.username)
			_password 		= self.driver.find_element_by_xpath(self.password_x_path)
			_password.send_keys(self.password)
			btnActions 		= self.driver.find_element_by_xpath("//button/span[contains(text(),'"+self.LoginKey+"')]")
			btnActions.click()
			time.sleep(3)
		except NoSuchElementException:
			return False

	def two_page_login_process(self):
		try:
			_email_or_phone = self.driver.find_element_by_xpath(self.email_phone_x_path)
			_email_or_phone.send_keys(self.username)
			btnActions 		= self.driver.find_element_by_xpath("//input[contains(@type,'submit')]")
			btnActions.click()
			_password 		= self.driver.find_element_by_xpath(self.password_x_path)
			_password.send_keys(self.password)
			_btnActions 	= self.driver.find_element_by_xpath("//input[contains(@type,'submit')]")
			_btnActions.click()
			time.sleep(4)
		except:
			return False

	def my_profile_section(self):
		try:
			print("fine")

		except:
			return False



	def start_scraping(self):
		m = re.search('https?://([A-Za-z_0-9.-]+).*', self.url)
		self.domain_name = m.group(1)
		response = self.validate_domain()
		if response == 200:
			self.driver.get(self.url)
			webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
			time.sleep(5)
			#Login button checks if available or not
			for item in self.LoginButtonsName:
				_txt_available = self.check_exists_by_link_text(item)
				if _txt_available == True:
					#move further
					self.LoginKey = item
					if self.elem_txt_action != None:
						self.elem_txt_action[0].click()
						#check if email / phone / username input text box available or not
						for frms in self.formTypes:
							_xPath 		= str("//input[@type='"+frms+"']")
							print(_xPath,"_xPath")
							_frm_types 	= self.check_exists_by_xpath(_xPath)
							print(_xPath,_frm_types,"_frm_types")
							if _frm_types == True:
								#pass values to input field
								print("path available")
								#add div element to self
								
								if frms == 'text' or frms == 'email':
									self.email_phone_x_path = _xPath

								if frms == 'password':
									self.password_x_path = _xPath
							else:
								print("path not available")
				else:
					print("Add login name in array : " + item)
			time.sleep(3)

			#goto login process
			if self.email_phone_x_path != "" and self.password_x_path != "":
				#check tow page or single paged container
				check = self.is_check_password_element(self.password_x_path)
				if check == True:
					self.two_page_login_process()
				else:
					self.login()


url= sys.argv[1]
if url:
	LinkCrawler(url)