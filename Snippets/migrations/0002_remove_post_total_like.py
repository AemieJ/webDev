# Generated by Django 2.1 on 2019-08-26 14:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Snippets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='total_like',
        ),
    ]