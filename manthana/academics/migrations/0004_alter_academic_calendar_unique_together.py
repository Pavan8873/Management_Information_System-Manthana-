# Generated by Django 3.2.12 on 2024-08-20 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('master_mgmt', '0002_detained_type'),
        ('academics', '0003_academic_calendar_acad_cal_type'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='academic_calendar',
            unique_together={('acad_cal_acad_year', 'acad_cal_sem', 'acad_cal_type')},
        ),
    ]
