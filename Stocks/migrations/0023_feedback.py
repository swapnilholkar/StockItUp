# Generated by Django 2.1.2 on 2019-03-29 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Stocks', '0022_auto_20190320_1522'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ease_of_use', models.CharField(max_length=201)),
                ('stat_info', models.CharField(max_length=201)),
                ('experience', models.CharField(max_length=201)),
                ('like', models.CharField(max_length=201)),
                ('not_like', models.CharField(max_length=201)),
                ('feedback_posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
