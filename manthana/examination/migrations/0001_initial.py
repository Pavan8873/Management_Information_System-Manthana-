# Generated by Django 3.2.12 on 2024-06-21 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('master_mgmt', '__first__'),
        ('academics', '0001_initial'),
        ('admission', '0001_initial'),
        ('hr', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam_Details',
            fields=[
                ('exam_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester', models.SmallIntegerField()),
                ('duration_theory_from', models.DateField()),
                ('duration_theory_to', models.DateField()),
                ('duration_lab_from', models.DateField(null=True)),
                ('duration_lab_to', models.DateField(null=True)),
                ('exam_type', models.SmallIntegerField()),
                ('description', models.CharField(max_length=50)),
                ('acad_cal_id', models.ForeignKey(db_column='acad_cal_id', on_delete=django.db.models.deletion.CASCADE, to='academics.academic_calendar')),
                ('acad_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.academicyear', to_field='acayear')),
            ],
            options={
                'unique_together': {('exam_type', 'acad_cal_id')},
            },
        ),
        migrations.CreateModel(
            name='Exam_HallTicket',
            fields=[
                ('hall_ticket_id', models.AutoField(primary_key=True, serialize=False)),
                ('ht_application_no', models.CharField(max_length=10, null=True, unique=True)),
                ('exam_id', models.ForeignKey(db_column='exam_id', on_delete=django.db.models.deletion.CASCADE, to='examination.exam_details')),
                ('st_uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.student_details')),
            ],
            options={
                'unique_together': {('exam_id', 'st_uid')},
            },
        ),
        migrations.CreateModel(
            name='Exam_QP',
            fields=[
                ('exam_qp_id', models.AutoField(primary_key=True, serialize=False)),
                ('course_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details')),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_QP', to='examination.exam_details')),
            ],
            options={
                'unique_together': {('exam_id', 'course_code')},
            },
        ),
        migrations.CreateModel(
            name='External_Valuator',
            fields=[
                ('ext_valuator_id', models.AutoField(primary_key=True, serialize=False)),
                ('ext_valuator_name', models.CharField(max_length=15)),
                ('ext_valuator_department', models.CharField(max_length=25)),
                ('ext_valuator_designation', models.CharField(max_length=25)),
                ('ext_valuator_pan', models.CharField(max_length=10, unique=True)),
                ('ext_valuator_phone', models.CharField(max_length=10, unique=True)),
                ('ext_valuator_college', models.ForeignKey(db_column='ext_valuator_college', on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.extvaluatorcollegename')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Results',
            fields=[
                ('exam_results_id', models.AutoField(primary_key=True, serialize=False)),
                ('semester', models.SmallIntegerField(null=True)),
                ('see_marks', models.SmallIntegerField(default=0)),
                ('final_marks', models.SmallIntegerField(default=0)),
                ('exam_old_grade', models.CharField(max_length=1)),
                ('exam_new_grade', models.CharField(max_length=1)),
                ('exam_gp_earned', models.SmallIntegerField(null=True)),
                ('exam_type', models.SmallIntegerField(null=True)),
                ('acad_cal_id', models.ForeignKey(db_column='acad_cal_id', on_delete=django.db.models.deletion.CASCADE, to='academics.academic_calendar')),
                ('academics_master_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.academics_master_details')),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_result', to='examination.exam_details')),
                ('grade_mapping_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.grademapping')),
                ('scheme_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details')),
                ('st_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.department')),
                ('st_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.student_details')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_QP_Pattern',
            fields=[
                ('qp_pattern_id', models.AutoField(primary_key=True, serialize=False)),
                ('qnum', models.SmallIntegerField(null=True)),
                ('subqnum', models.CharField(max_length=1)),
                ('max_marks', models.SmallIntegerField(null=True)),
                ('co', models.ManyToManyField(to='academics.Course_Outcome')),
                ('exam_qp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_QP_pattern', to='examination.exam_qp')),
            ],
            options={
                'unique_together': {('qnum', 'subqnum', 'exam_qp_id')},
            },
        ),
        migrations.CreateModel(
            name='Exam_HallTicket_Details',
            fields=[
                ('ht_details_id', models.AutoField(primary_key=True, serialize=False)),
                ('academics_master_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.academics_master_details')),
                ('hall_ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hallTicketDetails', to='examination.exam_hallticket')),
            ],
        ),
        migrations.CreateModel(
            name='Exam_Attendance',
            fields=[
                ('see_att_id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_Status', models.CharField(default='P', max_length=1)),
                ('ht_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.exam_hallticket_details')),
                ('st_uid', models.ForeignKey(db_column='st_uid', on_delete=django.db.models.deletion.CASCADE, to='admission.student_details', to_field='st_uid')),
            ],
            options={
                'unique_together': {('st_uid', 'ht_details_id')},
            },
        ),
        migrations.CreateModel(
            name='SEE_Valuator',
            fields=[
                ('valuator_id', models.AutoField(primary_key=True, serialize=False)),
                ('valuator_type', models.CharField(max_length=1)),
                ('course_code', models.ForeignKey(db_column='course_code', on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details', to_field='course_code')),
                ('exam_details_id', models.ForeignKey(db_column='exam_details_id', on_delete=django.db.models.deletion.CASCADE, to='examination.exam_details')),
                ('valuator_empId', models.ForeignKey(blank=True, db_column='valuator_empId', null=True, on_delete=django.db.models.deletion.CASCADE, to='hr.employee_details')),
                ('valuator_pan', models.ForeignKey(blank=True, db_column='valuator_pan', null=True, on_delete=django.db.models.deletion.CASCADE, to='examination.external_valuator', to_field='ext_valuator_pan')),
            ],
            options={
                'unique_together': {('valuator_empId', 'course_code', 'exam_details_id')},
            },
        ),
        migrations.CreateModel(
            name='SEE_Total_Marks',
            fields=[
                ('valuation_id', models.AutoField(primary_key=True, serialize=False)),
                ('total_valuation_marks', models.SmallIntegerField(default=0)),
                ('grade_obtained', models.CharField(max_length=1)),
                ('valuation_type', models.SmallIntegerField()),
                ('exam_qp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.exam_qp')),
                ('st_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.student_details')),
            ],
            options={
                'unique_together': {('st_id', 'exam_qp_id', 'valuation_type')},
            },
        ),
        migrations.CreateModel(
            name='SEE_timetable',
            fields=[
                ('see_att_date_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_date', models.DateField(null=True)),
                ('attendance_flag', models.SmallIntegerField(null=True)),
                ('absentees_count', models.SmallIntegerField(null=True)),
                ('exam_time', models.CharField(max_length=5)),
                ('acad_cal_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.academic_calendar')),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examination.exam_details')),
                ('scheme_details_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details')),
            ],
            options={
                'unique_together': {('acad_cal_id', 'exam_id', 'scheme_details_id')},
            },
        ),
        migrations.CreateModel(
            name='MPC_Report',
            fields=[
                ('mpc_report_id', models.AutoField(primary_key=True, serialize=False)),
                ('mpc_description', models.CharField(max_length=40, null=True)),
                ('reporter_designation', models.CharField(max_length=15)),
                ('reported_by', models.ForeignKey(db_column='reported_by', on_delete=django.db.models.deletion.CASCADE, to='hr.employee_details')),
                ('see_att_id', models.ForeignKey(db_column='see_att_id', on_delete=django.db.models.deletion.CASCADE, to='examination.exam_attendance')),
            ],
            options={
                'unique_together': {('see_att_id', 'reported_by')},
            },
        ),
        migrations.CreateModel(
            name='Makeup_Exam_Registration',
            fields=[
                ('makeup_exam_reg_id', models.AutoField(primary_key=True, serialize=False)),
                ('exemption_from_grade_reduction', models.BooleanField(default=False, null=True)),
                ('reason_for_application', models.CharField(max_length=50, null=True)),
                ('acad_cal_id', models.ForeignKey(db_column='acad_cal_id', on_delete=django.db.models.deletion.CASCADE, to='academics.academic_calendar')),
                ('branch', models.ForeignKey(db_column='branch', on_delete=django.db.models.deletion.CASCADE, to='master_mgmt.department')),
                ('exam_id', models.ForeignKey(db_column='exam_id', on_delete=django.db.models.deletion.CASCADE, to='examination.exam_details')),
                ('scheme_details_id', models.ForeignKey(db_column='scheme_details_id', on_delete=django.db.models.deletion.CASCADE, to='academics.scheme_details')),
                ('st_uid', models.ForeignKey(db_column='st_uid', on_delete=django.db.models.deletion.CASCADE, to='admission.student_details', to_field='st_uid')),
            ],
            options={
                'unique_together': {('st_uid', 'scheme_details_id')},
            },
        ),
        migrations.CreateModel(
            name='Exam_Bitwise_Marks',
            fields=[
                ('bitwise_marks_id', models.AutoField(primary_key=True, serialize=False)),
                ('code_number', models.CharField(max_length=30)),
                ('obtained_marks', models.SmallIntegerField(default=0)),
                ('valuation_type', models.SmallIntegerField()),
                ('qp_pattern_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_QP_bitwise_marks', to='examination.exam_qp_pattern')),
            ],
            options={
                'unique_together': {('code_number', 'qp_pattern_id', 'valuation_type')},
            },
        ),
        migrations.CreateModel(
            name='Bar_Code',
            fields=[
                ('serial_no', models.AutoField(primary_key=True, serialize=False)),
                ('barcode', models.CharField(max_length=15)),
                ('exam_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exam_barCode', to='examination.exam_details')),
                ('st_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admission.student_details')),
            ],
            options={
                'unique_together': {('st_id', 'barcode', 'exam_id')},
            },
        ),
    ]
