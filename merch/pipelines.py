import json
import uuid
import time
import ConfigParser
from httplib2 import Http
from urllib import urlencode

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
      price = price.replace('$','')
      price = float(price)
      price = int(price * 100)
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
    
#~ class RabbitMQPipeline(object):
  #~ def __init__(self):
    #~ self.pc = PikaClient()
  #~ 
  #~ def process_item(self, item, spider):
    #~ def message_wrapper(item):
      #~ message = {
          #~ "message_id": str(uuid.uuid4()),
          #~ "timestamp": int(time.time()),
          #~ "message_type": "Product",
          #~ "body": dict(item)}
      #~ return message
    #~ 
    #~ self.pc.publish(json.dumps(message_wrapper(item)))
    #~ return item
    
class HTTPPipeline(object):
  def __init__(self):
    config = ConfigParser.ConfigParser()
    config.read(CONFIG_FILE)
    self.key = config.get('api','key')
  
  def process_item(self, item, spider):
    data = dict(item)
    data["key"] = self.key
    
    h = Http()
    resp, content = h.request(MERCH_PRODUCT_URL, "POST", urlencode(data))
    return item
