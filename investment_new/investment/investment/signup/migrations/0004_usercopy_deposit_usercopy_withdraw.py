# Generated by Django 5.0.6 on 2024-07-13 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0003_deposit'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercopy',
            name='deposit',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='usercopy',
            name='withdraw',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]