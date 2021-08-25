from users.models import Customer
from .models import ShoppingCart


def cart(request):
    if request.user.is_anonymous:
        device = request.COOKIES['device']
        customer, created = Customer.objects.get_or_create(device=device)
    else:
        customer = request.user

    cart_items = ShoppingCart.objects.filter(order__customer=customer)
    return {'cart_items': cart_items}
