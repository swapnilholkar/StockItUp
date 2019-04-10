# Generated by Django 2.1.2 on 2018-11-12 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0006_auto_20181109_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='choice',
            name='question',
        ),
        migrations.RemoveField(
            model_name='choice',
            name='stock',
        ),
        migrations.RemoveField(
            model_name='question',
            name='pub_date',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_stock_id',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.AddField(
            model_name='response',
            name='questionid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stocks.Question'),
        ),
        migrations.AddField(
            model_name='response',
            name='stockid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Stocks.StockDetail'),
        ),
    ]
