# Generated by Django 3.1.4 on 2021-05-09 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_brand_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
        migrations.AddField(
            model_name='review',
            name='image6',
            field=models.ImageField(blank=True, null=True, upload_to='Ecommerce/Review'),
        ),
    ]
