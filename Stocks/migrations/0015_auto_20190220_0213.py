# Generated by Django 2.1.2 on 2019-02-20 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0014_stockdetail_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdetail',
            name='company_logo',
            field=models.ImageField(default='default.png', upload_to='logos'),
        ),
    ]
