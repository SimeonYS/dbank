import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import DbankItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class DbankSpider(scrapy.Spider):
	name = 'dbank'
	start_urls = ['https://www.dbank.bg/bg/novini']

	def parse(self, response):
		post_links = response.xpath('//a[@class="news__link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@class="paginator__link paginator__link--next"]/@href').get()
		if next_page:
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//article[@class="news-text-container news-text-container--main-pic text clearfix"]//time//text()').get()
		title = response.xpath('//h1[@class="main-title"]/text()').get()
		content = response.xpath('//article[@class="news-text-container news-text-container--main-pic text clearfix"]//text()[not (ancestor::time) and not(ancestor::h1)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))


		item = ItemLoader(item=DbankItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		return item.load_item()
