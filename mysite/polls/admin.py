from django.contrib import admin

# Register your models here.
from .models import Department,Staff,Servers,Computer

class DepartmentAdmin(admin.ModelAdmin):
    #fields=('name','email')
    empty_value_display = '-empty-'
    list_display = ('name','email','colored_name')
admin.site.register(Department,DepartmentAdmin)

#from simple_history.admin import SimpleHistoryAdmin
from reversion.admin import VersionAdmin
#@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    list_display = ('name','tel','email','ipaddress','entrydata','department')
admin.site.register(Staff,StaffAdmin)

#admin.site.register(Staff, SimpleHistoryAdmin)
'''
@admin.register(Computer)
class ComputerAdmin(VersionAdmin):
    empty_value_display = '-empty-'
    list_display = ['name']
'''

class ServersAdmin(admin.ModelAdmin):
    empty_value_display = '-empty-'
    #list_display = ('name','tel','email','ipaddress','entrydata','department')
    list_display=('name','staff')
admin.site.register(Servers,ServersAdmin)