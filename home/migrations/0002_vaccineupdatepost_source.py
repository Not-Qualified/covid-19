# Generated by Django 3.1.2 on 2020-10-16 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccineupdatepost',
            name='source',
            field=models.CharField(default='Google', max_length=250),
            preserve_default=False,
        ),
    ]
