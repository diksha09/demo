# Generated by Django 2.1 on 2019-07-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_notifications_notificationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentdetails',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
