# Generated by Django 3.1 on 2020-08-24 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='phone',
            field=models.CharField(default=' ', max_length=110),
        ),
    ]
