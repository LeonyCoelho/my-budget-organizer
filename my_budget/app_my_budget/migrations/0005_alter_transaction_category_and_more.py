# Generated by Django 5.0.4 on 2024-04-12 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_my_budget', '0004_alter_globalsettings_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_my_budget.transactioncategory'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='paid',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='recurrent',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subcategory',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app_my_budget.transactionsubcategory'),
        ),
    ]
