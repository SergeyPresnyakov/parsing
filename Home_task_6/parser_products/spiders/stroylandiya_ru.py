import scrapy
from scrapy.http import HtmlResponse
from parser_products.items import ParserProductsItem


class StroylandiyaRuSpider(scrapy.Spider):
    name = 'stroylandiya_ru'
    allowed_domains = ['stroylandiya.ru']
    start_urls = [
        'https://stroylandiya.ru/catalog/laminat/',
        'https://stroylandiya.ru/catalog/gipsokarton/',
        'https://stroylandiya.ru/catalog/dushevye-kabiny-poddony-ugolky/',
        ]

 
    def parse(self, response:HtmlResponse):
        
        
        next_page = response.xpath('//li[@class="fb-pagination__page fb-pagination__active"]/following-sibling::*[1]/a/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)


        products_links = response.xpath('//a[@class="fb-product-card__title-inner"]/@href').getall()
        for link in products_links:
            yield response.follow(link, callback=self.pars_products)
        
        print('\n########################\n%s\n########################\n'%response.url)


    def pars_products(self, response:HtmlResponse):
              
        products_name = response.css('h1::text').get()
        products_link = response.url
        products_price_1 = response.xpath("//div[@class='dc-row -md p_product_price']//div/div[contains(@class, 'h1')]/text()").get()
        products_price_2 = response.xpath("//div[@class='dc-row -md p_product_price']//div/div[contains(@class, 'h2')]/text()").get()


        # print('\n************************\n%s\n%s\n%s\n%s\n************************\n'%(


        yield ParserProductsItem(
            name = products_name,
            link = products_link,
            price_1 = products_price_1,
            price_2 = products_price_2)
            
    