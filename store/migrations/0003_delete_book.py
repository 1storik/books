# Generated by Django 4.2.13 on 2024-06-23 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_book_author'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Book',
        ),
    ]
