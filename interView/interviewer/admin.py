from django.contrib import admin
from . models import inter_viewer
from cantidate.models import Appointment

# Register your models here.

class InterviewAppointment(admin.TabularInline):
    model=Appointment


# admin.site.register()

class InterviewerAdmin(admin.ModelAdmin):
    list_display=['get_name','department', 'address', 'mobile', 'user']
    inlines=[InterviewAppointment]


admin.site.register(inter_viewer,InterviewerAdmin)