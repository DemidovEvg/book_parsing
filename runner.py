# II вариант
# 1) Создать пауков по сбору данных о книгах с сайтов labirint.ru и/или book24.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация должна складываться в базу данных

from pydoc import cram
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from books_project import settings
from books_project.spiders.labirint import LabirintSpider
from books_project.spiders.book24 import Book24Spider

if __name__ == '__main__':
    
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process.crawl(LabirintSpider)
    process.crawl(Book24Spider)
    process.start()