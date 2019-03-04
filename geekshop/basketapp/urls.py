from django.urls import path, re_path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    re_path(r'^$', basketapp.basket, name='view'),
    re_path(r'^remove/(?P<pk>\d+)/$', basketapp.basket_remove, name='remove'),
    re_path(r'^add/(?P<product_pk>\d+)/$', basketapp.basket_add, name='add'),
    re_path(r'^update/(?P<product_pk>\d+)/(?P<quantity>\d+)/$', basketapp.basket_update, name='update'),
]
