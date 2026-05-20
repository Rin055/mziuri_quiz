from django.db import models
from django.conf import settings
from project.products.models import Product

class Order(models.Model):
	STATUS_CHOICES = (("Pending", "Pending"), ("Completed", "Completed"), ("Cancelled", "Cancelled"))
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
	created_at = models.DateTimeField(auto_now_add=True)
	total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

	def __str__(self):
		return f"Order #{self.pk} by {self.customer.email}"


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
	product = models.ForeignKey(Product, on_delete=models.PROTECT)
	quantity = models.PositiveIntegerField()
	price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
