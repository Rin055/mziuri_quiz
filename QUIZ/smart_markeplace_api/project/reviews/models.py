from django.db import models
from django.conf import settings
from project.products.models import Product

class Review(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="review")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	rating = models.PositiveSmallIntegerField()
	comment = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ("product", "user")

	def save(self, *args, **kwargs):
		if not (1 <= self.rating <= 5):
			raise ValueError("Rating must be between 1 and 5")
		super().save(*args, **kwargs)
