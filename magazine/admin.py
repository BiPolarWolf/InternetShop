from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *
# Register your models here.



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',),}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',),}

admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username','email','avatar']
    add_fieldsets = (
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email','avatars')})

    )


admin.site.register(ProductImage)
admin.site.register(Comment)