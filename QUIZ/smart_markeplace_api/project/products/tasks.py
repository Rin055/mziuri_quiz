from celery import shared_task
from .models import Product

@shared_task
def update_out_of_stock_status(product_id):
    try:
        p = Product.objects.get(pk=product_id)
        if p.stock == 0 and p.status != "Out of Stock":
            p.status = "Out of Stock"
            p.save(update_fields=["status"])
        elif p.stock > 0 and p.status != "Available":
            p.status = "Available"
            p.save(update_fields=["status"])
    except Product.DoesNotExist:
        return None
