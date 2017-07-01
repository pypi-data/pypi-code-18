#!/usr/bin/env python3
# encoding: utf-8

"""
server: utilities to start and stop the server
"""

import selenium
import selenium.webdriver
from selenium.webdriver.common.keys import Keys


class ServerBase:
	LOGIN_URL = '?r=site/login'
	SERVERS_URL = '?r=server/index'
	SERVER_URL = '?r=server/view&id={}'
	
	def __init__(self, config):
		self._config = config
		self.base_url = self._config['host']['base_url']
		
		self.browser = selenium.webdriver.Chrome()
		
		# actions should timeout after 3 seconds
		self.implicitly_wait(3)
		self.set_script_timeout(3)
		
		self._login()
	
	
	def start(self):
		"""start the server"""
		
		self._click_manage_button('Start')

	
	def stop(self):
		"""stop the server"""

		self._click_manage_button('Start')
	
	
	def _click_manage_button(self, button_name):
		self._go_to_server_page()
		
		selector = 'input[value="{}"]'.format(button_name)
		
		self.find_element_by_css_selector(selector).click()
	
	
	def _go_to_server_page(self):
		"""go to the page that controls the server"""
		
		server_manage_url = self.base_url \
			+ self.SERVER_URL.format(self._config['server']['id_number'])
		
		if self.current_url != server_manage_url:
			self.get(server_manage_url)
		
	
	def _login(self):
		self.get(self.base_url + self.LOGIN_URL)
		
		# get the first two relevant input elements only
		username_elem, password_elem = self.find_elements_by_css_selector(
			'.row > input'
		)[:2]
		
		username_elem.send_keys(self._config['login']['username'])
		password_elem.send_keys(self._config['login']['password'])
		password_elem.send_keys(Keys.ENTER)
	
	
	
	def __getattribute__(self, attribute):
		"""make all self.browser attributes appear to be self attributes"""
		
		try:
			return object.__getattribute__(self, attribute)
		except AttributeError:
			return self.browser.__getattribute__(attribute)
