from django.urls import path, re_path
import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    # re_path(r'^$', adminapp.index, name='index'),
    re_path(r'^$', adminapp.UsersListView.as_view(), name='index'),

    re_path(r'^user/create/$', adminapp.user_create, name='user_create'),
    re_path(r'^user/update/(?P<user_pk>\d+)/$', adminapp.user_update, name='user_update'),
    re_path(r'^user/delete/(?P<pk>\d+)/$', adminapp.user_delete, name='user_delete'),

    re_path(r'^catalogue/(?P<category_pk>\d+)/$', adminapp.catalogue, name='catalogue'),
    # re_path(r'^catalogue/read/(?P<pk>\d+)/$', adminapp.catalogue_read, name='product_read'),
    re_path(r'^catalogue/read/(?P<pk>\d+)/$', adminapp.ProductDetailView.as_view(), name='product_read'),
    re_path(r'^catalogue/update/(?P<pk>\d+)/$', adminapp.catalogue_update, name='product_update'),

    re_path(r'^categories/$', adminapp.categories, name='categories'),
    # re_path(r'^category/update/(?P<pk>\d+)/$', adminapp.category_update, name='category_update'),
    re_path(r'^category/update/(?P<pk>\d+)/$', adminapp.ProductCategoryUpdateView.as_view(), name='category_update'),
    re_path(r'^category/delete/(?P<pk>\d+)/$', adminapp.ProductCategoryDeleteView.as_view(), name='category_delete'),
]
