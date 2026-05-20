from rest_framework import serializers
from .models import Order, OrderItem
from project.products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product")

    class Meta:
        model = OrderItem
        fields = ("product_id", "quantity", "price_at_purchase")
        read_only_fields = ("price_at_purchase",)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("id", "customer", "created_at", "total_price", "status", "items")
        read_only_fields = ("customer", "total_price", "status", "created_at")

    def create(self, validated_data):
        request = self.context.get("request")
        items_data = validated_data.pop("items")
        order = Order.objects.create(customer=request.user, status="Pending")
        total = 0
        for item in items_data:
            product = item["product"]
            qty = item["quantity"]
            if product.stock < qty:
                raise serializers.ValidationError({"stock": f"Product {product.id} does not have enough stock"})
            price = product.price
            product.stock -= qty
            product.save()
            OrderItem.objects.create(order=order, product=product, quantity=qty, price_at_purchase=price)
            total += price * qty
        order.total_price = total
        order.status = "Completed"
        order.save()
        from .tasks import send_order_confirmation_email
        send_order_confirmation_email.delay(order.id)
        return order
