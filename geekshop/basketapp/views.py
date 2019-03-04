from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from mainapp.models import Product
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.template.loader import render_to_string


def basket(request):
    basket_items = request.user.basket_set.all()
    context = {
        'title': 'basket',
        'basket_items': basket_items,
    }
    return render(request, 'basketapp/basket.html', context)


@login_required
def basket_add(request, product_pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('main:product',
                                            kwargs={
                                                'product_pk': product_pk
                                            }))

    product = get_object_or_404(Product, pk=product_pk)
    old_basket_item = Basket.objects.filter(user=request.user, product=product).first()

    if old_basket_item:
        old_basket_item.quantity += 1
        old_basket_item.save()

    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
# request.META.get('HTTP_REFERER') - возвращает предыдущую гиперссылку


def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk, user=request.user)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_update(request, product_pk, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        new_basket_item = Basket.objects.filter(pk=int(product_pk)).first()

        if quantity > 0:
            new_basket_item.quantity = quantity
            new_basket_item.save()

        else:
            new_basket_item.delete()

        basket_items = request.user.basket_set.all().order_by('product__category')
        context = {
            'basket_items': basket_items,
        }

        result = render_to_string('basketapp/includes/inc__basket_list.html', context)

        return JsonResponse({
            'result': result,
        })

