from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = (("Available", "Available"), ("Out of Stock", "Out of Stock"))
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.status = "Out of Stock"
        else:
            self.status = "Available"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
