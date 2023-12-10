# Generated by Django 4.2.6 on 2023-12-10 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_companybalance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investor',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=1000, null=True, upload_to='investor/profile_pictures/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])], verbose_name='Profile Picture'),
        ),
    ]
