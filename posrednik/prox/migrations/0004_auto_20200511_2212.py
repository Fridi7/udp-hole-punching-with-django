# Generated by Django 3.0.3 on 2020-05-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prox', '0003_address_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='status',
        ),
        migrations.AlterField(
            model_name='address',
            name='message',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
