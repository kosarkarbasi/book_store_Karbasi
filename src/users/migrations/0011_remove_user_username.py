# Generated by Django 3.2.6 on 2021-08-27 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_address_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]