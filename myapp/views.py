from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
import requests
from django.core.cache import cache

from .forms import RegisterForm, OrderRequestForm
from .models import Product, Category
from decimal import Decimal


# ---------------- Регистрация пользователя ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('products')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


# ---------------- Список товаров ----------------
# def products_view(request):
#     categories = Category.objects.all()
#     category_id = request.GET.get('category')
#     products = Product.objects.all()
#     if category_id:
#         products = products.filter(category_id=category_id)
#
#     usd_rate = cache.get('usd_rate')
#     for p in products:
#        p.price_usd = round(p.price / usd_rate, 2) if usd_rate else None
#
#     return render(request, 'products.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': category_id
#     })
#

# ---------------- Детали товара ----------------
@login_required(login_url='/login/')

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    usd_rate = cache.get('usd_rate')

    price_usd = round(product.price / usd_rate, 2) if usd_rate else None

    return render(request, 'product_detail.html', {
        'product': product,
        'price_usd': price_usd
    })


# ---------------- КОРЗИНА ----------------
@login_required(login_url='/login/')
def add_to_cart(request, product_id):
    """Добавление товара в корзину (только для авторизованных)."""
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')


@login_required(login_url='/login/')
def remove_from_cart(request, product_id):
    """Удаление товара из корзины."""
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
    request.session['cart'] = cart
    return redirect('cart_view')


@login_required(login_url='/login/')
def cart_view(request):
    """Показ корзины с итоговой суммой."""
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total = sum(p.price for p in products)
    return render(request, 'cart.html', {'products': products, 'total': total})


# ---------------- Оформление заказа ----------------
@login_required(login_url='/login/')
def order_request(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if not cart:
        return redirect('cart_view')

    if request.method == 'POST':
        form = OrderRequestForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']

            product_list = "\n".join([p.name for p in products])

            send_telegram_message(
                f"Новый заказ ✅\n"
                f"Имя: {name}\n"
                f"Телефон: {phone}\n"
                f"Товары:{product_list}"
            )

            request.session['cart'] = []
            return render(request, 'order_success.html')
    else:
        form = OrderRequestForm()

    total = sum(p.price for p in products)
    return render(request, 'order_request.html', {
        'form': form,
        'products': products,
        'total': total
    })


# ---------------- Функция отправки Telegram ----------------
def send_telegram_message(msg):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {"chat_id": chat_id, "text": msg}
    requests.post(url, data=data)


# ---------------- Кэш списка товаров ----------------
# def products_view(request):
#     products = cache.get('products_list')
#
#     if not products:
#         print("КЭШ ПУСТ — грузим из БД")  # можно удалить
#         products = list(Product.objects.all())
#         cache.set('products_list', products, 60 * 60)  # кэш на 1 час
#
#     categories = Category.objects.all()
#     category_id = request.GET.get('category')
#
#     if category_id:
#         products = [p for p in products if str(p.category_id) == category_id]
#
#     return render(request, 'products.html', {
#         'products': products,
#         'categories': categories,
#         'selected_category': category_id
#     })

def products_view(request):
    # --- Получаем продукты из кэша или из БД
    products = cache.get('products_list')
    if products is None:
        products = list(Product.objects.all())
        cache.set('products_list', products, 60 * 60)  # кэш на 1 час

    # --- Фильтр по категориям
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    if category_id:
        products = [p for p in products if str(p.category_id) == category_id]

    # --- Получаем курс USD из кэша и приводим к Decimal
    usd_rate = cache.get('usd_rate')
    if usd_rate is not None:
        usd_rate = Decimal(str(usd_rate))

    # --- Добавляем динамическое поле price_usd
    for p in products:
        if usd_rate:
            p.price_usd = round(p.price / usd_rate, 2)
        else:
            p.price_usd = None

    return render(request, 'products.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_id
    })