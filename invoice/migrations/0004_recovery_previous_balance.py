# Generated by Django 4.2.11 on 2024-05-03 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0003_recovery_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='recovery',
            name='previous_balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
