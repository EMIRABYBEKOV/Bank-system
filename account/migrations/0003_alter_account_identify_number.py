# Generated by Django 4.0.3 on 2022-04-19 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_identify_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='identify_number',
            field=models.CharField(default='7727670495', max_length=10),
        ),
    ]
