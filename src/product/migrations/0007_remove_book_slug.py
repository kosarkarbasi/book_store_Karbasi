# Generated by Django 3.2.6 on 2021-08-26 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_book_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='slug',
        ),
    ]
