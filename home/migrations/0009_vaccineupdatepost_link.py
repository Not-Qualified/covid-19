# Generated by Django 3.1.2 on 2020-10-16 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_vaccineupdatepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaccineupdatepost',
            name='link',
            field=models.URLField(default='https://www.google.com/search?q=covid-19', max_length=700),
            preserve_default=False,
        ),
    ]