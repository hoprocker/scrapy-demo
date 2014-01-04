# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ListingItem(Item):
    street_address = Field()
    city = Field()
    region = Field()
    postal = Field()
    price = Field()
    beds = Field()
    baths = Field()
    sqft = Field()
    property_type = Field()
