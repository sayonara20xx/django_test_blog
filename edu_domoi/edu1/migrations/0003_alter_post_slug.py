# Generated by Django 3.2.8 on 2021-10-12 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edu1', '0002_auto_20210727_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, max_length=150, unique=True),
        ),
    ]
