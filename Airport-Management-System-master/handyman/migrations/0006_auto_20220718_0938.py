# Generated by Django 3.2.11 on 2022-07-18 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_auto_20220711_1118'),
        ('flights', '0007_auto_20220718_0938'),
        ('handyman', '0005_auto_20220713_1503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkappointments',
            old_name='ELECTRICIAN',
            new_name='handyman',
        ),
        migrations.AddField(
            model_name='checkappointments',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.client'),
        ),
        migrations.AddField(
            model_name='handymanprofile',
            name='ClientService',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='flights.clientservice'),
        ),
    ]
