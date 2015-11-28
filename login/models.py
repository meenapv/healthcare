from django.db import models
from django.contrib.auth.models import User
import datetime
from datetime import datetime
# Create your models here.

class UserRole(models.Model):
    user = models.OneToOneField(User)
#    role = models.CharField(max_length=15)
    PATIENT, DOCTOR, STAFF, ADMIN = "Patient", "Doctor", "Staff", "Admin"
    ROLE_CHOICES = (
        (PATIENT, "Patient"),
        (DOCTOR, "Doctor"),
        (STAFF, "Staff"),
        (ADMIN, "Admin")
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null= False, blank= False)
    
User.roles = property(lambda u:UserRole.objects.get_or_create(user=u)[0])
    
class Appt(models.Model):
    patient = models.ForeignKey(User, related_name='patient_user', null=True)
    doctor = models.ForeignKey(User, related_name='doctor_user',null=True)
    medical_problem = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    prescription = models.CharField(max_length=50)

    
class Billing(models.Model):
    patient = models.ForeignKey(User, null=True)
    reason = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.FloatField(max_length=50)
    status = models.CharField(max_length=100)
    
class Leave(models.Model):
    doctor = models.ForeignKey(User, related_name='doctor',null=True)
    reason = models.CharField(max_length=100)
    date_of_leave = models.DateField()
    current_year = models.IntegerField(default=1111)
    leave_limit = models.IntegerField(default=6)
    status = models.CharField(max_length=30)
    is_latest = models.BooleanField(default=True)
    
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/')
