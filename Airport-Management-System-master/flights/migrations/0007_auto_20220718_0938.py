# Generated by Django 3.2.11 on 2022-07-18 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0006_auto_20220711_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientservice',
            name='client',
        ),
        migrations.RemoveField(
            model_name='clientservice',
            name='handyman',
        ),
    ]