# Generated by Django 3.2.6 on 2021-08-17 18:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_alter_shoppingcart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoppingcart',
            name='customer',
        ),
    ]