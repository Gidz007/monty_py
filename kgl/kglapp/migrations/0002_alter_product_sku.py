# Generated by Django 5.2 on 2025-04-28 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kglapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
