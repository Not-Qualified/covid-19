# Generated by Django 3.1.2 on 2020-10-10 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_hospitalregister_hospital_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospitalregister',
            name='insurance_facility',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='YES', max_length=3),
        ),
        migrations.AlterField(
            model_name='hospitalregister',
            name='ventilator_facility',
            field=models.CharField(choices=[('YES', 'Yes'), ('NO', 'No')], default='YES', max_length=3),
        ),
    ]