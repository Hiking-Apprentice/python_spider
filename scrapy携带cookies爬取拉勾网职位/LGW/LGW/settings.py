# -*- coding: utf-8 -*-

# Scrapy settings for LGW project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'LGW'

SPIDER_MODULES = ['LGW.spiders']
NEWSPIDER_MODULE = 'LGW.spiders'
# LOG_LEVEL='DEBUG'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'LGW (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
    'Cookie':'user_trace_token=20200220092116-595a7bb5-9842-4428-95f3-086a26b28db2; LGUID=20200220092116-ea26f786-1e84-4380-a1e5-f272da747409; _ga=GA1.2.179793190.1582161678; index_location_city=%E4%B8%8A%E6%B5%B7; lagou_utm_source=B; _gid=GA1.2.1429308555.1584457578; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22170602f6a0938e-01e139f7f46b82-b383f66-1638720-170602f6a0ad97%22%2C%22%24device_id%22%3A%22170602f6a0938e-01e139f7f46b82-b383f66-1638720-170602f6a0ad97%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; JSESSIONID=ABAAAECABGFABFFA1234DE7112529620807B5F7DB8B812B; WEBTJ-ID=20200318160102-170eca8fde83fa-0172e055df3e9a-4313f6a-1638720-170eca8fde9ae0; LGSID=20200318160103-d0faaae8-1bba-47d7-a177-40e14f1e3a4d; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584509624,1584509628,1584510282,1584518464; X_MIDDLE_TOKEN=a324578cc9b25f415ae243858b41c4da; ab_test_random_num=0; gate_login_token=ddea3187ae4f7b34c6d417780422ae19459bcbb4e444a000f08735904c5c6c8c; LG_HAS_LOGIN=1; _putrc=91716C7CF3F6E711123F89F2B170EADC; login=true; hasDeliver=0; privacyPolicyPopup=false; _gat=1; unick=%E7%94%A8%E6%88%B78677; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; TG-TRACK-CODE=index_search; SEARCH_ID=79f5a9f8fd484f8d9e830b7f0d723771; X_HTTP_TOKEN=1f9f122afbbf969273332548518fdf6f0ae1901f8c; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1584523338; LGRID=20200318172218-3d36e9bf-02ef-4bf3-b95f-7662a26a65c3'
}
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'LGW.middlewares.LgwSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'LGW.middlewares.RandomUserAgent': 1,

}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'LGW.pipelines.LgwPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
USER_AGENTS = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
]