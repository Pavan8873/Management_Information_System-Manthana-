from academics.models import *

def check_students(Present_students,st):
    for present in Present_students:
        if present == st: 
            return True
    return False

#def student_present(st,batch_no,scheme_details_id): testing attendance feature  without batches 18-04-2023
def student_present(st,scheme_details_id,acad_cal_id):
    print("________________________________________")
    #stud_obj = student_attendance.objects.get(batch_no=batch_no,st_uid = st,scheme_details_id=scheme_details_id)
    print(st,scheme_details_id,acad_cal_id)
    stud_obj = student_attendance.objects.get(st_uid = st,scheme_details_id=scheme_details_id,acad_cal_id=acad_cal_id)
    print(stud_obj)
    stud_status = stud_obj.status
    print(stud_status)

    if stud_status == '0':
        new_status = str('P')
    else :
        new_status = str(stud_status) + str('P')
    
    total = len(new_status)

    present = (new_status.count('P'))
    present = int(present)
    total = int(total)

    percentage = present*100/total
    percentage = round(percentage)
    stud_obj.Percentage_of_attendance = percentage
    stud_obj.No_classes_attended = present
    stud_obj.status = new_status

    stud_obj.save()
    print("byeeeeeeeeeeeeeeee")

#def student_absent(st,batch_no,scheme_details_id): testing attendance feature  without batches 19-04-2023
def student_absent(st,scheme_details_id,acad_cal_id):
    #stud_obj = student_attendance.objects.get(batch_no=batch_no,st_uid = st,scheme_details_id=scheme_details_id)
    stud_obj = student_attendance.objects.get(st_uid = st,scheme_details_id=scheme_details_id,acad_cal_id=acad_cal_id)
    stud_status = stud_obj.status

    print(type(stud_status))
    if stud_status == '0':
        new_status = str('A')
    else :
        new_status = str(stud_status) + str('A')

    total = len(new_status)

    present = (new_status.count('P'))

    present = int(present)
    total = int(total)

    percentage = present*100/total
    percentage = round(percentage)
    stud_obj.Percentage_of_attendance = percentage
    stud_obj.No_classes_attended = present
    stud_obj.status = new_status

    stud_obj.save()


def edit_student_present(st,session_index,batch_no,scheme_details_id,acad_cal_id):
    print("pppppppppp",batch_no,session_index)
    stud_obj = student_attendance.objects.get(st_uid = st,batch_no=batch_no,scheme_details_id=scheme_details_id,acad_cal_id=acad_cal_id)
    stud_status = stud_obj.status

    position = session_index-1
    new_character = 'P'

    updated_status = stud_status[:position] + new_character + stud_status[position+1:]

    total = len(updated_status)

    present = (updated_status.count('P'))


    present = int(present)
    total = int(total)

    percentage = present*100/total
    percentage = round(percentage)
    stud_obj.Percentage_of_attendance = percentage
    stud_obj.No_classes_attended = present
    stud_obj.status = updated_status

    stud_obj.save()

def edit_student_absent(st,session_index,batch_no,scheme_details_id,acad_cal_id):
    stud_obj = student_attendance.objects.get(st_uid = st,batch_no=batch_no,scheme_details_id=scheme_details_id,acad_cal_id=acad_cal_id)
    stud_status = stud_obj.status

    position = session_index-1
    new_character = 'A'

    updated_status = stud_status[:position] + new_character + stud_status[position+1:]

    total = len(updated_status)

    present = (updated_status.count('P'))


    present = int(present)
    total = int(total)

    percentage = present*100/total
    percentage = round(percentage)
    stud_obj.Percentage_of_attendance = percentage
    stud_obj.No_classes_attended = present
    stud_obj.status = updated_status

    stud_obj.save()

#----------------------------SEE Attendance------------------------------
def see_student_present(h_id):
    stud_obj = SEE_attendance.objects.get(Hall_ticket_id = h_id)
    stud_status = stud_obj.attendance_Status
    


    if stud_status == '0':
        new_status = str('P')
    else :
        new_status = str(stud_status) + str('P')
    
    stud_obj.status = new_status
    stud_obj.save()

def see_student_absent(h_id):
    stud_obj = SEE_attendance.objects.get(Hall_ticket_id = h_id)
    stud_status = stud_obj.attendance_Status

    if stud_status == '0':
        new_status = str('A')
    else :
        new_status = str(stud_status) + str('A')
    
    stud_obj.status = new_status

    stud_obj.save()