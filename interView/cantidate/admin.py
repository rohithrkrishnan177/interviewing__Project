from django.contrib import admin
from .models import cantidate, cantidate_history, Appointment

# Register your models here.

# admin.site.register(cantidate)
# admin.site.register(cantidate_history)
admin.site.register(Appointment)

class CantidateAppointment(admin.TabularInline):
    model = Appointment


class CantidateHistoryAdmin(admin.ModelAdmin):
    list_display = ('cantidate', 'assigned_interviewer', 'interview_date', 'department', 'release_date')
    inlines = [CantidateAppointment]


admin.site.register(cantidate_history, CantidateHistoryAdmin)


class CantidateHistoryInline(admin.StackedInline):
    model = cantidate_history


class CantidateAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'address', 'mobile')
    inlines = [CantidateHistoryInline]


admin.site.register(cantidate, CantidateAdmin)
