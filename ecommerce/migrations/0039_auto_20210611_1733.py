# Generated by Django 3.1 on 2021-06-11 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0038_auto_20210611_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image1',
            field=models.FileField(blank=True, upload_to='Ecommerce/images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image2',
            field=models.FileField(blank=True, upload_to='Ecommerce/images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image3',
            field=models.FileField(blank=True, upload_to='Ecommerce/images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image4',
            field=models.FileField(blank=True, upload_to='Ecommerce/images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image5',
            field=models.FileField(blank=True, upload_to='Ecommerce/images'),
        ),
    ]
