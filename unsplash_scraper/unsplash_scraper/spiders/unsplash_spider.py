# import scrapy
# from unsplash_scraper.items import UnsplashScraperItem

# class UnsplashSpider(scrapy.Spider):
#     name = 'unsplash_spider'
#     allowed_domains = ['unsplash.com']
#     start_urls = ['https://unsplash.com/']

#     def parse(self, response):
#         # Extract image URLs and metadata
#         for image in response.xpath('//figure'):
#             item = UnsplashScraperItem()
#             item['image_urls'] = [image.xpath('.//a/@href').get()]
#             item['titles'] = [image.xpath('.//figcaption/text()').get()]
#             item['categories'] = ['example_category'] 
#             yield item

#             # Follow pagination links
#             next_page = response.xpath('//a[@class="next"]/@href').get()
#             if next_page:
#                 yield response.follow(next_page, callback=self.parse)

from unsplash_scraper.items import UnsplashScraperItem
import scrapy

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_spider"
    start_urls = [
        'https://unsplash.com']

    def start_requests(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/95.0'
        }
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
 
    def parse(self, response):
        # Извлекаем ссылки на страницы изображений
        image_page_links = response.xpath('//a[contains(@href, "/photos/")]/@href').getall()
        
        for link in image_page_links:
            absolute_link = response.urljoin(link)
            yield scrapy.Request(absolute_link, callback=self.parse_image_page)

        # Переход на следующую страницу, если есть
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_image_page(self, response):
        img_url = response.xpath('//img[@class="_2zEKz"]/@src').get()
        title = response.xpath('//title/text()').get()
        category = response.xpath('//meta[@property="og:type"]/@content').get() or 'unknown'

        if img_url:
            img_url = response.urljoin(img_url)
            item = UnsplashScraperItem()
            item['image_urls'] = [img_url]
            item['titles'] = [title]
            item['categories'] = [category]
            yield item
