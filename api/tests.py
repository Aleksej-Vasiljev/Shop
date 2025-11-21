from django.test import TestCase

from decimal import Decimal
from myapp.models import Product
from rest_framework import status, response
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from datetime import timedelta
from django.contrib.auth.models import User


# class ProductTests(TestCase):
#     def test_price_with_vat(self):
#         product = Product(name='Phone', price=Decimal('100.00'))
#         self.assertEqual(product.price_with_vat, Decimal('120.00'))
#
#     def test_apply_discount(self):
#         product = Product(name='Phone', price=Decimal('500.00'))
#         discounted = product.apply_discount(10)
#         self.assertEqual(discounted, Decimal(450.00))
#
# class ProductIntegrationTests(APITestCase):
#     def test_create_product(self):
#         data = {'name': 'Laptop', 'price': '1000'}
#         response = self.client.post('/api/products/create/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertTrue(Product.objects.filter(name='Laptop').exists())
#
# class ProductBlackBoxTests(APITestCase):
#     def test_create_product(self):
#         data = {'name': 'Laptop', 'price': '1000.00'}
#         response = self.client.post('/api/products/create/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
# class ProductWhiteBoxTests(APITestCase):
#     def test_create_product(self):
#         product = Product(name='Laptop', price=Decimal('1000.00'))
#         result = product.price_with_vat
#         self.assertEqual(result, Decimal('1200.00'))
#
# class ProductModelTest(TestCase):
#     def test_crud_operations(self):
#         product = Product.objects.create(name='Tablet', price=Decimal('1000.00'))
#         self.assertEqual(Product.objects.count(), 1)
#
#         product.price = 900
#         product.save()
#         self.assertEqual(Product.objects.get(pk=product.pk).price, 900)
#
#         product.delete()
#         self.assertEqual(Product.objects.count(), 0)
#
# class ProductViewTests(TestCase):
#     def test_redirect_after_register(self):
#         response = self.client.post('/register/', {
#             'username': 'user',
#             'password': '123',
#             'password2': '123',
#             'email': 'test@gmail.com'
#         })
#         self.assertEqual(response.status_code, status.HTTP_302_FOUND)
#         self.assertIn('', response['Location'])
#
# #проверка, возвращает ли корректные данные
# class ProductListAPITests(APITestCase):
#     def test_list_products(self):
#         Product.objects.create(name='Phone', price=Decimal('500.00'))
#         Product.objects.create(name='Laptop', price=Decimal('1500.00'))
#         response = self.client.get('/api/products/')
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 2)
#         self.assertEqual(response.data[0]['name'], 'Phone')
#         self.assertEqual(Decimal(response.data[0]['price']), Decimal('500.00'))
#
# # тест на некорректные данные
# class ProductValidationTests(APITestCase):
#     def test_create_product_invalid_price(self):
#         data = {'name': 'BadProduct', 'price': '-100'}
#
#         response = self.client.post('/api/products/create/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertFalse(Product.objects.filter(name='BadProduct').exists())


User = get_user_model()

class SimpleJWTTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username1', password='pass123')

    def test_can_access_protected_api(self):
        token = str(AccessToken.for_user(self.user))

        response = self.client.get(
            '/api/products/',
            HTTP_AUTHORIZATION=f'Bearer {token}',
        )

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# обработка просроченного токена
class JWTTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='username2', password='pass1456')

    def test_jwt_expired(self):
        token = AccessToken.for_user(self.user)
        token.set_exp(lifetime=timedelta(seconds=-1))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.get('/api/protected/')
        self.assertEqual(response.status_code, 401)


