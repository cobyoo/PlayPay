# Generated by Django 3.1.1 on 2020-10-27 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Proj', '0003_text_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avg_time',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='food_choice',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='region',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.IntegerField(default=0),
        ),
    ]
