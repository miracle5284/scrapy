
from selenium.webdriver import Chrome, ChromeOptions

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .settings import SELENIUM_AGENT
from .variables import SELENIUM_MAPS


class Renderer:

    def parse(self, driver):
        """Gets the attr location on the webpage and set the attr on the home obj"""
        fields = self.Meta.fields
        for field, el_map in fields.items():
            try:
                data = self.get_element(driver, el_map)
                data = hasattr(self, f'get_{field}') and getattr(self, f'get_{field}')(data) or get_ascii(data)
            except:
                data = ''
            self.__setitem__(field, data)

    @staticmethod
    def get_element(driver, element):
        """returns web elements at the given location"""
        if isinstance(driver, WebDriver):

            by, ref = element
            ref_path = ref.split('///')
            ref = None if len(ref_path) == 1 else ref_path[1]
            html_element = driver.waiter(driver.EC.presence_of_element_located((SELENIUM_MAPS[by], ref_path[0])))
            if ref == 'img':
                return html_element.get_attribute('src')
            elif ref == 'raw':
                return driver, html_element
            elif element[1].endswith('/a'):
                return html_element.get_attribute('href')
            return html_element.text


def get_chromedriver():
    """returns a Chrome browser instance"""
    options = ChromeOptions()
    options.headless = True
    driver = Chrome(SELENIUM_AGENT, options=options)
    driver.waiter, driver.EC = WebDriverWait(driver, 30).until, EC
    return driver


def get_ascii(string):
    """returns pure ascii strings for csv"""
    return string.encode('ascii', 'ignore').decode()
