# Generated by Django 4.2.3 on 2023-08-12 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magazine', '0005_remove_productimage_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photos',
            field=models.ManyToManyField(blank=True, related_name='product', to='magazine.productimage'),
        ),
    ]
