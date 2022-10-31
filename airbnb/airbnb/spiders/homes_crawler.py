import scrapy
from selenium.webdriver.common.by import By

from ..items import HomeItem
from ..utils import get_chromedriver


class HomesCrawlerSpider(scrapy.Spider):
    name = 'homes_crawler'
    allowed_domains = ['www.airbnb.com']
    pagination = True

    # The links to the 3 locations
    urls = [
            'https://www.airbnb.com/s/Fayetteville--Arkansas--United-States/homes',
            'https://www.airbnb.com/s/Rogers--Arkansas--United-States/homes',
            'https://www.airbnb.com/s/Springdale--Arkansas--United-States/homes',
            ]

    # Lazy loading links that won't load until in view
    Lazy_loading_items = [(By.XPATH, '//section/div[3]/div/span/span')]

    @property
    def start_urls(self):
        """I intend to set the start_urls as function attr to control and get all the links to scrape"""
        for url in self.urls:
            urls = self.get_urls(url)
            while True:
                try:
                    yield next(urls)
                except StopIteration:
                    break

    def get_urls(self, site):
        """
            gets all the home links on each page (locations)
        """
        driver = get_chromedriver() # get a Chrome browser instance to render the javascript content
        driver.get(site)

        while True:
            # all the distinct links to the homes
            homes = driver.waiter(driver.EC.presence_of_all_elements_located((By.CLASS_NAME, 'rfexzly.dir.dir-ltr')))
            for links in {links.get_attribute('href') for links in homes}:
                yield links
            if not self.pagination:
                break

            # Pagination; following the next page
            current_window = driver.current_url
            driver.waiter(driver.EC.presence_of_element_located((By.CSS_SELECTOR, 'a._1bfat5l'))).click()
            if driver.current_url == current_window:
                break

        driver.quit()

    def parse(self, response):

        """Open a Chrome instance on each home links and scrap all the home data"""
        url = response.url
        driver = get_chromedriver()
        driver.get(url)

        # Bring the required lazy loading content in view
        for items in self.Lazy_loading_items:
            driver.execute_script("arguments[0].scrollIntoView();",
                                  driver.waiter(driver.EC.presence_of_element_located((items))))

        # creates the home item instance and render it with the scraped data
        home = HomeItem()
        home.parse(driver)
        driver.quit()
        yield home
