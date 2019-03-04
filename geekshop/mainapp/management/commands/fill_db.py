from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Product
from authapp.models import ShopUser

import os
import json


JSON_PATH = 'mainapp/json'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='UTF-8') as infile:
        return json.load(infile)


class Command(BaseCommand):

    help = 'Fill DB new data'

    def handle(self, *args, **options):

        categories = load_from_json('categories')
        print(categories)

        ProductCategory.objects.all().delete()
        categories_objs = []
        for category in categories:
            categories_objs.append(ProductCategory(**category))

        ProductCategory.objects.bulk_create(categories_objs)

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:
            category_name = product['category']
            # Получаем категорию по имени
            # _category = ProductCategory.objects.get(name=category_name)
            _category = ProductCategory.objects.filter(name=category_name).first()
            # Заменяем название категории объектом
            product['category'] = _category
            Product(**product).save()

        # Создаем суперпользователя при помощи менеджера модели
        # _superuser = User.objects.filter(username='django').first()

        _superuser = ShopUser.objects.filter(username='django').first()
        if not _superuser:
            ShopUser.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains', age=25)
            print('SU created')
