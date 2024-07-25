# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# import logging
# import scrapy
# import os
# import csv
# from scrapy.pipelines.images import ImagesPipeline

# class UnsplashScraperPipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield scrapy.Request(image_url)

#     def item_completed(self, results, item, info):
#         if not results:
#             return item

#         # Save image metadata to CSV
#         with open('image_metadata.csv', 'a', newline='') as file:
#             writer = csv.writer(file)
#             for result in results:
#                 if result[0]:
#                     image_url = result[0]['url']
#                     title = item['titles'][0] if item['titles'] else 'No Title'
#                     category = item['categories'][0] if item['categories'] else 'No Category'
#                     writer.writerow([image_url, title, category])
#         return item

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import os
import scrapy

class UnsplashScraperPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'image_url' in item:
            yield scrapy.Request(item['image_url'])

    def file_path(self, request, response=None, info=None, *, item=None):
        # Сохранение изображений с их именами
        return os.path.join('full', os.path.basename(request.url))

    def item_completed(self, results, item, info):
        if not any(result[0] for result in results):
            raise DropItem("Image download failed")
        return item
