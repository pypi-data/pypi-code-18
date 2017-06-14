import os
import time
import modconf
import ws_sheets.tests.functions

import ws_web_aiohttp
import ws_web_aiohttp.test_support

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class MySeleniumTests(ws_web_aiohttp.test_support.SeleniumTest):

    def test_view_sheet(self):
        
        if 0:
            user = core.models.User.objects.create_user('test', 'test@test', 'password')
            user.is_staff = True
            user.save()
    
            self.driver.get('%s%s' % (self.live_server_url, '/admin/login/'))
    
            username_input = self.driver.find_element_by_name("username")
            username_input.send_keys("test")
    
            password_input = self.driver.find_element_by_name("password")
            password_input.send_keys("password")
    
            self.driver.find_element_by_xpath('//input[@value="Log in"]').click()
    
    
            WebDriverWait(self.driver, 10).until(
                    EC.title_is("Site administration | Django site admin"))
        
        if 0:
            self.driver.get('%s%s' % (self.live_server_url, django.urls.reverse('sheets:index')))
    
            text_input = self.driver.find_element_by_name("book_name")
            text_input.send_keys("selenium test book")
    
            self.driver.find_element_by_xpath('//input[@value="new book"]').click()

        url = '{}/book_new/{}/'.format(self.url_root, 'test_' + self.__class__.__qualname__)

        print('url = {}'.format(url))

        self.driver.get(url)
       
        self.google_login()

        WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, 
                    '//table[@class="htCore"]')))
       
        print('hot table found')

        # test script pre
        e = self.driver.find_element_by_xpath(
                '//textarea[@id="script_pre"]')
        e.click()
        e.send_keys('import math\na=2+2\nprint(a)')

        e = self.driver.find_element_by_xpath(
                '//button[@id="button_script_pre"]')
        e.click()
        time.sleep(3)
        
        e = self.driver.find_element_by_xpath(
                '//textarea[@id="script_pre_output"]')
        
        text = e.get_attribute('value')

        print('script pre output')
        print(repr(e.get_attribute('id')))
        print(repr(text))

        self.assertEqual(text, '4\n')
        
        # cell
        e = self.driver.find_element_by_xpath(
                '//table[@class="htCore"]/tbody/tr/td')

        e.click()
        e.send_keys('2+2\n')

        time.sleep(3)

        print('cell')
        print(repr(e.text))

        self.assertEqual(e.text, '4')

        # cell
        e.click()
        e.send_keys('a\n')

        time.sleep(3)

        print('cell')
        print(repr(e.text))

        self.assertEqual(e.text, '4')

        # test script post
        e = self.driver.find_element_by_xpath(
                '//textarea[@id="script_post"]')
        e.click()
        e.send_keys('print(a)')

        e = self.driver.find_element_by_xpath(
                '//button[@id="button_script_post"]')
        e.click()
        time.sleep(3)
    
        e = self.driver.find_element_by_xpath(
                '//textarea[@id="script_post_output"]')

        text = e.get_attribute('value')

        print('script post output')
        print(repr(text))

        self.assertEqual(text, '4\n')

class TestDemos(ws_web_aiohttp.test_support.SeleniumTest):

    def test_demo_sum(self):

        for k, cls in ws_sheets.tests.functions.DEMOS.items():
            url = '%s%s' % (self.url_root, '/demo/' + k + '/')

            print('url = {}'.format(url))

            self.driver.get(url)

            time.sleep(3)
            
            cls._test_selenium(self.driver)



