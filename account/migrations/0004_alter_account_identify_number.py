# Generated by Django 4.0.3 on 2022-04-19 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_alter_account_identify_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='identify_number',
            field=models.CharField(default='4933876672', max_length=10),
        ),
    ]
