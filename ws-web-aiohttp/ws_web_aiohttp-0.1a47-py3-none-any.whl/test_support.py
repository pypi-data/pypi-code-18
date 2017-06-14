import os
import modconf
import subprocess
import time
import unittest
import ws_web_aiohttp

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumTest(unittest.TestCase):
    def setUp(self):
        conf_web_module = 'ws_web_aiohttp.tests.conf.simple_secure'
        conf_web = modconf.import_conf(conf_web_module)
        
        self.driver = webdriver.Firefox()
        
        self.p_sheets = subprocess.Popen(('ws_sheets_server', 
            'ws_sheets_server.tests.conf.simple'))

        print('waiting for sheets server to start')
        time.sleep(3)

        self.p_web = subprocess.Popen(('ws_web_aiohttp', conf_web_module))
        
        print('waiting for web server to start')
        time.sleep(5)
        
        self.url_root = conf_web.Conf.url_root()

    def tearDown(self):
        self.p_sheets.kill()
        self.p_web.kill()
        self.driver.quit()

    def google_login(self):
        google_login = modconf.import_conf('google_login', 
                os.path.join(os.environ['HOME'], 'config'))

        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 
                    '//input[@id="identifierId"]')))
        
        e = self.driver.find_element_by_xpath('//input[@id="identifierId"]')
        
        print('enter username')
        e.click()
        e.send_keys(google_login.email)

        e = self.driver.find_element_by_xpath('//div[@id="identifierNext"]')
        e.click()
        
        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 
                    '//input[@name="password"]')))

        while True:
            try:
                e = self.driver.find_element_by_xpath('//input[@name="password"]')
                print('password', e)
                e.click()
                e.send_keys(google_login.password)
                break
            except Exception as e:
                print(e)
            time.sleep(1)

        e = self.driver.find_element_by_xpath('//div[@id="passwordNext"]')
        print('next', e)
        e.click()


