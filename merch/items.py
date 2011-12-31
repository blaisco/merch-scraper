# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MerchItem(Item):
  merchant_url = Field()
  url = Field()
  name = Field()
  description = Field()
  inventory = Field()
  image_urls = Field()
  images = Field() # leave empty, will be auto-populated
