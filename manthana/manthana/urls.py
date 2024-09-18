"""manthana URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import admission.views
import academics.views #added after app creation
import insignia
import rbac.views
import master_mgmt.views
import examination.views
import hr.views
import insignia.views

urlpatterns = [
    #Master MGMT URLs
    #add/edit department URLs
    path('AddDepartment',master_mgmt.views.add_department,name="AddDepartment"),
    path('CreateDepartment',master_mgmt.views.CreateDepartment,name="CreateDepartment"),
    path('EditDepartment/<str:dept_id>',master_mgmt.views.edit_department,name="EditDepartment"),
    path('EditDepartmentSave',master_mgmt.views.EditDepartment,name="EditDepartmentSave"),
    #add/edit Religion URLs
    path('AddReligion',master_mgmt.views.add_religion,name="AddReligion"),
    path('CreateReligion',master_mgmt.views.CreateReligion,name="CreateReligion"),
    path('EditReligion/<str:religion_id>',master_mgmt.views.edit_religion,name="EditReligion"),
    path('EditReligionSave',master_mgmt.views.EditReligion,name="EditReligionSave"),
    #add/edit States URLs
    path('AddStates',master_mgmt.views.add_states,name="AddStates"),
    path('CreateStates',master_mgmt.views.CreateStates,name="CreateStates"),
    path('EditStates/<str:state_id>',master_mgmt.views.edit_states,name="EditStates"),
    path('EditStatesSave',master_mgmt.views.EditStates,name="EditStatesSave"),
    #add/edit BloodGroup URLs
    path('AddBloodGroup',master_mgmt.views.add_bloodgroup,name="AddBloodGroup"),
    path('CreateBloodGroup',master_mgmt.views.CreateBloodGroup,name="CreateBloodGroup"),
    path('EditBloodGroup/<str:bg_id>',master_mgmt.views.edit_bloodgroup,name="EditBloodGroup"),
    path('EditBloodGroupSave',master_mgmt.views.EditBloodGroup,name="EditBloodGroupSave"),
    #add/edit Employee URLs
    #currently add/edit employee views available under Master Mgmt
    #in-future needs to be moved to HR app ONLY
    #Employee_Details model available under HR app
    path('AddEmployee',hr.views.add_employee,name="AddEmployee"),
    path('CreateEmployee',hr.views.CreateEmployee,name="CreateEmployee"),
    path('EditEmployee/<str:emp_id>',hr.views.edit_employee,name="EditEmployee"),
    path('EditEmployeeSave',hr.views.EditEmployee,name="EditEmployeeSave"),
    #add/edit Academic Year URLs
    path('AddAcademicYear',master_mgmt.views.add_academicyear,name="AddAcademicYear"),
    path('CreateAcademicYear',master_mgmt.views.CreateAcademicYear,name="CreateAcademicYear"),
    path('Editacayear/<str:acayear_id>',master_mgmt.views.edit_acayear,name="Editacayear"),
    path('UpdateAcaYear',master_mgmt.views.EditAcaYear,name="UpdateAcaYear"),
    #add/edit Division Creation URLs
    path('AddDivision',master_mgmt.views.add_division,name="AddDivision"),
    path('CreateDivision',master_mgmt.views.CreateDivision,name="CreateDivision"),
    path('AddRooms',master_mgmt.views.add_room,name="AddRooms"),
    path('CreateRoom',master_mgmt.views.CreateRoom,name="CreateRoom"),
    path('Editroom/<str:room_id>',master_mgmt.views.edit_room,name="Editroom"),
    path('UpdateRoom',master_mgmt.views.EditRoom,name="UpdateRoom"),
    path('Editdivision/<str:div_id>',master_mgmt.views.edit_division,name="Editdivision"),
    path('UpdateDivision',master_mgmt.views.EditDivision,name="UpdateDivision"),
    #add/edit UserType Creation URLs
    path('AddUserType',master_mgmt.views.add_usertype,name="AddUserType"),
    path('CreateUsertype',master_mgmt.views.CreateUserType,name="CreateUsertype"),
    path('Editusertype/<str:usertype_id>',master_mgmt.views.edit_usertype,name="Editusertype"),
    path('UpdateUsertype',master_mgmt.views.EditUsertype,name="UpdateUsertype"),
    #add/edit Admission Quota URLs
    path('AddQuota',master_mgmt.views.add_Quota,name="AddQuota"),
    path('CreateQuota',master_mgmt.views.CreateQuota,name="CreateQuota"),
    path('Editquota/<str:quota_id>',master_mgmt.views.edit_quota,name="Editquota"),
    path('UpdateQuota',master_mgmt.views.EditQuota,name="UpdateQuota"),
    #add/edit Months master management
    path('AddMonths',master_mgmt.views.add_Months,name="AddMonths"),
    path('CreateMonths',master_mgmt.views.CreateMonths,name="CreateMonths"),
    path('Editmonth/<str:month_id>',master_mgmt.views.edit_month,name="Editmonth"),
    path('UpdateMonth',master_mgmt.views.EditMonth,name="UpdateMonth"),
    
    #add/edit Category master management
    path('AddCategory',master_mgmt.views.add_Category,name="AddCategory"),
    path('CreateCategory',master_mgmt.views.CreateCategory,name="CreateCategory"),
    path('EditCategory/<str:category_id>',master_mgmt.views.edit_category,name="EditCategory"),
    path('UpdateCategory',master_mgmt.views.EditCategory,name="UpdateCategory"),

    #add/edit Semester master management
    path('AddSemester',master_mgmt.views.add_Semester,name="AddSemester"),
    path('CreateSemester',master_mgmt.views.CreateSemester,name="CreateSemester"),
    path('EditSemester/<str:sem_id>',master_mgmt.views.edit_semester,name="EditSemester"),
    path('UpdateSemester',master_mgmt.views.EditSemester,name="UpdateSemester"),
    
    #add/edit External Valuators college list master management
    path('AddExtValCollege',master_mgmt.views.add_ExtValCollege,name="AddExtValCollege"),
    path('CreateExtValCollege',master_mgmt.views.CreateExtValCollege,name="CreateExtValCollege"),
    path('EditExtValCollege/<str:clg_id>',master_mgmt.views.edit_College,name="EditExtValCollege"),
    path('UpdateExtValCollege',master_mgmt.views.EditExtValCollege,name="UpdateExtValCollege"),

    #add/edit Grade Mapping master management
    path('AddGradempping',master_mgmt.views.add_Gradempping,name="AddGradempping"),
    path('CreateGradempping',master_mgmt.views.CreateGradempping,name="CreateGradempping"),
    path('EditGradempping/<str:grademapping_id>',master_mgmt.views.edit_Gradempping,name="EditGradempping"),
    path('UpdateGradempping',master_mgmt.views.EditGradempping,name="UpdateGradempping"),
    
    #add/edit Course Type master management
    path('AddCoursetype',master_mgmt.views.add_AddCoursetype,name="AddCoursetype"),
    path('CreateCoursetype',master_mgmt.views.CreateCoursetype,name="CreateCoursetype"),
    path('EditCoursetype/<str:coursetype_id>',master_mgmt.views.edit_Coursetype,name="EditCoursetype"),
    path('UpdateCoursetype',master_mgmt.views.EditCoursetype,name="UpdateCoursetype"),
    #Reset Password workflow URLs
    path('reset_password',master_mgmt.views.reset_password,name="reset_password"),
    path('ResetPassword',master_mgmt.views.ResetPassword,name="ResetPassword"),

    #RBAC URLs
    path('AddRights',rbac.views.add_rights, name='AddRights'),  #has to enable for developer to create roles for others
    path('CreateRights',rbac.views.CreateRights, name='CreateRights'),
    path('EditRights/<str:right_id>',rbac.views.edit_rights,name="EditRights"),
    path('EditRightsSave',rbac.views.EditRights,name="EditRightsSave"),
    path('assignRights',rbac.views.assignRights, name='assignRights'), #has to enable for admin to assign roles to others
    path('AssignRights',rbac.views.AssignRights, name='AssignRights'), 
    path('LoginDashBoard',rbac.views.LoginDashBoard,name="LoginDashBoard"),
    #Change password workflow URLs
    path('change_password',rbac.views.change_password,name="change_password"),
    path('ChangePassword',rbac.views.ChangePassword,name="ChangePassword"),

    #Admission URLs
    path('',admission.views.loginPage),
    #To be used to while server is under maintenance
    # path('',admission.views.serverDown),
    path('admin/', admin.site.urls),
    path('About Us',admission.views.about_us,name="About Us"),
    path('doLogin',admission.views.doLogin),

    path('SearchStudent',admission.views.SearchStudent),
    path('SearchSCHEME',academics.views.SearchSCHEME),
    path('admin_home',admission.views.admin_home),  
    path('staff_home',admission.views.staff_home),      # Yet to Implement
    path('student_home',admission.views.student_home),  # Yet to Implement
    path('logout',admission.views.logout_user,name="logout"),
    path('captcha', include("captcha.urls")),   
    path('AddStudent',admission.views.add_student,name="AddStudent"), #Not being used
    path('EditUGStudent/<str:st_id>',admission.views.edit_student,name="EditUGStudent"),
    # path('admissionStat',admission.views.admission_stat,name="admissionStat"),
    path('admissionStat',admission.views.admissionStat, name='admissionStat'),
    path('admissionStatReport/<str:ad_type>,<str:ac_year>',admission.views.admissionStatReport, name='admissionStatReport'),
    path('AddLateralStudent',admission.views.add_lateral,name="AddLateralStudent"), #Not being used
    path('EditLateralStudent/<str:st_id>',admission.views.edit_lateral,name="EditLateralStudent"),

    
    #Addmission of Transfer of College
    path('AddTransferOfCollege',admission.views.add_transferofcollege,name="AddTransferOfCollege"), 
    path('Editransferofcollege/<str:st_id>',admission.views.edit_transferofcollege,name="Editransferofcollege"),
    path('admitCollegetransferstud',admission.views.admitClgtrstudent,name='admitCollegetransferstud'),

    path('AddPGStudent',admission.views.add_pg,name="AddPGStudent"), #Not being used
    path('EditPGStudent/<str:st_id>',admission.views.edit_studentpg,name="EditPGStudent"),
    path('Admission_Higher_Semester_Details_view',admission.views.Admission_Higher_Semester_Details_view,name="Admission_Higher_Semester_Details_view"),
    path('admitStudentUG',admission.views.admitStudent_ug, name='admitStudentUG'),
    path('admitStudentLat',admission.views.admitStudent_lat, name='admitStudentLat'),
    path('admitStudentPG',admission.views.admitStudent_pg, name='admitStudentPG'),
    path('ViewStudent',admission.views.view_student,name="ViewStudent"),
    path('Student Report',admission.views.student_report,name="Student Report"),    # Yet to Implement
    path('Delete Student',admission.views.delete_student,name="Delete Student"),    # Yet to Implement
    path('admindashboard',admission.views.admindashboard,name="admindashboard"),    
    path('StudentHome',admission.views.StudentHome,name="StudentHome"),             # Yet to Implement
    path('pdf_students',admission.views.pdf_students,name="PDFStudents"),
    path('id_card_students',admission.views.id_card_students,name="GenerateIDCard"),
    path('export_excel',admission.views.export_excel,name="ExportExcel"),
    path('export_csv',admission.views.export_csv,name="ExportCSV"),
    path('ackPdf_ug/<str:st_id>',admission.views.ackPdf_ug,name="ackPdf_ug"),
    path('ackPdf_lat/<str:st_id>',admission.views.ackPdf_lat,name="ackPdf_lat"),
    path('ackPdf_pg/<str:st_id>',admission.views.ackPdf_pg,name="ackPdf_pg"),
    path('ackPdf_tr/<str:st_id>',admission.views.ackPdf_tr,name="ackPdf_tr"),
    path('gen_ack',admission.views.gen_ack,name="gen_ack"),
    path('view_ug/<str:st_id>', admission.views.view_ug, name="view_ug"),
    path('view_lat/<str:st_id>', admission.views.view_lat, name="view_lat"),
    path('view_pg/<str:st_id>', admission.views.view_pg, name="view_pg"),
    path('view_clgtrns/<str:st_id>', admission.views.view_clgtrns, name="view_clgtrns"),
   
    path('reportPage', admission.views.reportPage, name="reportPage"),
    path('mapUSNPage',admission.views.mapUSNPage,name="mapUSNPage"),
    path('load_st_uid',admission.views.load_st_uid,name='ajax_load_st_uid'),
    path('allot_usn',admission.views.allot_usn),
    path('upload/', admission.views.upload_file, name='upload_file'),

    #Academics URLs
    path('Editscheme/<str:scheme_details_id>',academics.views.editSCHEME,name="Editscheme"),
    path('viewscheme',academics.views.view_scheme,name="viewscheme"),
    path('view_scheme',academics.views.view_scheme,name="view_scheme"),
    path('admitStudent_higher',admission.views.admitStudent_higher),
    path('allotCourseToFaculty',academics.views.allotCourseToFaculty,name='allotCourseToFaculty'),
    path('addcalender',academics.views.addcalender),
    path('allotScheme',academics.views.allotScheme),
    path('allotCycle',academics.views.allotCycle),
    path('allotDivision',academics.views.allotDivision,name="allotDivision"),
    path('ugAllotDivision',academics.views.ugAllotDivision),
    path('addSchemedetails',academics.views.addschemedetails,name="addSchemedetails"),
    path('UgAcadCalender',academics.views.ug_acad_calender,name="UgAcadCalender"),
    path('EditSchemeDEtails',academics.views.edit_scheme,name="editscheme"),
    path('EditAcadCalender/<str:acad_cal_id>',academics.views.edit_calender,name='EditAcadCalender'),
    path('print_calender/<str:acad_cal_id>',academics.views.print_calender,name='print_calender'),
    path('ViewAcadCalender',academics.views.view_calender,name='ViewAcadCalender'),
    path('SchemeAllotment',academics.views.SchemeAllotment,name="SchemeAllotment"),
    path('EditSchemeallot',academics.views.edit_schemeallot,name="editschemeallot"),
    path('AddSchemeDetails',academics.views.AddSchemeDetails,name="AddSchemeDetails"),
    path('First_year_StudentDivisionAllotment',academics.views.First_year_StudentDivisionAllotment,name="First_year_StudentDivisionAllotment"),
    path('load_student/',academics.views.load_student,name="ajax_load_student"),
    path('UGStudentDivisionAllotment',academics.views.UGStudentDivisionAllotment,name="UGStudentDivisionAllotment"),    
    path('ugload_student/',academics.views.ugload_student,name="ajax_ugload_student"),
    path('CycleDivisionAllotment',academics.views.CycleDivisionAllotment,name="CycleDivisionAllotment"),
    path('Searchdiv',academics.views.Searchdiv,name='Searchdiv'),
    path('EditCycleDivisionAllotment/<str:cycle_div_allot_id>/<str:acad_cal_id>',academics.views.Edit_CycleDivisionAllotment,name="EditCycleDivisionAllotment"),
    path('FirstYearCourseDetails',academics.views.FirstYearCourseDetails,name="FirstYearCourseDetails"),
    path('FacultyCourseAllot',academics.views.faculty_course_allotment,name="FacultyCourseAllot"),
    path('DeclareAssessment',academics.views.declareAssessment,name="DeclareAssessment"), 
    path('getAssessment',academics.views.getAssessment,name="getAssessment"),
    path('assessment_pattern',academics.views.assessment_pattern,name="assessment_pattern"),
    path('add_assessment_pattern/<str:id>',academics.views.add_assessment_pattern,name="add_assessment_pattern"),
    path('edit_assessment_pattern/<str:id>',academics.views.edit_assessment_pattern,name="edit_assessment_pattern"),
    path('bitWiseMarks',academics.views.bitWiseMarks,name="bitWiseMarks"), 
    path('load-faculty/', academics.views.load_faculty, name='ajax_load_faculty'),

    path('load_courses/',academics.views.load_courses, name='ajax_load_courses'),
    
    path('displaycourses/',academics.views.displaycourses, name='ajax_displaycourses'),
    


    path('load_sem/',academics.views.load_sem, name='ajax_load_sem'),
    path('load_first_year_course', academics.views.load_first_year_course,name="load_first_year_course"),
    path('load_first_year_subjects/', academics.views.load_first_year_subjects, name='ajax_load_first_year_subjects'),
    path('addFirstYearCourses', academics.views.addFirstYearCourses),
    path('UGCourseRegistration',academics.views.UGCourseRegistration,name="UGCourseRegistration"),

    path('load_UG_courses/',academics.views.load_UG_courses, name='ajax_ug_load_courses'),

    path('First Year Course Registration (Bulk)',academics.views.load_first_year_student_course_reg_page,name="First Year Course Registration (Bulk)"), 
    path('load_first_year_st_reg_subjects/',academics.views.load_first_year_st_reg_subjects,name='ajax_load_first_year_subjects_st_reg_bulk'),
    path('bulkRegisterFirstYearStudentCourses',academics.views.bulkRegisterFirstYearStudentCourses),
    path('bulkRegisterUGStudentCourses',academics.views.bulkRegisterUGStudentCourses),
    path('CourseEquivalence',academics.views.CourseEquivalence, name='CourseEquivalence'),
    

    path('load_courseslist/',academics.views.load_courseslist,name='ajax_load_courseslist'), 
    path('load_newcourseslist/',academics.views.load_newcourseslist,name='ajax_load_newcourseslist'),
    path('displaylist/',academics.views.displaylist,name='ajax_displaylist'),
    path('addCourseEquivalent',academics.views.addCourseEquivalent),
    path('EditCourseEquivalence/<str:course_equivalence_id>',academics.views.edit_course_equivalence,name='EditCourseEquivalence'),
    path('UGProgramElective',academics.views.UGProgramElective,name="UGProgramElective"),
    path('ugload_student_elective_reg/',academics.views.ugload_student_elective_reg,name='ajax_ugload_student_elective_reg'),
    
    path('ajax_load_courses_select/',academics.views.load_courses_select,name='ajax_load_courses_select'),
    path('loadElectives/',academics.views.loadElectives,name='ajax_ugload_program_elective'),
    path('bulkRegisterElectives',academics.views.bulkRegisterElectives),
    
    # path('UG_Lab_Batch_Allotment',academics.views.UGStudentBatchAllotment,name='UG_Lab_Batch_Allotment'),
    # path('ajax_ugload_lab_student',academics.views.ug_load_students_batch_allot,name='ajax_ugload_lab_student'),
    # path('ugAllotBatch',academics.views.ugAllotBatch),

    path('addFeedbackQue',academics.views.addFeedbackQue,name="addFeedbackQue"),
    path('AddQuestionnaire',academics.views.add_feedback_questionnaire,name="AddQuestionnaire"),
    # path('studentclassattendance',academics.views.Student_Attendance,name="studentclassattendance"),
    path('student_attendance',academics.views.student_attendance_det,name='student_attendance'),
    path('studenteachclassattendance',academics.views.studenteachclassattendance,name='studenteachclassattendance'),
    path('attendancelist/<str:attend_date>/<str:numberofclasses>/<str:course_code>/<str:division>/<str:acad_year>/<str:session1>/<str:session2>/<str:acad_cal_type>/<str:batch_no>',academics.views.student_attendance_list,name='attendancelist'),
    path('Editstudentattendance',academics.views.edit_student_attendance,name='Editstudentattendance'),
    path('UG_Lab_Batch_Allotment',academics.views.UGStudentBatchAllotment,name='UG_Lab_Batch_Allotment'),
    path('ajax_ugload_lab_student',academics.views.ug_load_students_batch_allot,name='ajax_ugload_lab_student'),
    
    path('ajax_load_first_year_subjects_for_declare_assement',academics.views.load_first_year_subjects_for_declare_assement,name='ajax_load_first_year_subjects_for_declare_assement'),
    path('ugAllotBatch',academics.views.ugAllotBatch),
    path('Report_ia_Marks',academics.views.Report_ia_Marks,name="Report_ia_Marks"),
    path('attendance_report',academics.views.attendance_report,name="attendance_report"),
    path('course_registration/', academics.views.course_registration_page, name='course_registration_page'),
    path('load_courses/', academics.views.load_courses, name='ajax_load_courses'),
    path('register_course/', academics.views.register_course, name='register_course'),
    path('ajax_load_faculty/', academics.views.ajax_load_faculty, name='ajax_load_faculty'),
    path('fetch_failed_students/', academics.views.fetch_failed_students, name='fetch_failed_students'),
    path('map_co_po', academics.views.map_co_po, name='map_co_po'),
    path('load_courses_co_po/', academics.views.load_courses_co_po, name='load_courses_co_po'),
    

  


    #Examination URLs
    # ajax_load_courses_for_exam 
    path('ajax_load_courses_for_exam',examination.views.load_courses_for_exam,name="ajax_load_courses_for_exam"),
    path('UG_SEE_ExamDetails',examination.views.loadExamDetails,name="UG_SEE_ExamDetails"), #menu
    path('addExamDetails',examination.views.addExamDetails),
    path('loadExternalValuatorsPage',examination.views.loadExternalValuatorsPage,name="Add External Valuators"), #menu
    path('addExternalValuators',examination.views.addExternalValuators,name="addExternalValuators"),
    path('loadSEEValuatorsPage',examination.views.loadSEEValuatorsPage,name="Rights to SEE Valuators"), #menu
    path('ajax_load_see_subjects',examination.views.loadSEESubjects,name='ajax_load_see_subjects'),
    path('assignRightsToValuators',examination.views.assignRightsToValuators),
    path('seetimetable',examination.views.generate_see_timetable,name='seetimetable'),    #menu
    path('ajax_load_see_subjects_tt',examination.views.loadSubjectsSEETimetable,name='ajax_load_see_subjects_tt'),
    path('generate_barcode',examination.views.gen_barcode,name="generate_barcode"),  #menu
    path('generate_hallticket',examination.views.generate_hallticket,name="generate_hallticket"),
    path('gen_hallTicket',examination.views.gen_hallTicket,name='gen_hallTicket'), #menu
    path('MPCReport',examination.views.MPCReport, name='MPCReport'),    #menu
    path('addMPCReport',examination.views.addMpcReport, name='addMPCReport'),
    path('EditMPCReport/<str:mpc_report_id>',examination.views.EditMPCReport,name="EditMPCReport"),
    path('ViewEditMPCReport',examination.views.view_mpc_report,name="ViewEditMPCReport"),   #menu
    path('SearchMpcStudent',examination.views.SearchMpcStudent,name="SearchMpcStudent"),
    path('MakeUpExamRegistration',examination.views.MakeUpExamRegistration,name="MakeUpExamRegistration"),
    path('addMakeupExam',examination.views.addMakeupExam,name="addMakeupExam"), #menu
    path('loadStudentRegisteredSubjects/',examination.views.loadStudentRegisteredSubjects,name='ajax_load_student_subjects'),
    path('ViewEditMakeupExamRegister',examination.views.view_makeup_register,name="ViewEditMakeupExamRegister"),
    path('SearchMakeupStudent',examination.views.SearchMakeupStudent,name="SearchMakeupStudent"),
    path('EditMakeupExamRegister/<str:makeup_exam_reg_id>',examination.views.EditMakeupExamRegister,name="EditMakeupExamRegister"),
    path('seeattendance',examination.views.see_student_attendance,name='seeattendance'),    #manu
    path('editseeattendance',examination.views.edit_see_student_attendance,name='editseeattendance'),
    path('seeattendancelist/<str:attend_date>/<str:course_code>/<str:acad_cal_id>/<str:exam_desc>',examination.views.see_student_attendance_list,name='seeattendancelist'),
    path('exam_qp',examination.views.exam_qp,name="exam_qp"),
    path('add_exam_qp_pattern/<str:id>',examination.views.add_exam_qp_pattern,name="add_exam_qp_pattern"),  #menu
    path('exam_qp_pattern',examination.views.exam_qp_pattern,name=" exam_qp_pattern"),
    path('edit_exam_qp_pattern/<str:id>',examination.views.edit_exam_qp_pattern,name="edit_exam_qp_pattern"),
    path('external_exam_bitwise',examination.views.external_exam_bitwise,name="external_exam_bitwise"), #menu
    path('gen_result',examination.views.gen_result,name="gen_result"), #menu
    path('student_promotion_list',examination.views.student_promotion_list,name="student_promotion_list"),
    path('provisional',examination.views.provisional,name="provisional"),
    path('pro',examination.views.pro,name="pro"),
    path('exam_schedule_view', examination.views.exam_schedule_view, name='exam_schedule_view'),
    path('fetch_exams', examination.views.fetch_exam_details_seetitable, name='fetch_exams'),
    path('qporder', examination.views.order, name='qporder'),
    path('order', examination.views.order, name='order'),
    path('fetch_exam_details', examination.views.fetch_exam_details, name='fetch_exam_details'),
    path('fetch_faculty_by_course', examination.views.fetch_faculty_by_course, name='fetch_faculty_by_course'),
    
    path('backLogExamRegistration', examination.views.backLogExamRegistration, name='backLogExamRegistration'),
    
    path('valuator', examination.views.valuator, name='valuator'),
     
    #HR URLs
    path('addforevent',insignia.views.hello,name="addforevent"),
    path('addforevents',insignia.views.hello1,name="addforevents"),
    path('reg',insignia.views.reg1, name='reg'),
    path('list',insignia.views.part, name='list'),
    path('registrationlist',insignia.views.reglist, name='registrationlist'),
    path('ADDWINNERS',insignia.views.WINNER, name='ADDWINNERS'),
    path('win',insignia.views.win, name='win'),
    path('winl',insignia.views.winl, name='winl'),
    path('win_list',insignia.views.win_list, name='win_list'),
    path('addev',insignia.views.addev, name='addev'),
    path('addeven',insignia.views.addeven, name='addeven'),
    path('FEEDBACKFORM',insignia.views.feedback1, name='FEEDBACKFORM'),
    path('dump',insignia.views.dump123,name='dump'),
    path('report',insignia.views.report,name='report'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
