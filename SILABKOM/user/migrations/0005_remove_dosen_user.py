# Generated by Django 4.2.1 on 2023-06-23 02:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_dosen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dosen',
            name='user',
        ),
    ]
