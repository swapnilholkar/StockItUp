# Generated by Django 2.1.2 on 2018-11-09 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0004_remove_choice_votes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_stock_id',
        ),
        migrations.AddField(
            model_name='question',
            name='question_stock_id',
            field=models.ManyToManyField(to='Stocks.StockDetail'),
        ),
    ]