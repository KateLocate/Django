from django.shortcuts import render, get_object_or_404
from mainapp.models import ProductCategory, Product
import random

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket_set.all()

    context = {
        'title': 'home',
        'basket': basket,
    }
    return render(request, 'mainapp/index.html', context)


def catalogue(request, category_pk=None, page=1):
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket_set.all()

    category_links = ProductCategory.objects.all()

    if category_pk:
        if category_pk == '0':
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category__pk=category_pk)

        products = Paginator(products, 2)
        try:
            products = products.page(page)
        except PageNotAnInteger:
            products = products.page(1)
        except EmptyPage:
            products = products.page(products.num_pages)

        context = {
            'title': 'products',
            'category_links': category_links,
            'products': products,
            'basket': basket,
            'category_pk': category_pk,
        }
        return render(request, 'mainapp/catalogue.html', context)

    else:
        any_category = random.choice(ProductCategory.objects.all())
        same_products = Product.objects.exclude(category__pk=any_category.pk).order_by('-price','-category')[:3]

        context = {
            'title': 'products',
            'category_links': category_links,
            'any_category': any_category,
            'same_products': same_products,
            'basket': basket,
        }
        return render(request, 'mainapp/catalogue.html', context)


def product(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    category_links = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = request.user.basket_set.all()

    context = {
        'title': 'product',
        'category_links': category_links,
        'basket': basket,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)


def contacts(request):

    contact = [
        {
            'address': '151 West 34th Street, New York, NY',
            'phone': '8-158-198-200',
            'email': 'info_ny@pro-fashion.com',
            'map': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3594.4096226374904!2d-73.99154966221086!3d40.'
                   '75045070332367!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a94d88162b%3A0x2d91fb85460'
                   '28ba4!2s151+W+34th+St%2C+New+York%2C+NY+10001%2C+USA!5e0!3m2!1sen!2sru!4v1542378595586'
        },
        {
            'address': '175 Berkeley St Boston, MA 02116, USA',
            'phone': '8-555-888-123',
            'email': 'info_boston@pro-fashion.com',
            'map': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14437.68971948382!2d-71.08790165449938!3d42.3'
                   '4794774504444!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89e37a749ef3e70b%3A0x598d86e5f4e9'
                   '7fba!2zMTc1IEJlcmtlbGV5IFN0LCBCb3N0b24sIE1BIDAyMTE2LCDQodCo0JA!5e0!3m2!1sru!2sru!4v1543507160758'
        },
    ]

    context = {
        'title': 'address and feedback',
        'contact': contact,
    }
    return render(request, 'mainapp/contacts.html', context)
