# Generated by Django 4.0.3 on 2022-04-20 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0005_credit_notices_alter_credit_credit_long'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='approval',
            field=models.BooleanField(default=False),
        ),
    ]
