# Generated by Django 3.1.7 on 2021-04-12 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profilePic',
            field=models.FileField(default='uploads/images/default.gif', upload_to='uploads/images/'),
        ),
    ]
