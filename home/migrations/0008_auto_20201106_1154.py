# Generated by Django 3.1.2 on 2020-11-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_contactuslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactuslist',
            name='message',
            field=models.TextField(max_length=5000),
        ),
    ]