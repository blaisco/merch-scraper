# Scrapy settings for tutorial project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'merchbot'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['merch.spiders']
NEWSPIDER_MODULE = 'merch.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
  'scrapy.contrib.pipeline.images.ImagesPipeline',
  'merch.pipelines.InventoryPipeline',
  'merch.pipelines.HTTPPostPipeline'
]

IMAGES_STORE = '/tmp/scrapy/images/'

DOWNLOAD_DELAY = 2 # seconds
