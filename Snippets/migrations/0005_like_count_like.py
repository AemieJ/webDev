# Generated by Django 2.1 on 2019-08-28 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Snippets', '0004_auto_20190827_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='count_like',
            field=models.IntegerField(default=0),
        ),
    ]