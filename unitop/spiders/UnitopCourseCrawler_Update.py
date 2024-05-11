import scrapy
from unitop.items import UnitopItem

class UnitopCourseSpider(scrapy.Spider):
    name = "UUnitopAppCrawler_Update"
    allowed_domains = ["books.toscrape.com"]

    def start_requests(self):
        yield scrapy.Request(url='https://books.toscrape.com/catalogue/category/books/mystery_3/index.html', callback=self.parse)
        
    def parse(self, response):
        courseList = response.xpath('//div/descendant::ol/li/article/div/a/@href').getall()
        for courseItem in courseList:
            item = UnitopItem()
            item['courseUrl'] = response.urljoin(courseItem)
            request = scrapy.Request(url = response.urljoin(courseItem), callback=self.parseCourseDetailPage)
            request.meta['datacourse'] = item
            yield request
            

    def parseCourseDetailPage(self, response):
        item = response.meta['datacourse']
        item['product_main'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/h1))').get()
        item['rating'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/p[@class="price_color"]))').get()
        item['in_stock'] = response.xpath('normalize-space(string(//div[@class="col-sm-6 product_main"]/p[@class="instock availability"]))').get()
        item['star'] = response.xpath("substring-after(//div[contains(@class, 'product_main')]/p[contains(@class, 'star-rating')]/@class, 'star-rating ')").extract_first()
        item['description'] = response.xpath('normalize-space(string(//article[@class="product_page"]/p))').get()
        item['upc'] = response.xpath('normalize-space(string(//th[text()="UPC"]/following-sibling::td))').get()
        item['product_type'] = response.xpath('normalize-space(string(//th[text()="Product Type"]/following-sibling::td))').get()
        item['price_exc'] = response.xpath('normalize-space(string(//th[text()="Price (excl. tax)"]/following-sibling::td))').get()
        item['price_inc'] = response.xpath('normalize-space(string(//th[text()="Price (incl. tax)"]/following-sibling::td))').get()
        item['tax'] = response.xpath('normalize-space(string(//th[text()="Tax"]/following-sibling::td))').get()
        item['availability'] = response.xpath('normalize-space(string(//th[text()="Availability"]/following-sibling::td))').get()
        item['nor'] = response.xpath('normalize-space(string(//th[text()="Number of reviews"]/following-sibling::td))').get()

        yield item