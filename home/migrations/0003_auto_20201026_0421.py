# Generated by Django 3.1.2 on 2020-10-26 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_vaccineupdatepost_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalregister',
            name='address',
            field=models.TextField(max_length=500),
        ),
    ]
