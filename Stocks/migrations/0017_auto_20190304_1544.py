# Generated by Django 2.1.2 on 2019-03-04 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0016_auto_20190304_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdetail',
            name='company_logo',
            field=models.ImageField(default='default.png', upload_to='logos'),
        ),
    ]