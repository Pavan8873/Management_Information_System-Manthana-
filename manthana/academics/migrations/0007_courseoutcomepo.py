# Generated by Django 3.2.12 on 2024-08-29 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academics', '0006_courseoutcome'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOutcomePO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mapping_level', models.CharField(choices=[('Substantial', 'Substantial Level (3)'), ('Moderate', 'Moderate Level (2)'), ('Slight', 'Slight Level (1)')], max_length=12)),
                ('acad_cal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.academic_calendar')),
                ('co', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.courseoutcome')),
                ('po', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.programoutcome')),
                ('scheme_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details')),
            ],
            options={
                'unique_together': {('acad_cal_id', 'scheme_details_id', 'co', 'po', 'mapping_level')},
            },
        ),
    ]
