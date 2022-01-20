import scrapy
from scrapy.http import HtmlResponse
from ..items import BooksProjectItem
import re

class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/search/?q=фантастика&newproduct=1']
    start_page_num = 1
    set_links = set()
    stop_when_repeat_book = False


    def parse(self, response: HtmlResponse):
        books = response.xpath("//div[@class='catalog__product-list-holder']//a[contains(@class, 'product-card__name')]")

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
            next_page = re.sub(r'/page-\d+/', f'/page-{self.start_page_num}/', next_page)
        else:
            next_page = re.sub(r'/\?', f'/page-{self.start_page_num}/?', next_page)

        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        book = {}
        book['book_name'] = response.xpath("//h1/text()").get()
        book['authors'] = response.xpath("//div[@class='product-characteristic__item']//a[contains(@href, '/author')]/text()").getall()

        if response.xpath("//span[contains(@class, 'product-sidebar-price__price-old')]"):
            book['price'] = response.xpath("//span[contains(@class, 'product-sidebar-price__price-old/text()").get()
            book['discount_price'] = response.xpath("//span[contains(@class, 'product-sidebar-price__price')]/text()").get()
        else:
            book['price'] = response.xpath("//span[contains(@class, 'product-sidebar-price__price')]/text()").get()
            book['discount_price'] = None
        book['rating'] = response.xpath("//div[contains(@class, 'rating-widget')]//span[@class='rating-widget__main-text']/text()").getall()
        book['link'] = response.url
        yield BooksProjectItem(**book)
