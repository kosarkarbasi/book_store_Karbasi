# Generated by Django 3.2.6 on 2021-08-20 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountpercentdiscount',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='amountpercentdiscount',
            name='max_discount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
