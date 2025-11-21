from faker import Faker
import random
from .models import Product, Category

fake = Faker('ru_RU')


def run():
    # Создаём категории (если их ещё нет)
    category_names = ['Ноутбуки', 'Смартфоны', 'Аксессуары', 'Гаджеты']
    categories = []
    for name in category_names:
        cat, created = Category.objects.get_or_create(name=name)
        categories.append(cat)


    # Создаём несколько случайных продуктов
    for _ in range(50):
        cat = random.choice(categories)
        Product.objects.create(
            name=fake.word().capitalize() + ' ' + cat.name,
            description=fake.sentence(nb_words=8),
            price=round(random.uniform(100, 2000), 2),
            in_stock=random.choice([True, False]),
            category=cat
        )

    print("Данные успешно созданы!")