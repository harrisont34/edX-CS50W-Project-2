# Generated by Django 3.1.4 on 2021-02-24 17:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listcomment_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listcomment',
            name='timestamp',
        ),
    ]
