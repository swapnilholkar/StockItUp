# Generated by Django 2.1.2 on 2019-04-23 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0025_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exstockinfo',
            name='stock_company',
        ),
        migrations.DeleteModel(
            name='ExStockInfo',
        ),
    ]
