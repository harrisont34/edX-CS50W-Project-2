# Generated by Django 3.1.4 on 2021-02-25 18:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]