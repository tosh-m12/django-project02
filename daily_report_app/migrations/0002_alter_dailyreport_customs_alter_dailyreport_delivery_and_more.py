# Generated by Django 5.2.4 on 2025-07-24 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily_report_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailyreport',
            name='customs',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='delivery',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='inbound',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='outbound',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='shipment',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='dailyreport',
            name='special_tag',
            field=models.PositiveIntegerField(blank=True, default=None, null=True),
        ),
    ]
