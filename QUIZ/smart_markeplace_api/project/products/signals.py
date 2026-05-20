from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import update_out_of_stock_status

@receiver(post_save, sender=Product)
def check_stock(sender, instance, **kwargs):
    # ensure status correctness asynchronously for heavy loads
    update_out_of_stock_status.delay(instance.id)
    