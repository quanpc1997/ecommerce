from django.urls import path

from . import views

urlpatterns = [
    path('', views.ListProductView.as_view(), name='home'),
    path('s/', views.SearchProductView.as_view(), name='search'),
    path('products/<slug:slug>', views.DetailProductView.as_view(), name='detail_product'),
]