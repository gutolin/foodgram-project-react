# Generated by Django 2.2.16 on 2023-02-12 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20230212_1808'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredientamount',
            old_name='ingredient',
            new_name='name',
        ),
    ]