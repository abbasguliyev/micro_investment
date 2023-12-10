# Generated by Django 4.2.6 on 2023-12-10 13:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entrepreneur', '0007_delete_charityfund_delete_debtfund'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrepreneurimages',
            name='image',
            field=models.ImageField(max_length=1000, upload_to='investor/entrepreneur_image/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])], verbose_name='Entrepreneur Image'),
        ),
    ]
