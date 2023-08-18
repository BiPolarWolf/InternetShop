from django.contrib.auth.models import  AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from pytils.translit import slugify
from django.core.exceptions import ValidationError
import uuid


# create path in media for images special for uniq users
def user_directory_path(instance,filename):
    return f'user_{0}/{1}'.format(instance.owner.username,filename)

# create path in media for images special for products (if delete error )
def product_images_path(instance,filename):
    return f'product_{0}/{1}'.format(instance.product.title,filename)


# create path in media for images in ProductImages model
def get_image_filename(instance, filename):
    title = instance.post.title
    slug = slugify(title)
    return "post_images/%s-%s" % (slug, filename)

# generation uniq slug for models in  custom save() method (Product model upper)
def generate_unique_slug(title):
     base_slug = slugify(title)
     unique_id = str(uuid.uuid4())[:8]  # Возьми первые 8 символов из UUID (модуль для помощи создания уникальных слагов)
     return f'{base_slug}-{unique_id}'

# model for each Product
class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    slug = models.SlugField(max_length=250,unique=True,db_index=True)
    img = models.ImageField(verbose_name='Главное изображение',upload_to='img/%Y-%m-%d/',blank=True, null=True)
    owner = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
    status_have = models.BooleanField(default=True)
    cat = models.ForeignKey('Category',on_delete=models.CASCADE)
    price = models.IntegerField( validators=[
            MinValueValidator(100),
        ],verbose_name='Цена')
    discount = models.IntegerField( validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],blank=True,null=True,verbose_name='Скидка в процентах')
    discounted_price = models.IntegerField(blank=True,null=True, verbose_name='Экономия')
    sell_price = models.IntegerField(blank=True,null=True,verbose_name='цена со скидкой')

    @property
    def discounted_price(self):
        return ((self.price) * (self.discount)) / 100

    @property
    def sell_price(self):
        return (self.price) - (self.discounted_price)


    # если пользователь не загрузил картинку то вместо нее будет картинка из инета нейтральная
    @property
    def img_url(self):
        if self.img and hasattr(self.img,'url'):
            return self.img.url
        else:
            return 'https://pskovokb.ru/templates/yootheme/cache/4c/no-phono-4c3d352d.jpeg'



    # create uniq slag for each product
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = generate_unique_slug(self.title) # здесь используется функция которую мы написали над моделью Product
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})




# модель для добавления дополнительных изображений к нашим товарам
class ProductImage(models.Model):
    post = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='images')
    img = models.ImageField(verbose_name='Дополнительное Изображение',upload_to=get_image_filename)
    # используется уникальный путь который мы прописали для медиа файлов выше




    class Meta:
        verbose_name= 'фото товара'
        verbose_name_plural = 'фото товара'

class Category(models.Model):
    parent_category=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20,verbose_name='cat_name')
    slug = models.SlugField(max_length=20,unique=True,db_index=True)

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = generate_unique_slug(self.name)  # здесь тоже используется функция для генерации уникальных слагов
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

# Пользоватьель с картинкой и полями для Имени , Фамилии и Емайла
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to=f'avatar/%Y/%m/%d',blank=True, null=True)

    def __str__(self):
        return self.username


    # Если пользователь не загружает картинку то мы берем ее поумолчанию из интернета
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar,'url'):
            return self.avatar.url
        else :
            return 'https://pic.onlinewebfonts.com/svg/img_165779.svg'

    @property
    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.id})



# модель для создания комментариев
class Comment(models.Model):

    responce = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='response')
    # responce поле это поле для ответа на другой комментарий и таким образом формируется связь между двумя экземплярами одной модели


    author = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField('комментарий')
    date = models.DateTimeField(auto_now=True)

    class CommentManager(models.Manager):
        def all(self):
            """
            Список статей (SQL запрос с фильтрацией для страницы списка статей)
            """
            all= self.get_queryset().select_related('author', 'product').all()

            return all.prefetch_related('responce')