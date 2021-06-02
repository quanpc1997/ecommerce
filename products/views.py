from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView)
from django.utils import timezone

import logging

from .models import Product, ProductImage

# Create your views here.

class ListProductView(ListView):
    model = Product

    def get_queryset(self):
        return Product.objects.all()

class DetailProductView(DetailView):
    model = Product
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_request = get_object_or_404(Product, slug=self.kwargs.get('slug'))
        product_img = get_object_or_404(ProductImage, product=product_request)
        context['product_img'] = product_img
        return context

class SearchProductView(ListView):
    model = Product
    template_name = 'products/product_search.html'

    def get_queryset(self):
        try:
            q = self.request.GET.get('q')
        except:
            q = None
        object_list = Product.objects.filter(title__icontains=q)
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q')
        logging.info('[',__name__ ,']: ', context['q'])
        return context

    # def search(request):
    #     try:
    #         q = request.GET.get('q')
    #     except:
    #         q = None
    #     if q:
    #         template = 'products/product_list.html'
    #         context = {'query', p}
    #     else:
    #         template = 'products/product_list.html'
    #         context = {}

    #     return render(request, template, context)

    
    
#################################
#################################


