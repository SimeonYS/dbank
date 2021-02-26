import scrapy


class DbankItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    date = scrapy.Field()
    link = scrapy.Field()
