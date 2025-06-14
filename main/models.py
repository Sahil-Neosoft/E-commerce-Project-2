from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.cart.models import Cart


class User(AbstractUser):
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def get_active_cart(self):
        """Get or create active cart for user"""
        cart, created = Cart.objects.get_or_create(
            user=self,
            defaults={'session_id': None}
        )
        return cart

    def get_orders(self):
        """Get user's orders ordered by creation date"""
        return self.orders.all().order_by('-created_at')

