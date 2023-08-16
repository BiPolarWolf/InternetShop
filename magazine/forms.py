from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Product, Comment, ProductImage
from django.db import models


class ProductCreate(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['cat'].empty_label = 'Не выбрано'


    class Meta:
        model = Product
        fields = ('title','description','cat','price','discount','img')


class ImageForm(forms.ModelForm):

    class Meta:
        model = ProductImage
        fields = ('img', )

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username','avatar','first_name','last_name')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email', 'username','avatar')

class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)