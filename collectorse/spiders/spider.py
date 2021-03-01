import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import CollectorseItem
from itemloaders.processors import TakeFirst


class CollectorseSpider(scrapy.Spider):
	name = 'collectorse'
	start_urls = ['https://www.collector.se/om-collector/pressreleaser/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="excerpt-container regulatory-information"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="article-body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="excerpt-date-stamp"]//text()').get()
		if date:
			date = re.findall(r'\d+\s[a-z]+,\s\d{4}', date)[0]

		item = ItemLoader(item=CollectorseItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
