from rbac.models import RightCategory, RightDetails, RightType, UserRights
from admission.models import CustomUser
from hr.models import Employee_Details 
from admission.models import Student_Details
def categories_processor(request):
    try:
        usrName = None
        usrPic = None
        usrType = None
        userName=CustomUser.objects.get(id=request.user.id)
        print(userName)
        user=CustomUser.objects.filter(id=request.user.id)     
        print(user) 
        for usr in user:
            #check for employee
            if usr.user_type == 2 or usr.user_type == 4:
                emp = Employee_Details.objects.get(employee_emp_id = usr.username)
                usrName = emp.employee_name
                usrPic = emp.employee_profile_pic
                usrType = usr.user_type
            #To check developer type
            elif usr.user_type == 5:
                print(usr.user_type)
                try:
                    emp = Employee_Details.objects.get(employee_emp_id = usr.username)
                    usrName = emp.employee_name
                    usrPic = emp.employee_profile_pic
                    usrType = usr.user_type    
                except Exception as e:
                    print("Inside inner try")
            #check for student
            elif usr.user_type == 3:
                student = Student_Details.objects.get(st_uid = usr.username)
                usrName = student.st_name
                usrPic = student.st_profile_pic
                usrType = usr.user_type
            #check for admin
            elif usr.user_type == 1:
                try:
                    cusr = CustomUser.objects.get(username = usr.username)
                    usrName = cusr.username
                    usrPic = 'images/login_image.webp'
                    usrType = usr.user_type    
                except:
                    pass
    except Exception as e:
        return { }
    usrroles=UserRights.objects.filter(user=userName.id).values('right_id')
    roles=RightDetails.objects.filter(id__in=usrroles).values('abbr','details','category','type').order_by('category','type')
    rcategory=RightDetails.objects.filter(id__in=usrroles).values('category').order_by('category').distinct()
    catdesc=RightCategory.objects.filter(category__in=rcategory)
    print (usrPic)
    # return userName, roles, catdesc, usrName
    return {'userName':userName,'roles':roles, 'category':catdesc, 'usrName':usrName,'usrPic':usrPic,'usrType':usrType}