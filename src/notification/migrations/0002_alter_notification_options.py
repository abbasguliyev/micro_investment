# Generated by Django 4.2.6 on 2023-12-17 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'ordering': ('-pk',)},
        ),
    ]
