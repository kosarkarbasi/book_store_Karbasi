from order.models import Order


def user_orders(customer_id):
    orders = Order.objects.filter(customer_id=customer_id)
    return orders
