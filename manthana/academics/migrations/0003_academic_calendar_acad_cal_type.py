# Generated by Django 3.2.12 on 2024-08-16 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0002_detained_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='academic_calendar',
            name='acad_cal_type',
            field=models.SmallIntegerField(null=True),
        ),
    ]
