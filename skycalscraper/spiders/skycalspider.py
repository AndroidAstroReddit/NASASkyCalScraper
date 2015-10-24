import scrapy

from selenium import webdriver
import time

from skycalscraper.items import SkycalscraperItem


class SkyCal(scrapy.Spider):
    name = "skycal-table"

    start_urls = ["http://eclipse.gsfc.nasa.gov/SKYCAL/SKYCAL.html"]


    def __init__(self, name=None):
        super(SkyCal, self).__init__(self)
        self.driver = webdriver.Firefox()


    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('jgyear').click()
        self.driver.find_element_by_id('jgyear').send_keys('2015')
        self.driver.find_element_by_id('maketb').click()
        #the javascript needs to be populated so let it sleep for 1 second
        time.sleep(1)


        table = self.driver.find_element_by_tag_name('table')
        for row in table.find_element_by_tag_name('tr'):
            if row.find_elements_by_tag_name('td')[0].extract() != '':
                month = row.find_elements_by_tag_name('td')[0].text()
            item = SkycalscraperItem()
            item['month'] = month
            item['day'] = row.find_elements_by_tag_name('td')[1].text()
            item['day_of_week'] = row.find_elements_by_tag_name('td')[2].text()
            item['time'] = row.find_elements_by_tag_name('td')[3].text()
            item['event'] = row.find_elements_by_tag_name('td')[4].text()
            yield item

