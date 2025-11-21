from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product
from django.core.cache import cache


@receiver(post_save, sender=Product)
def product_created_signal(sender, instance, created, **kwargs):
    if created:
        # Если объект только что создан
        print(f"cоздан новый продукт: {instance.name}")
    else:
        # Если объект обновлён
        print(f"Обновлён продукт: {instance.name}")

@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_products_cache(sender, **kwargs):
    cache.delete('products_list')
    print("КЭШ ТОВАРОВ ОЧИЩЕН — добавлен или изменён товар")
