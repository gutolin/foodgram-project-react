# Generated by Django 2.2.16 on 2023-02-12 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='description',
            new_name='text',
        ),
    ]