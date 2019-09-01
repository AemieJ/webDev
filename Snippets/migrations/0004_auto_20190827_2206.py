# Generated by Django 2.1 on 2019-08-27 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Snippets', '0003_post_vote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='vote',
        ),
        migrations.AddField(
            model_name='like',
            name='post',
            field=models.ForeignKey(on_delete='CASCADE', to='Snippets.Post'),
        ),
    ]
