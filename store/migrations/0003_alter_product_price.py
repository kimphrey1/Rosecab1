# Generated by Django 3.2.25 on 2024-05-05 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True),
        ),
    ]
