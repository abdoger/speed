from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Product

@receiver(post_save, sender=Product)
def update_product_cache(sender, instance, **kwargs):
    cache_key = f"pro__{instance.id}"
    cache.set(cache_key, instance, timeout=60*60)  # ساعة واحدة

@receiver(post_delete, sender=Product)
def delete_product_cache(sender, instance, **kwargs):
    cache_key = f"pro__{instance.id}"
    cache.delete(cache_key)
