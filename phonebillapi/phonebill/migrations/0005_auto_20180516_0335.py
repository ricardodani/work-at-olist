# Generated by Django 2.0.5 on 2018-05-16 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phonebill', '0004_auto_20180515_0017'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='call',
            index=models.Index(fields=['start_record', 'end_record'], name='phonebill_c_start_r_0cee0b_idx'),
        ),
    ]
