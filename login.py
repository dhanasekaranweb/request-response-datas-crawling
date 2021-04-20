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
		self.username 			= "dhanasekaran164@gmail.com"
		self.password 			= "9976784692"
		self.email_phone_x_path	= ""
		self.password_x_path	= ""
		self.elem_txt_action 	= None
		self.LoginElemForm 		= None
		self.keyElem 			= None
		self.LoginKey			= None
		self.LoggedUserName 	= "Dhanasekaran"
		self.is_password_field_hide = False
		self.navbarActions	 	= ['My Profile','Your Account']
		self.sidenavbarActions 	= ['Manage Addresses','Your Addresses']
		self.addressActions 	= ['ADD A NEW ADDRESS','Add address']
		self.addressFields		= ['name','phone','pincode','addressLine2','addressLine1','locationTypeTag']
		self.btnSaveActions 	= ['Save','Add address']
		self.addressFieldsValues= [
			{
				"name":"Dhanasekaran"
			},
			{
				"phone": "+91 9514586795"
			},
			{
				"pincode":"600047"
			},
			{
				"addressLine2":"chennai"
			},
			{
				"addressLine1":"thoraipakkam"
			},
			{
				"locationTypeTag":"HOME"
			}
		]
		self.profilenavbarActions = []
		self.profileActions 	= []
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
				self.elem_txt_action = elem
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

	def check_exists_by_btn_or_link_text(self,text):
		try:
			elem 	= self.driver.find_elements_by_link_text(text)
			if len(elem) > 0:
				self.elem_txt_action = elem
				return True
			else:
				elem = self.driver.find_elements_by_xpath("//form//button[contains(text(), '"+text+"')]")
				if len(elem) > 0:
					self.elem_txt_action = elem
					return True
				else:
					elem = self.driver.find_elements_by_xpath("//form//*[contains(text(), '"+text+"')]//..")
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

	def is_check_username_valid(self):
		try:
			elem	= self.driver.find_elements_by_xpath("//*[contains(text(), '"+self.LoggedUserName+"')]")
			if len(elem) > 0:
				self.elem_txt_action = elem
				return True
			else:
				return False
		except NoSuchElementException:
			return False

	def get_key_values(self, key):
		try:
			val = [print(x) for idx, x in self.addressFieldsValues]
			return val
		except Exception as e:
			print("error" + str(e))
			return False

	def add_new_address(self):
		try:
			print("done")
			if self.elem_txt_action != None:
				actn = self.elem_txt_action[0].click()
				time.sleep(3)
				for item in self.btnSaveActions:
					#_xPath 	= "//form//*[contains(text(), '"+item+"')]//.."
					check 	= self.check_exists_by_btn_or_link_text(item)
					if check == True:
						self.elem_txt_action[0].click()
					else:
						print("failed")
			time.sleep(5)
		except Exception as e:
			print("error" + str(e))
			return False

	def ManageAddress(self):
		try:
			print("here")
			#check side navbar actions
			for item in self.sidenavbarActions:
				_xPath 	= "//*[contains(text(), '"+item+"')]"
				_txt_available = self.check_exists_by_xpath(_xPath)
				if _txt_available == True:
					if self.elem_txt_action != None:
						self.elem_txt_action[0].click()
						time.sleep(3)
						for actns in self.addressActions:
							#_actns_available = self.driver.find_elements_by_xpath("//*[contains(text(), '"+actns+"')]")
							_xPath 	= "//*[contains(text(), '"+actns+"')]"
							_actns_available 	= self.check_exists_by_xpath(_xPath)
							print(_actns_available,actns,"_actns_available")
							if _actns_available == True:
								self.add_new_address()

			time.sleep(5)

		except Exception as e:
			print("error " + str(e))
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
			self.my_profile_section()
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
			time.sleep(20)
			self.my_profile_section() 
		except:
			return False

	def my_profile_section(self):
		try:
			print("fine")
			_chk_username	= self.is_check_username_valid()
			print(_chk_username,"_chk_username")
			if _chk_username == True:
				#hover profile section and click action
				_txt_hover	= self.driver.find_element_by_xpath("//*[contains(text(), '"+self.LoggedUserName+"')]")
				_txt_hover  = ActionChains(self.driver).move_to_element(_txt_hover)
				_txt_hover.perform()
				time.sleep(4)
				
				#check nav bar actions
				for item in self.navbarActions:
					_txt_available = self.check_exists_by_link_text(item)
					if _txt_available == True:
						if self.elem_txt_action != None:
							self.elem_txt_action[0].click()


				#move cursor out from navbar
				_cursor_elem_ 	= self.driver.find_element_by_xpath("//input[@type='text']")
				_cursor_elem 	= ActionChains(self.driver).move_to_element(_cursor_elem_)
				_cursor_elem.perform()

				time.sleep(4)
				self.ManageAddress()

			else:
				print("logger username is wrong")

		except Exception as e:
			print("error" + str(e))
			return False



	def start_scraping(self):
		m = re.search('https?://([A-Za-z_0-9.-]+).*', self.url)
		self.domain_name = m.group(1)
		response = self.validate_domain()
		if response == 200:
			self.driver.get(self.url)
			self.driver.maximize_window()
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
							_frm_types 	= self.check_exists_by_xpath(_xPath)
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