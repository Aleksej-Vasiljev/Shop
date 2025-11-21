from django import forms
from django.contrib.auth.models import User

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'in_stock', 'category']


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class OrderRequestForm(forms.Form):
    name = forms.CharField(max_length=50, label="Ваше имя")
    phone = forms.CharField(max_length=20, label="Ваш номер телефона")
