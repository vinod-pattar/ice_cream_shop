# Generated by Django 5.1 on 2024-08-16 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_alter_product_brand_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
