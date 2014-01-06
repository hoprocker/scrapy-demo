# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, Compose
from types import ListType, TupleType
import re

DEBUG = True

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

### helpers for the loader
def strip_extra(val):
    """
    strip whitespace and the outer <span> elements
    """
    if type(val) in [ListType, TupleType] and len(val) > 0:
        val = val[0]
    if isinstance(val, basestring):
        val = val.strip()
        srch_val = re.search("<span[^>]+>(.*)<\/span>", val)
        if srch_val:
            return srch_val.groups()[0]
        return val
    return val
def parse_num_fld(val):
    if DEBUG:
        print "VAL: %s" % val
    if type(val) in [ListType, TupleType] and len(val) > 0:
        val = val[0]
    if isinstance(val, basestring):
        try:
            return float(re.sub("[^0-9.]+", "", val))
        except ValueError:
            pass
    return val
def parse_baths(val):
    """
    extract only 'Full' baths
    """
    if DEBUG:
        print "VAL: %s" % val
    if type(val) in [ListType, TupleType] and len(val) > 0:
        val = val[0]
    if isinstance(val, basestring):
        real_val = re.search("([0-9.]+)[a-z><\/]+ Full", val)
        if real_val:
            if DEBUG:
                print "real_val: %s" % (real_val.groups(),)
            return float(real_val.groups()[0])
    return val

def print_output(val):
    if DEBUG:
        print "output val: %s" % val
    return val
        
class ListingItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = Compose(strip_extra, print_output)

    sqft_in = Compose(strip_extra, parse_num_fld, print_output)
    beds_in = Compose(strip_extra, parse_num_fld, print_output)
    price_in = Compose(strip_extra, parse_num_fld, print_output)
    baths_in = Compose(strip_extra, parse_baths, print_output)
