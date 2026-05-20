from celery import shared_task
from django.utils import timezone
from .models import DailyStatistics
from orders.models import Order
from django.db.models import Sum

@shared_task
def compute_daily_statistics():
    today = timezone.now().date()
    orders = Order.objects.filter(created_at__date=today)
    stats, _ = DailyStatistics.objects.get_or_create(date=today)
    stats.orders_count = orders.count()
    total = orders.aggregate(total=Sum("total_price"))["total"] or 0
    stats.total_revenue = total
    stats.save()
    return {"date": str(today), "orders": stats.orders_count, "revenue": float(stats.total_revenue)}
