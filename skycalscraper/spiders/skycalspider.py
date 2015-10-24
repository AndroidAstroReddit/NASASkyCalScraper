import scrapy

from selenium import webdriver
import time

from skycalscraper.items import SkycalscraperItem


class SkyCal(scrapy.Spider):
    name = "skycal-table"
    years = ['2015', '2016', '2017', '2018', '2019']
    time_zones = ['tzchoice-10','tzchoice-9','tzchoice-8', 'tzchoice-7', 'tzchoice-6', 'tzchoice-5']
    start_urls = ["http://eclipse.gsfc.nasa.gov/SKYCAL/SKYCAL.html"]

    def __init__(self, name=None):
        super(SkyCal, self).__init__(self)
        self.driver = webdriver.Firefox()

    def parse(self, response):
        for year in self.years:
            for time_zone in self.time_zones:
                self.driver.get(response.url)
                self.driver.find_element_by_id('jgyear').clear()
                self.driver.find_element_by_id('jgyear').send_keys('2015')
                self.driver.find_element_by_id(time_zone).click()
                self.driver.find_element_by_id('maketb').click()
                # the javascript needs to be populated so let it sleep for 3 seconds
                time.sleep(3)
                self.driver.switch_to_window(self.driver.window_handles[1])


                container = self.driver.find_element_by_id('container')
                for table in container.find_elements_by_tag_name('table'):
                    for row in table.find_elements_by_tag_name('tr'):
                        if len(row.find_elements_by_tag_name('td')) == 5:
                            if row.find_elements_by_tag_name('td')[0].text != u' ':
                                month = row.find_elements_by_tag_name('td')[0].text
                            item = SkycalscraperItem()
                            item['month'] = month
                            item['day'] = row.find_elements_by_tag_name('td')[1].text
                            item['day_of_week'] = row.find_elements_by_tag_name('td')[2].text
                            item['time'] = row.find_elements_by_tag_name('td')[3].text
                            item['event'] = row.find_elements_by_tag_name('td')[4].text
                            item['year'] = year
                            item['time_zone'] = time_zone
                            yield item
