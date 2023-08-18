"""
URL configuration for SHOP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import urls

from SHOP import settings
from magazine.views import products_all, ProductDetailView, products_cat, SignUpView, profile, \
    edit_product, SearchResponceList, AddComment, RespondComment, post, DeleteProduct

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',products_all , name = 'home'),
    path('categories/<slug:cat_slug>',products_cat,name='category'),
    path('product/<slug:product_slug>',ProductDetailView.as_view(),name='product'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('add/',post,name='add_product'),
    path('edit/<int:prod_id>',edit_product,name='edit_product'),
    path('search/',SearchResponceList.as_view(),name = 'search'),
    path('review/<int:id>',AddComment.as_view(),name='add_review'),
    path('delete/<int:product_id>',DeleteProduct.as_view(),name='delete_product'),
    path('review/<int:prod_id>/<int:com_id>',RespondComment.as_view(),name='respond_review'),
]

if settings.DEBUG:
    urlpatterns = [
        # ...
        path("__debug__/", include("debug_toolbar.urls")),
    ]+urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)