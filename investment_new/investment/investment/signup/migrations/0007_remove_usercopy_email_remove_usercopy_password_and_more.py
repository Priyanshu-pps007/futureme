# Generated by Django 4.2.3 on 2024-07-15 09:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signup', '0006_alter_usercopy_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercopy',
            name='email',
        ),
        migrations.RemoveField(
            model_name='usercopy',
            name='password',
        ),
        migrations.AddField(
            model_name='usercopy',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]