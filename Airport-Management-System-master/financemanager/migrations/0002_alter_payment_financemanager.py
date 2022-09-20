# Generated by Django 3.2.11 on 2022-07-09 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('financemanager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='financemanager',
            field=models.ForeignKey(help_text='Finance manager', null=True, on_delete=django.db.models.deletion.CASCADE, to='financemanager.financemanager'),
        ),
    ]
