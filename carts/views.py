from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import (ListView, DeleteView)
from django.urls import reverse, reverse_lazy
import logging

from products.models import Product


from .models import Cart, CartItem
# Create your views here.
class ListCartView(ListView):
    model = Cart

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['my_cart'] = Cart.objects.all()[0]
    #     context['products'] = Cart.objects.all()[0].products.all()
    #     return context    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            the_id = self.request.session['cart_id']
        except:
            the_id = None
        if the_id:
            cart = Cart.objects.get(id=the_id)
            context['my_cart'] = cart
        else:
            context['empty'] = True 
        return context

class DeleteCartView(DeleteView):
    model = Cart
    success_url = reverse_lazy('cart')


def update_cart(request, slug, qty):
    request.session.set_expiry(300)
    try:
        the_id = request.session['cart_id']
    except: 
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
    cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if qty == 0:
        cart_item.delete()
    else:
        cart_item.quantity = qty
        cart_item.save()


    # if not cart_item in cart.items.all():
    #     cart.add_to_cart(cart_item)
    # else:
    #     cart.remove_to_cart(cart_item)
    new_total = 0
    for item in cart.cartitem_set.all():
        line_total = item.product.price * item.quantity
        new_total += line_total
    request.session['item_total'] = cart.cartitem_set.count()
    cart.total = new_total
    cart.save()
    return HttpResponseRedirect(reverse('cart'))




    
