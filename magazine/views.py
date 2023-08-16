import random

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, ListView
from .forms import CustomUserCreationForm, AddCommentForm, ImageForm, ProductCreate
from django.forms import modelformset_factory
from django.db.models import Q, Count
# Create your views here.

from .models import *

'''показать все посты'''
def products_all(request):
    model = Product.objects.all()
    categories = Category.objects.filter(parent_category=None)
    context = {
        'products': model,
        'categories': categories,
    }
    return render(request,'product_list.html',context)

'''показать посты для категории'''
def products_cat(request,cat_slug):
    model = Product.objects.filter(Q(cat__slug=cat_slug) | Q(cat__parent_category__slug=cat_slug))
    categories = Category.objects.filter(parent_category=None)
    cat_selected = Category.objects.get(slug=cat_slug)
    context = {
        'products':model,
        'categories': categories,
        'cat_selected':cat_selected,
               }
    return render(request,'product_list.html',context)

'''показать страницу для определенного поста'''
class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    slug_url_kwarg = 'product_slug'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent_category=None)
        context['comments'] = Comment.objects.filter(product = self.object)
        return context


'''страница регистрации с формой и переодрессацией после регистрациии'''
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

'''страница для редактирования постов'''
@login_required
def edit_product(request,prod_id):
    ImageFormSet = modelformset_factory(ProductImage, ImageForm, extra=3)

    product = get_object_or_404(Product,id=prod_id)
    if request.method == 'POST':
        post_form = ProductCreate(request.POST,request.FILES,instance=product)
        formset = ImageFormSet(request.POST,request.FILES,queryset=ProductImage.objects.filter(post=product))
        if post_form.is_valid() and formset.is_valid():
            post_form.save()
            for form in formset:
                if form.is_valid():
                    if 'img' in form.cleaned_data:
                        image = form.cleaned_data['img']
                        if image:
                            photo = ProductImage(post=product, img=image)
                            photo.save()


            return HttpResponseRedirect(product.get_absolute_url())
    else:
        post_form = ProductCreate(instance=product)
        formset = ImageFormSet(queryset=ProductImage.objects.none())
    context = {'postForm':post_form,'formset':formset,'title':"Обновить",}
    return render(request,'add_product.html',context)


'''страница с профилем'''
def profile(request,user_id):
    profile = CustomUser.objects.get(id=user_id)
    return render(request,'profile.html',{'profile':profile})


'''отвечает за поиск постов по заголовку'''
class SearchResponceList(ListView):
    template_name = 'product_list.html'
    context_object_name = 'products'
    """Поиск по названию товара"""

    def get_queryset(self):
         return Product.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['categories']  = Category.objects.filter(parent_category=None)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context

'''добавить комментарий'''
class AddComment(View):
    def post(self,request,id):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product_id = id
            form.save()
            return redirect('/')
        else:
            return HttpResponseRedirect('/')

'''ответить на комментарий'''
class RespondComment(View):
    def post(self,request,prod_id,com_id):
        form = AddCommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product_id = prod_id
            form.responce_id = com_id
            form.save()
            return redirect('/')
        else:
            return HttpResponseRedirect('/')


@login_required
def post(request):
    ImageFormSet = modelformset_factory(ProductImage,ImageForm,extra=3,can_delete=True)

    if request.method == 'POST':
        postform = ProductCreate(request.POST,request.FILES or None)
        formset = ImageFormSet(request.POST,request.FILES,queryset=ProductImage.objects.none())

        if postform.is_valid() and formset.is_valid():
            post_form =  postform.save(commit=False)
            post_form.owner = CustomUser.objects.get(id=request.user.id)
            post_form.save()

            for form in formset:
                if form.is_valid():
                    if 'img' in form.cleaned_data:
                        image = form.cleaned_data['img']
                        if image:
                            photo = ProductImage(post=post_form, img=image)
                            photo.save()
            messages.success(request,'Все данные были добавлены и вы успешно создали товар!')
            return HttpResponseRedirect('/')
        else:
            print(postform.errors, formset.errors)

    else:
        postform = ProductCreate()
        formset = ImageFormSet(queryset=ProductImage.objects.none())

    return render(request,'add_product.html',{'postForm':postform,'formset':formset})


