# Generated by Django 4.2.6 on 2023-12-23 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0006_investment_amount_deducated_from_balance_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='investment',
            options={'ordering': ('-investor__user__first_name',)},
        ),
        migrations.AlterModelOptions(
            name='investmentreport',
            options={'ordering': ('-investor__user__first_name',)},
        ),
    ]
