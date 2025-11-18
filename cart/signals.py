from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Cart, CartItem
from django.conf import settings

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user = instance)


@receiver([post_save, post_delete], sender = CartItem)
def update_total_price(sender, instance, **kwargs):

    cart = instance.cart
    items = cart.cart_items.all()

    if items > 0:
        total =  sum(item.price * item.quantity for item in items if item.price and item.quantity is not None)

    cart.total_price = total
    cart.save(update_fields = ["total_price"])
