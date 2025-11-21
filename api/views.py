from pprint import pprint

from django.core.cache import cache
from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from myapp.models import Product
from rest_framework.views import APIView

from api.serializers import ProductSerializer, RegisterSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@api_view(['GET'])
def test_api(request):
    products = Product.objects.all()
    category = request.query_params.get('category')
    if category:
        products = products.filter(category_id=category)
    data = [
        {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        } for product in products
    ]
    return Response(data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        return Response({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'price_with_vat': product.price_with_vat
        })


class ProductListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(30))
    def get(self, request):
        print(">>> get")
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductCreateAPIView(APIView):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        pprint(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def set_cookie_example(request):
    response = Response({'message': 'Cookie установлено'})
    response.set_cookie(
        key='user_token',
        value='12345abcdef',
        max_age=15,
        httponly=True
    )
    return response


@api_view(['GET'])
def get_cookie_example(request):
    token = request.COOKIES.get('user_token')
    if token:
        return Response({'message': 'Cookie найден', 'token': token})
    return Response({'message': 'Cookie не найден'}, status=404)

class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"username": request.user.username})


