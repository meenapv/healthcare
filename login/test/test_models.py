from django.test import Client
import nose.tools as nt
from login import views
from login.views import *
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db.models import *
from login.forms import *
from login.models import *

class TestModels(TestCase):
    
    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@gmail.com', 'password1')
        setDoctor(self.user)
        
    def setDoctor(self,user):
        self.user = User.objects.create_user('doctoruser', 'doctor@gmail.com', 'password2')
        UserRole.objects.create(user=user,role="Doctor")
        
    def test_UserRole(self):
        user = User.objects.filter(username="doctoruser")  
        if not(UserRole.objects.filter(user=user, role="doctor").exists()):
            nt.assert_false
        
#    def test_Appt(self):
#        doctor = User.objects.get(username="doctoruser")
#        patient = User.objects.get(username="testuser")
#        w = Appt.objects.create(doctor=doctor, patient=patient, medical_problem='fever', date="2015-12-20", time="13:30")
#        self.assertTrue(isinstance(w, Appt))
#        
#    def test_Billing(self):
#        patient = User.objects.filter(id="testuser")
#        w = Billing.objects.create(patient=patient, reason="consulting", date="2015-01-01",amount="400",status="paid")
#        self.assertTrue(isinstance(w, Billing))

	def test_leave(self):
		doctor = User.object.get(username="doctoruser")
		w = Leave.object.create(reason = personal, date = "2015-01-05", Curent-year= "2015", leave_limit= "5" , Status= "approved", is_latest="true")
		self.assertTrue(isinstance(w, leave)
