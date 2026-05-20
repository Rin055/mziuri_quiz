from django.db import models


class DailyStatistics(models.Model):
    date = models.DateField(unique=True)
    orders_count = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=14, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.date} - orders: {self.orders_count} revenue: {self.total_revenue}"
from django.db import models

# Create your models here.
