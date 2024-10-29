# Generated by Django 4.2.16 on 2024-10-29 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingNumber',
            fields=[
                ('tracking_number', models.CharField(db_index=True, max_length=16, primary_key=True, serialize=False, unique=True)),
                ('origin_country_id', models.CharField(max_length=2)),
                ('destination_country_id', models.CharField(max_length=2)),
                ('weight', models.DecimalField(decimal_places=3, max_digits=10)),
                ('order_created_at', models.DateTimeField()),
                ('customer_id', models.UUIDField()),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_slug', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['origin_country_id'], name='parcels_tra_origin__3edb38_idx'), models.Index(fields=['destination_country_id'], name='parcels_tra_destina_453ad9_idx')],
            },
        ),
    ]
