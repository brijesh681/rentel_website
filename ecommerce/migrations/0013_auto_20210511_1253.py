# Generated by Django 3.1.4 on 2021-05-11 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0012_accessories'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessories',
            name='free_size_length',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accessories',
            name='free_size_weight',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accessories',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='material',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='neck_design',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
