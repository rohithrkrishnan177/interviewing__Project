from django.db import models
from django.db.models.fields import DateField
from account.models import User

# Create your models here.

class inter_viewer(models.Model):
    Team_Lead='TL'
    Senior_Developer='SD'
    Manager='MC'
    #The first element in each tuple is the actual value to be set on the model, and the second element is the human-readable name.
    department_choices=[(Team_Lead,'Team_Lead'),
        (Senior_Developer,'Senior_Developer'),
        (Manager,'Manager')
    ]
    department=models.CharField(max_length=3, choices=department_choices, default=Manager)
    address= models.TextField()
    mobile=models.CharField(max_length=20)
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)
