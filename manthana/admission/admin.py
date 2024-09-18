from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from admission.models import *

# Register your models here.
class UserModel(UserAdmin):
    pass

# class StatesAdmin(StatesAdmin):
#     pass

class EmployeeAdmin(EmployeeAdmin):
    pass

# class StudentAdmin(StudentAdmin):
#     pass

class PrivilegeAdmin(PrivilegeAdmin):
    pass

class RoleDetailAdmin(RoleDetailAdmin):
    pass

admin.site.register(CustomUser,UserModel)
# admin.site.register(States,StatesAdmin)
admin.site.register(Privilege,PrivilegeAdmin)
admin.site.register(RoleDetail,RoleDetailAdmin)