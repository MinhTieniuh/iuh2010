from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from unitop.spiders.UnitopCourseCrawler_Update import UnitopCourseSpider


process = CrawlerProcess(get_project_settings())
process.crawl(UnitopCourseSpider)
process.start()
