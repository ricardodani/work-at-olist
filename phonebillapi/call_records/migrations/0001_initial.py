# Generated by Django 2.0.5 on 2018-05-23 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Call',
            fields=[
                ('call_id', models.AutoField(primary_key=True, serialize=False)),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('source', models.CharField(db_index=True, max_length=11)),
                ('destination', models.CharField(blank=True, max_length=11, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompletedCall',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('call_records.call',),
        ),
        migrations.CreateModel(
            name='NotCompletedCall',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('call_records.call',),
        ),
    ]
