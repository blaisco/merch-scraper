import ConfigParser
import json
from decimal import *
from urllib2 import Request, urlopen, URLError
from urllib import urlencode, quote
from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

MERCH_PRODUCT_URL = 'http://localhost:3000/api/products'
CONFIG_FILE = 'settings.ini'

class MerchPipeline(object):
  def process_item(self, item, spider):
    return item

class InventoryPipeline(object): 
  def process_item(self, item, spider):
    
    # Convert price from $13.78 to 1378
    def price_str_to_int(price):
      price = str(price).replace('$','')
      price = Decimal(price)
      price = str(int(price * 100))
      return price
      
    sizes = {
      'S' : 'S',
      'M' : 'M',
      'L' : 'L',
      'XL' : 'XL',
      '2XL' : '2XL',
      '3XL' : '3XL',
      'XXL' : '2XL',
      'XXXL' : '3XL', 
      'Small' : 'S',
      'Medium' : 'M',
      'Large' : 'L',
      'X-Large' : 'XL',
      '2X-Large' : '2XL',
      '3X-Large' : '3XL'
    }
    
    if item['inventory']:
      for inv in item['inventory']:
        if inv['price']:
          inv['price'] = price_str_to_int(inv['price'])
        if inv['sale_price']:
          inv['sale_price'] = price_str_to_int(inv['sale_price'])
        if inv['size']:
          inv['size'] = sizes[inv['size']]
        
    return item
    
class HTTPPostPipeline(object):  
  def __init__(self):
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    self.key = config.get('api','key')
  
  def process_item(self, item, spider):
    data = dict()
    data["product"] = json.dumps(dict(item))
    data["key"] = self.key
    
    req = Request(MERCH_PRODUCT_URL, urlencode(data))
    try:
      response = urlopen(req)
    except URLError, e:
      if hasattr(e, 'reason'):
        log.msg('Failed to reach the server. Reason: ' + e.reason, level=log.ERROR)
      elif hasattr(e, 'code'):
        log.msg('Server couldn\'t fulfill the request. Error code: ' + str(e.code), level=log.ERROR)
    # else:
      # All good. Rejoice!
    
    return item
