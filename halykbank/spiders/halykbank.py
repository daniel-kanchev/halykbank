import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from halykbank.items import Article


class HalykbankSpider(scrapy.Spider):
    name = 'halykbank'
    start_urls = ['https://halykbank.ge/ka/news']

    def parse(self, response):
        links = response.xpath('//div[@class="news"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="newsdetail__date"]//text()').getall()
        date = [text for text in date if text.strip()]
        date = " ".join(date).strip()

        content = response.xpath('//div[@class="page__text"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
