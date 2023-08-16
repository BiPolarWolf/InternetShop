import os

from django.core.files import File
from django.test import Client
from django.test.testcases import TestCase

from SHOP.settings import BASE_DIR
from magazine.views import *


class MagazineViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = CustomUser.objects.create_user(username='sergey',password='qsedwa')
        user1 = CustomUser.objects.create_user(username='snegir', password='qsedwa')
        Category.objects.create(name='sport',parent_category=None,slug='sport')
        Category.objects.create(name='winter', parent_category=Category.objects.get(id=1))
        sport_cat = Category.objects.get(id=1)
        Product.objects.create(title='sport clothes',description='sport clothes for all your family',
                               cat=sport_cat,owner=user,price=200)
        Product.objects.create(title='book Steven King', description='all about book',
                               cat=sport_cat, owner=user, price=200)

    #Проверка на выдачу главной страницы со всеми товарами
    def test_home(self):
        responce=self.client.get('/')
        self.assertEquals(responce.status_code,200)

    # проверка выдачи страницы для определенной категории
    #проверка выдачи субкатегорий нашей основной категории
    def test_category(self):
        responce=self.client.get('/categories/sport')
        self.assertEquals(responce.status_code,200)
        self.assertIn('sport clothes',responce.content.decode())
        self.assertIn('winter',responce.content.decode())

    # проверка выдачи страницы для одного продукта с описанием
    def test_product_detail(self):
        responce = self.client.get('/product/sport-clothes')
        self.assertEquals(responce.status_code,200)
        self.assertIn('sport clothes for all your family', responce.content.decode())

    # проверка работы переодесации при успешном введение данных в странице login
    # проверка выдачи страницы авторизации
    def test_login_True(self):
        responce = self.client.get('/accounts/login/')
        responce1 = self.client.post('/accounts/login/',{'username':'sergey','password':'qsedwa'})
        self.assertEquals(responce.status_code, 200)
        self.assertEquals(responce1.status_code, 302)

    # тест при неудачной авторизации
    def test_login_False(self):
        responce = self.client.post('/accounts/login/',{'username':'sergey','password':'not_right_password'})
        self.assertEquals(responce.status_code, 200)

    # проверка того что юзер вошел на сайт
    def test_user(self):
        user = CustomUser.objects.get(username='sergey')
        self.client.force_login(user=user)
        responce = self.client.get('/')
        self.assertEquals(responce.status_code, 200)
        self.assertIn('sergey',responce.content.decode())

    # проверка открытия страниц создания и редактирования постов для неавторизованных

    def test_protected_links(self):
        responce= self.client.get('/add/')
        self.assertEquals(responce.status_code, 302)
        responce1 = self.client.get('/edit/1')
        self.assertEquals(responce1.status_code, 302)

    # проверка открытия страниц создания и редактирования постов для авторизованных
    def test_protected_links_sergey(self):
        user = CustomUser.objects.get(username='sergey')
        client = Client()
        client.force_login(user=user)
        responce= client.get('/add/')
        self.assertEquals(responce.status_code, 200)
        responce1 = client.get('/edit/1')
        self.assertEquals(responce1.status_code, 200)


    # проверка открытия страниц создания и редактирования постов для авторизованных
    def test_notuniq_product(self):
        user = CustomUser.objects.get(username='sergey')
        client = Client()
        client.force_login(user=user)
        sport_cat = Category.objects.get(id=1)
        responce = client.post('/add/', {'title':'sport clothes2','description':'sport clothes for all your family',
                               'cat':sport_cat,'owner':user,'price':200})
        self.assertEquals(responce.status_code,200)

    # поиск по ключу sport
    def test_search(self):
        client = Client()
        responce = client.get(f"/search/?q=sport")
        self.assertIn('sport clothes',responce.content.decode())
        self.assertNotIn('book Steven King',responce.content.decode())

    # поиск по ключу Steven
    def test_search1(self):
        client = Client()
        responce = client.get(f"/search/?q=Steven")
        self.assertNotIn('sport clothes',responce.content.decode())
        self.assertIn('book Steven King',responce.content.decode())


    # проверка страницы профиль
    def test_profile(self):
        client = Client()
        responce = client.get(f"/profile/2/")
        self.assertEquals(responce.status_code,200)
        self.assertIn('snegir',responce.content.decode())
'''
    def test_form_submission(self):
        # Создаем объект для тестирования
        test_data = {
            'title': 'TestProduct',
            'description': 'aboutTestProduct',
            'cat': 'value2',
            'price': 'value2',
            'discount': 'value2',
            'img': 'value2',
            # ...
        }
        response = self.client.post(reverse('your-view-name'), test_data)

        # Проверяем, что объект был создан
        self.assertEqual(response.status_code, 200)  # Проверяем статус код
        self.assertTrue(YourModel.objects.filter(field1='value1').exists())  # Проверяем создание объекта

        # Проверяем, что форма отображается на странице
        self.assertIsInstance(response.context['form'], YourForm)

        # Проверяем, что после успешной отправки формы перенаправление происходит на нужную страницу
        self.assertRedirects(response, reverse('success-view-name'))'''