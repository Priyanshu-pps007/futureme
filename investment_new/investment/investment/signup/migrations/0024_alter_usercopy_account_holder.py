# Generated by Django 4.2.3 on 2024-07-17 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0023_deposit_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercopy',
            name='account_holder',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]