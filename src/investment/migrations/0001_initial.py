# Generated by Django 4.2.6 on 2023-10-30 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('entrepreneur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Amount')),
                ('profit', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Profit')),
                ('investment_date', models.DateField(auto_now_add=True, help_text='Yatırım tarixi', verbose_name='Investment date')),
                ('entrepreneur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='entrepreneur.entrepreneur')),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='account.investor')),
            ],
        ),
    ]
