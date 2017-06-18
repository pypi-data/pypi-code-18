import unittest

import ws_sheets.tests.functions
import ws_web_aiohttp.test_support

def suite():
    class Test(ws_web_aiohttp.test_support.SeleniumTest):
        def test(self):
            url = '{}/demo/{}/'.format(self.url_root, self.name)

            print('url = {}'.format(url))

            self.driver.get(url)
            
            self.google_login()

            self.o._test_selenium(self.driver)

    suite = unittest.TestSuite()
    for name, cls in ws_sheets.tests.functions.DEMOS.items():
        t = type('Test_'+name, (Test,), {'name':name,'o':cls()})
        suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(t))
    
    return suite

if __name__=='__main__':
    runner = unittest.TextTestRunner(verbosity=2, failfast=True)
    runner.run(suite())


 
