# Generated by Django 3.0.2 on 2020-02-01 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200201_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
