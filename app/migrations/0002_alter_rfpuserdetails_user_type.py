# Generated by Django 5.1.6 on 2025-03-29 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rfpuserdetails',
            name='user_type',
            field=models.CharField(choices=[('vendor', 'Vendor'), ('admin', 'Admin')], default='vendor', max_length=10),
        ),
    ]
