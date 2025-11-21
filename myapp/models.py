from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from decimal import Decimal

class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    # discount_percent = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    @property
    def price_with_vat(self):
        return self.price * Decimal('1.2')

    def apply_discount(self, percent):
        return float(self.price) * (1 - percent / 100)


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name