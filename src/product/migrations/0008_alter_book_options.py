# Generated by Django 3.2.6 on 2021-08-28 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_book_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('created',), 'verbose_name': 'کتاب', 'verbose_name_plural': 'کتاب ها'},
        ),
    ]
