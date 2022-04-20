# Generated by Django 4.0.3 on 2022-04-20 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_account_identify_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='cards',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='account',
            name='identify_number',
            field=models.CharField(default='0794781894', max_length=10),
        ),
    ]
