# Generated by Django 5.0.2 on 2025-05-28 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_alter_ecommercedemo_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ecommercedemo',
            name='category',
            field=models.CharField(blank=True, choices=[('single', 'Single Vendor'), ('multi', 'Multivendor')], max_length=30),
        ),
    ]
