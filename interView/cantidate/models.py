from django.db import models
from account.models import User
from interviewer.models import inter_viewer


# Create your models here.



class cantidate(models.Model):
    age = models.DecimalField(max_digits=4, decimal_places=1)
    address = models.TextField()
    mobile = models.CharField(max_length=20)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return self.user.username


class cantidate_history(models.Model):
    Team_Lead = 'TL'
    Senior_Developer = 'SD'
    Manager = 'MC'
    # The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name.
    department_choices = [(Team_Lead, 'Team_Lead'),
                          (Senior_Developer, 'Senior_Developer'),
                          (Manager, 'Manager')
                          ]
    interview_date = models.DateField(verbose_name="Interview Date", auto_now=False, auto_now_add=True)
    queries = models.TextField()
    department = models.CharField(max_length=3, choices=department_choices, default=Team_Lead)
    release_date = models.DateField(verbose_name="Release Date", auto_now=False, auto_now_add=False, null=True,
                                    blank=True)
    cantidate = models.ForeignKey(cantidate, on_delete=models.CASCADE)
    assigned_interviewer = models.ForeignKey(inter_viewer, on_delete=models.CASCADE)

    def __str__(self):
        return self.patient.get_name


class Appointment(models.Model):
    appointment_date = models.DateField(verbose_name="Appointment date", auto_now=False, auto_now_add=False)
    appointment_time = models.TimeField(verbose_name="Appointement time", auto_now=False, auto_now_add=False)
    status = models.BooleanField(default=False)
    cantidate_history = models.ForeignKey(cantidate_history, related_name='cantidate_appointments', on_delete=models.CASCADE)
    interviewer = models.ForeignKey(inter_viewer, related_name='interview_appointments', null=True, on_delete=models.SET_NULL)

    @property
    def cantidate_name(self):
        self.cantidate_history.cantidate.get_name

    def __str__(self):
        return self._history.patient.get_name + '-' + self.doctor.get_name


