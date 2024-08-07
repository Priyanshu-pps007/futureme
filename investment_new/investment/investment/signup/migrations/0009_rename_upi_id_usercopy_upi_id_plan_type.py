# Generated by Django 4.2.3 on 2024-07-15 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signup', '0008_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercopy',
            old_name='UPI_ID',
            new_name='upi_id',
        ),
        migrations.AddField(
            model_name='plan',
            name='type',
            field=models.CharField(blank=True, choices=[('D', 'Daily'), ('W', 'Weekly'), ('M', 'Monthly')], max_length=20, null=True),
        ),
    ]
