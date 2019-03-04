from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from authapp.models import ShopUser
from django.contrib.auth.decorators import user_passes_test
from mainapp.models import ProductCategory, Product
from adminapp.forms import ShopUserRegisterAdminForm, ShopUserChangeAdminForm, CategoryEditForm, ProductEditForm
from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


# @user_passes_test(lambda x: x.is_superuser)
# def index(request):
#     title = 'admin/users'
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list,
#     }
#
#     return render(request, 'adminapp/index.html', context)


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/index.html'

    @method_decorator(user_passes_test(lambda x: x.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def user_create(request):
    title = 'users/creation'
    if request.method == 'POST':
        user_form = ShopUserRegisterAdminForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        user_form = ShopUserRegisterAdminForm()

    context = {
        'title': title,
        'form': user_form,
    }
    return render(request, 'adminapp/user_update.html', context)


def user_update(request, user_pk):
    user = get_object_or_404(ShopUser, pk=user_pk)
    title = 'users/edit'
    if request.method == 'POST':
        user_form = ShopUserChangeAdminForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:index'))
    else:
        user_form = ShopUserChangeAdminForm(instance=user)

    context = {
        'title': title,
        'form': user_form,
    }
    return render(request, 'adminapp/user_update.html', context)


def user_delete(request, pk):
    item = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        item.is_active = False
        item.save()
        return HttpResponseRedirect(reverse('admin:index'))
    return render(request, 'adminapp/user_delete.html', {'object': item})


def categories(request):
    title = 'admin/categories'
    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list,
    }

    return render(request, 'adminapp/categories.html', context)


# def category_update(request, pk):
#     category = get_object_or_404(ProductCategory, pk=pk)
#     title = 'category/edit'
#     if request.method == 'POST':
#         form = CategoryEditForm(request.POST, request.FILES, instance=category)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin:categories'))
#     else:
#         form = CategoryEditForm(instance=category)
#
#     context = {
#         'title': title,
#         'form': form,
#     }
#     return render(request, 'adminapp/category_update.html', context)


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'categories/edit'
        return context


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def catalogue(request, category_pk):
    title = 'admin/products'

    products_list = Product.objects.filter(category__pk=category_pk).order_by('name')
    # category = get_object_or_404(ProductCategory, pk=category_pk)
    # products_list = category.product_set.all().order_by('name')

    context = {
        'title': title,
        'objects': products_list,
    }

    return render(request, 'adminapp/catalogue.html', context)


# def catalogue_read(request, pk):
#     item = get_object_or_404(Product, pk=pk)
#     title = 'catalogue/view'
#     context = {
#         'title': title,
#         'object': item,
#     }
#     return render(request, 'adminapp/product_read.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


def catalogue_update(request, pk):
    item = get_object_or_404(Product, pk=pk)
    category = item.category
    title = 'categories/edit'
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin:catalogue',
                                                kwargs={
                                                    'category_pk': category.pk,
                                                }))
    else:
        form = ProductEditForm(instance=item)

    context = {
        'title': title,
        'form': form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', context)
