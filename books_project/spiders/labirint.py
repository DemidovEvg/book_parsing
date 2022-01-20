import scrapy
from ..items import BooksProjectItem
from scrapy.http import HtmlResponse
import re

class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = [r'https://www.labirint.ru/search/фантастика/?stype=0']
    start_page_num = 1
    set_links = set()
    stop_when_repeat_book = False

    def parse(self, response: HtmlResponse):
        books = response.xpath("//a[@class='product-title-link']/@href")
        if not books or self.stop_when_repeat_book:
            return

        for link in books:
            if link.get() in self.set_links:
                self.stop_when_repeat_book = True
            else:
                self.set_links.add(link.get())
            yield response.follow(link, callback=self.book_parse)

        self.start_page_num +=1 
        next_page = response.url
        if 'page' in response.url:
            next_page = re.sub(r'&page=\d+', f'&page={self.start_page_num}', next_page)
        else:
            next_page = f'{next_page}&page={self.start_page_num}'

        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book = {}
        book['book_name'] = response.xpath("//h1/text()").get()
        book['authors'] = response.xpath("//div[contains(text(), 'Автор: ') and contains(@class, 'authors')]/a/text()").getall()
        book['price'] = response.xpath("//span[@class='buying-priceold-val-number']/text()").get()
        book['discount_price'] = response.xpath("//span[@class='buying-pricenew-val-number']/text()").get()
        book['rating'] = response.xpath("//div[@id='rate']/text()").get()
        book['link'] = response.url
        yield BooksProjectItem(**book)
