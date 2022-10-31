# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from itemadapter import ItemAdapter


settings = get_project_settings()


class ExportPipeline:

    def open_spider(self, spider):
        self.client = MongoClient(settings.get('MONGO_URL'))
        self.db = self.client[settings.get('MONGO_DB_NAME')]
        self.file = open(settings.get('CSV_FILE'), 'w', newline='')
        self.writer = csv.writer((self.file))
        self.has_title = False

    def close_spider(self, spider):
        self.client.close()
        self.file.close()

    def process_item(self, item, spider):
        item = ItemAdapter(item).asdict()
        self.db[settings.get('MONGO_COLLECTION_NAME')].insert_one(item)

        if not self.has_title:
            self.writer.writerow([cols for cols in item])
            self.has_title = True
        self.writer.writerow([(isinstance(entries, str) and entries or '; '.join([et for et in entries])).replace(',', '')
                              for cols, entries in item.items() if cols != '_id'])

