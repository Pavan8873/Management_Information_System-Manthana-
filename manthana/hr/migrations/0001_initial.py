# Generated by Django 3.2.12 on 2024-06-21 12:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('master_mgmt', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee_Details',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('employee_type', models.SmallIntegerField(choices=[(1, 'Admin'), (2, 'Teaching Staff'), (3, 'Student'), (4, 'Non Teaching Staff'), (5, 'Developer')], default=2)),
                ('employee_name', models.CharField(max_length=25)),
                ('employee_emp_id', models.CharField(max_length=10, unique=True)),
                ('employee_gender', models.SmallIntegerField(choices=[(1, 'Male'), (2, 'Female'), (3, 'Others')], default=1)),
                ('employee_profile_pic', models.ImageField(default=False, upload_to='employee/%Y/%m/%d')),
                ('employee_designation', models.CharField(max_length=20)),
                ('employee_qualification', models.CharField(max_length=20)),
                ('employee_cellphone', models.CharField(max_length=15, unique=True)),
                ('employee_dob', models.DateField()),
                ('employee_bld_group', models.SmallIntegerField(choices=[(1, 'A +ve'), (2, 'A -ve'), (3, 'B +ve'), (4, 'B -ve'), (5, 'AB +ve'), (6, 'AB -ve'), (7, 'O +ve'), (8, 'O -ve')], default=1)),
                ('employee_joining_date', models.DateField()),
                ('employee_email', models.CharField(max_length=50)),
                ('employee_pan', models.CharField(max_length=15, unique=True)),
                ('employee_aadhar', models.CharField(max_length=15, unique=True)),
                ('employee_voter_id', models.CharField(max_length=15, unique=True)),
                ('employee_subcaste', models.CharField(max_length=15, null=True)),
                ('employee_postal_address', models.CharField(max_length=50)),
                ('emp_login', models.ForeignKey(db_column='emp_login', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('employee_dept_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.department')),
                ('employee_religion', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.religion')),
            ],
        ),
    ]
