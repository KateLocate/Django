from django.db import models
from django.conf import settings
from mainapp.models import Product


class Basket(models.Model):
    # settings.AUTH_USER_MODEL - наша модель пользователя, ссылка на которую лежит в settings.py
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='quantity', default=0)
    add_datetime = models.DateTimeField(verbose_name='time', auto_now_add=True)

    def _get_product_cost(self):

        return self.product.price * self.quantity

    product_cost = property(_get_product_cost)

    def _get_total_quantity(self):
        _items = self.user.basket_set.all()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))

        return _total_quantity

    total_quantity = property(_get_total_quantity)

    def _get_total_cost(self):
        _items = self.user.basket_set.all()
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))

        return _total_cost

    total_cost = property(_get_total_cost)
