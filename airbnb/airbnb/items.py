# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from selenium.webdriver.common.by import By

from .utils import Renderer


class HomeItem(scrapy.Item, Renderer):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name_of_listing = scrapy.Field()
    listing_id = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()
    bedrooms = scrapy.Field()
    bathrooms = scrapy.Field()
    beds = scrapy.Field()
    accommodation_total = scrapy.Field()
    listing_amenities = scrapy.Field()
    ratings = scrapy.Field()
    host_name = scrapy.Field()
    host_id = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    # room = scrapy.Field()
    room_type = scrapy.Field()
    picture_url = scrapy.Field()

    class Meta:
        fields = {
            'name_of_listing': ('CSS', 'h1._fecoyn4'),
            'listing_id': ('XPATH', '//section/div[2]/div[2]/div[1]/a'),
            'city': ('CSS', 'span._9xiloll'),
            'state': ('CSS', 'span._9xiloll'),
            'country': ('CSS', 'span._9xiloll'),
            'bedrooms': ('XPATH', '//ol/li[2]/span[2]'),
            'bathrooms': ('XPATH', '//ol/li[4]/span[2]'),
            'beds': ('XPATH', '//ol/li[3]/span[2]'),
            'accommodation_total': ('CSS', 'span._tyxjp1'),
            'host_name': ('XPATH', '//section/div[1]/div[2]/h2'),
            'host_id': ('XPATH', '//section/div[1]/div[1]/div/a'),
            'latitude': ('XPATH', '//section/div[3]/div[4]/div[2]/div/div/div[14]/div/a'),
            'longitude': ('XPATH', '//section/div[3]/div[4]/div[2]/div/div/div[14]/div/a'),
            # room = scrapy.Field()
            'room_type': ('XPATH', '//section/div/div/div/div[1]/div/h2'),
            'picture_url': ('XPATH', '//*[@id="FMP-target"]///img'),
            'ratings': ('XPATH', '//div/div[1]/div[4]/div/div/div/div[2]/section/div[2]/div/div///raw'),
            "listing_amenities": ('XPATH',
                                  '//section/div[@class="b6xigss dir dir-ltr"]/button[@class="b65jmrv v7aged4 dir dir-ltr"]///raw'),
        }

    def get_country(self, data):
        return data.split(', ')[-1]

    def get_city(self, data):
        return data.split(', ')[0]

    def get_state(self, data):
        return data.split(', ')[1]

    def get_longitude(self, data):
        return data.split('=')[1].split(',')[1].split('&')[0]

    def get_latitude(self, data):
        return data.split('=')[1].split(',')[0]

    def get_host_id(self, data):
        return data.split('/')[-1]

    def get_host_name(self, data):
        return data.split('by')[-1]

    def get_listing_amenities(self, data):
        data[0].execute_script("arguments[0].click();", data[1])
        amenities = data[0].waiter(data[0].EC.presence_of_all_elements_located((By.CLASS_NAME, '_11jhslp')))
        return {els.find_element(By.CLASS_NAME, '_14i3z6h').text:
                    [el.text for el in els.find_elements(By.CLASS_NAME, '_gw4xx4')] for els in amenities}

    def get_ratings(self, data):
        return {**{el.find_element(By.CLASS_NAME, '_y1ba89').text: el.find_element(By.CLASS_NAME, '_4oybiu').text
                for el in data[1].find_elements(By.CLASS_NAME, '_a3qxec')},
                **{'review_count': data[0].find_element(By.CLASS_NAME, '_1qx9l5ba').text}
                }

    def get_listing_id(self, data):
        return data.split('/')[4]
