from django.contrib import admin
from .models import DailyStatistics


@admin.register(DailyStatistics)
class DailyStatisticsAdmin(admin.ModelAdmin):
	list_display = ("date", "orders_count", "total_revenue")
	ordering = ("-date",)
