# Generated by Django 2.1.2 on 2018-11-07 16:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0003_auto_20181107_1620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
    ]
