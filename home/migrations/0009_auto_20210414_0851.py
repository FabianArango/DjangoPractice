# Generated by Django 3.1.7 on 2021-04-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_userpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='creationDate',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='userpost',
            name='creationDate',
            field=models.DateTimeField(),
        ),
    ]
