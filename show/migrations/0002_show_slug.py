# Generated by Django 3.0.5 on 2020-04-27 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='slug',
            field=models.SlugField(default=1, unique=True, verbose_name='Slug'),
            preserve_default=False,
        ),
    ]
