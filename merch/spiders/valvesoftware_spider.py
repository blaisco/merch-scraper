from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from merch.items import MerchItem
from scrapy.spider import BaseSpider
from scrapy.http import Request
import string

# scrapy crawl store.valvesoftware.com

class ValvesoftwareSpider(BaseSpider):
  # class ValvesoftwareSpider(CrawlSpider):
  name = "store.valvesoftware.com"
  base_url = "http://store.valvesoftware.com/"
  allowed_domains = ["valvesoftware.com"]
  #start_urls = ["http://store.valvesoftware.com/"]
  start_urls = ["http://store.valvesoftware.com/product.php?i=P0909"]
  rules = (
    # Extract links matching 'index.php' and follow links from them 
    # (since no callback means follow=True by default).
    Rule(SgmlLinkExtractor(allow=('index\.php', )), follow=True),

    # Extract links matching 'product.php' and parse them with the spider's parse_item method
    Rule(SgmlLinkExtractor(allow=('product\.php', )), callback='parse_item'),
  )

  # def parse_item(self, response):
  def parse(self, response):
    self.log('We\'re parsing: %s' % response.url)
    # self.log(response.body)

    hxs = HtmlXPathSelector(response)
    item = MerchItem()
    
    item['url'] = response.url
    
    # Using .encode('utf-8') on certain fields because the text may contain 
    # non-ascii characters which throws a UnicodeEncodeError exception when 
    # calling urlencode.
    
    # Two divs within this div; join with a space
    product_name = hxs.select("//div[@id='product_header_box']//h3/text()").extract()
    item['name'] = string.capwords(' '.join(product_name))
    
    # Paragraph with text split by <br>'s
    description = hxs.select("//div[@id='product_info']/p/text()").extract()
    item['summary'] = description[0]
    item['description'] = ''.join(description)
    
    sale_price = None
    price = hxs.select("//div[@class='product_price']/text()").extract()
    if price:
      price = price[0]
    else:
      price = hxs.select("//div[@class='product_old_price']/text()").extract()[0]
      sale_price = hxs.select("//div[@class='product_sale_price']/text()").extract()[0]
    
    # price = price[1].replace('$','')
    sizes = hxs.select("//div[@id='size']/select/option/text()").extract()
    
    item['inventory'] = []
    if sizes:
      for size in sizes:
        item['inventory'].append({
          "color": None, 
          "size": size, 
          "price": price, 
          "sale_price": sale_price, 
          "in_stock": True
        })
    else:
      item['inventory'].append({
        "color": None, 
        "size": None, 
        "price": price, 
        "sale_price": sale_price, 
        "in_stock": True
      })
      
    item['image_urls'] = [self.base_url + hxs.select("//div[@id='product_image']/img/@src").extract()[0]]
    
    return item
  
