# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RealtortestItem(Item):
    address = Field()
    price = Field()
    bedrooms = Field()
    bathrooms = Field()
    sqft = Field()
    prop_type = Field()
