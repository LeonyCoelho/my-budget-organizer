# Generated by Django 5.0.4 on 2024-05-06 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_my_budget', '0006_transaction_target_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='recurrent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='target_account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transactions_received', to='app_my_budget.account'),
        ),
    ]
