# Generated by Django 3.2.6 on 2021-08-20 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_city_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='province',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.province'),
        ),
    ]
