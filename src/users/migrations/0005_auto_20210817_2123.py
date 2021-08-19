# Generated by Django 3.2.6 on 2021-08-17 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True, verbose_name='email address'),
        ),
    ]