# Generated by Django 2.1.2 on 2018-11-07 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0002_stockdetail'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExStockInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=200)),
                ('ex_target_price', models.FloatField(max_length=200)),
                ('stock_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stocks.StockDetail')),
            ],
        ),
        migrations.AddField(
            model_name='choice',
            name='stock',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Stocks.StockDetail'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='question_stock_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Stocks.StockDetail'),
            preserve_default=False,
        ),
    ]
