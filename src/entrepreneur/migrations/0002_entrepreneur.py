# Generated by Django 4.2.5 on 2023-09-23 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_investor_referances_investor_references'),
        ('entrepreneur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entrepreneur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entrepreneurs', to='account.investor')),
            ],
        ),
    ]
