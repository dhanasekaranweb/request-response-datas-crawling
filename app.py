#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import sys
from multiprocessing.pool import ThreadPool, Pool
from threading import *
import time
import json

class LinkCrawler:

	def __init__(self, url):
		self.url				= url
		self.driver 			= webdriver.Chrome(executable_path=r"/home/dhanasekaran/dhana/practice/link_crawler/chromedriver")
		self._scrapped_links 	= []
		self.semaphore 			= Semaphore(3)
		self.threads 			= list()
		self.driver_index  		= None
		self.StartCrawl()


	def assign_list_to_driver(self):
		self.driver_index 	= list(range(len(self._scrapped_links)))
		return self.driver_index

	def crawl_complete_data(self, links, index):
		self.semaphore.acquire()
		try:
			self.driver_index[index] = webdriver.Chrome(executable_path=r"/home/dhanasekaran/dhana/practice/link_crawler/chromedriver")
			self.driver_index[index].get(links)
			time.sleep(5)
			collected_data 	= []
			for request in self.driver_index[index].requests:
				temp 	= {}
				if request.response:
					temp["request_link"] 	= request.url
					temp["request_method"] 	= request.method
					temp["request_body"] 	= str(request.body)
					temp["request_header"] 	= dict(request.headers)
					temp["request_path"] 	= request.path
					temp["response_status_code"] 	= request.response.status_code
					temp["request_querystring"] 		= request.querystring
					temp["response_data"] 			= str(request.response.body)
					collected_data.append(temp)

			if(len(collected_data) > 0):
				with open('datas.json', 'a') as final:
					json.dump(collected_data, final)
			self.driver_index[index].quit()

		except Exception as e:
			print("Error "+e)

		finally:
			self.semaphore.release()



	def StartCrawl(self):
		self.driver.maximize_window()
		self.driver.get(self.url)
		webdriver.ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
		elems = self.driver.find_elements_by_xpath("//*[@href]")

		for elem in elems:
			temp = {}
			temp["_scrapped_links"] = elem.get_attribute('href')
			self._scrapped_links.append(elem.get_attribute('href')) 

		self.driver_index 	= list(range(len(self._scrapped_links)))
		#self.assign_list_to_driver()

		for i in range(len(self._scrapped_links)):
			Crawl_thread 	= Thread(target = self.crawl_complete_data, args=(self._scrapped_links[i], i ,))
			self.threads.append(Crawl_thread)
			Crawl_thread.start()

url= sys.argv[1]
if(url):
	LinkCrawler(url)