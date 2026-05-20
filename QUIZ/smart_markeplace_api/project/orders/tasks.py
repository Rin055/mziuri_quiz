from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order

@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.get(pk=order_id)
        subject = f"Order Confirmation #{order.id}"
        message = f"Thank you for your order #{order.id}. Total: {order.total_price}."
        recipient = [order.customer.email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=True)
    except Order.DoesNotExist:
        return None
