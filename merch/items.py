# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class MerchItem(Item):
  url = Field()
  name = Field()
  short_desc = Field()
  description = Field()
  inventory = Field()
  features = Field()
  image_urls = Field()
  images = Field() # leave empty, will be auto-populated
