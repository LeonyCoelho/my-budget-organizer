# Generated by Django 5.0.4 on 2024-04-11 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_my_budget', '0003_globalsettings_remove_account_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='globalsettings',
            name='currency',
            field=models.CharField(choices=[('R$', 'Reais (BRL)'), ('$', 'US Dollar (USD)')], default='BRL', max_length=3),
        ),
    ]
