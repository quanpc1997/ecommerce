from django.contrib import admin

from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'total', 'active', 'updated']
    list_editable = ['active']
    class Meta:
        model = Cart

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'quantity']
    list_editable = ['quantity']
    class Meta:
        model = CartItem

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)