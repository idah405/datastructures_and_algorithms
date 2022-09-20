# Generated by Django 3.2.11 on 2022-07-09 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0003_auto_20220709_2056'),
        ('handyman', '0002_alter_handyman_user_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='handyman',
            options={'verbose_name': 'handyman', 'verbose_name_plural': 'handyman'},
        ),
        migrations.AlterModelOptions(
            name='handymanfeedback',
            options={'verbose_name': 'handyman Feedback', 'verbose_name_plural': 'handyman Feedback'},
        ),
        migrations.AlterModelOptions(
            name='handymanprofile',
            options={'verbose_name': 'handyman Profile', 'verbose_name_plural': 'handyman Profiles'},
        ),
        migrations.RemoveField(
            model_name='handymanprofile',
            name='ClientService',
        ),
        migrations.AddField(
            model_name='handymanprofile',
            name='Service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='flights.service'),
        ),
    ]
