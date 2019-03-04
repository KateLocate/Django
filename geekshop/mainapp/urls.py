from django.urls import path, re_path
import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    re_path(r'^$', mainapp.index, name='index'),
    re_path(r'^catalogue/$', mainapp.catalogue, name='catalogue'),
    re_path(r'^catalogue/(?P<category_pk>\d+)/$', mainapp.catalogue, name='products_in_category'),

    re_path(r'^catalogue/(?P<category_pk>\d+)/page/(?P<page>\d+)/$', mainapp.catalogue, name='page'),

    re_path(r'^product/(?P<product_pk>\d+)/$', mainapp.product, name='product'),
    re_path(r'^contacts/$', mainapp.contacts, name='contacts'),
]
