# Generated by Django 3.1.2 on 2020-10-16 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_vaccineupdatepost_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vaccineupdatepost',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
