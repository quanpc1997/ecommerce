from django.db import models

from products.models import Product
# Create your models here.

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=0, max_digits=1000, decimal_places=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        try:
            return str(self.cart.id)
        except:
            return self.product.title

class Cart(models.Model):
    total = models.DecimalField(max_digits=100, decimal_places=0, default=0)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "Card id: %s" %(self.id)

    def add_to_cart(self, product):
        self.items.add(product)
        self.save()

    def remove_to_cart(self, product):
        self.items.remove(product)
        self.save()
            

