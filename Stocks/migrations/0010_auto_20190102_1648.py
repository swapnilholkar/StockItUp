# Generated by Django 2.1.2 on 2019-01-02 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0009_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
