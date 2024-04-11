# Generated by Django 5.0.4 on 2024-04-11 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_my_budget', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='currency',
            field=models.CharField(choices=[('R$', 'Reais (BRL)'), ('$', 'US Dollar (USD)')], max_length=3),
        ),
    ]
