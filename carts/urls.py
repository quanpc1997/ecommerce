from django.urls import path

from . import views

urlpatterns = [
    path('cart/', views.ListCartView.as_view(), name='cart'),
    path('cart/<slug:slug>', views.update_cart, name='update_cart'),
]