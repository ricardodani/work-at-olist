# Generated by Django 2.0.5 on 2018-05-12 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phonebill', '0002_auto_20180512_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='call',
            old_name='total',
            new_name='price',
        ),
    ]