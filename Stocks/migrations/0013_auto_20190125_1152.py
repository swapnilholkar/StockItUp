# Generated by Django 2.1.2 on 2019-01-25 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0012_response_response_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='response_posted',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
