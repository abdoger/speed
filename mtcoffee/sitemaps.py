from django.contrib.sitemaps import  Sitemap

from django.shortcuts import reverse

from product.models import Product

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index','addindex','signin','signup','add_to_cart','cart','payment','show_orders','order_complted']
    
    def location(self, item):
        return reverse(item)
class ProductViewSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
    