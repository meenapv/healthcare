from django.test import Client
import nose.tools as nt
from login import views
from login.views import *
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import models
from login.forms import *

class TestViews(TestCase):

    def setup(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'testuser@gmail.com', 'password1')
        setDoctor(self.user)
        
    def setDoctor(self,user):
        self.user = User.objects.create_user('doctoruser', 'doctor@gmail.com', 'password2')
        UserRole.objects.create(user=user,role="Doctor")

    def test_login(self):
        response = self.client.get("/")
        if (response.content.find("Welcome to Hospital Management system !!")==-1):
            nt.assert_false
            
    def test_register_form(self):
        form_data = {'username': 'registereduser', "password1":"password", "password2": "password","email":"register@gmail.com"}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_login_required(self):
        response = self.client.get(reverse('login.views.appointment'))
        self.assertRedirects(response, '/accounts/login/?next=/user/bookappt/')
        
    def test_book_appt_positive(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/user/bookappt/', {'Doctor_name': 'doctoruser', 'medprob': 'fever', "date":"2015-12-20", "time":"13:30"})
        if (response.content.find("Appointment Successful")==-1):
            nt.assert_false

        
    def test_book_appt_negative(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/user/bookappt/', {'Doctor_name': 'doctoruser', 'medprob': 'fever', "date":"2014-12-20", "time":"13:30"})
        if (response.content.find("Appointment Successful")==-1):
            nt.assert_false
            
    def test_medical_history(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/user/bookappt/', {'Doctor_name': 'doctoruser', 'medprob': 'fever', "date":"2015-12-20", "time":"13:30"})
        patient = User.objects.filter(username="testuser")
        if not(Appt.objects.filter(patient=patient).exists()):
            nt.assert_false
            
    def test_nil_medical_history(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post('/user/bookappt/', {'Doctor_name': 'doctoruser', 'medprob': 'fever', "date":"2014-12-20", "time":"13:30"})
        if (response.content.find("No records found.")==-1):
            nt.assert_false
        
    def test_billing_history(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('login.views.billing'))
        if(response.content.find("Billing History")==-1):
            nt.assert_false
            
    def test_doctor_appts(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('login.views.doctor_appts'))
        if(response.content.find("Your appointments")==-1):
            nt.assert_false
        
    def test_doctor_appts_data(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('login.views.doctor_appts'))
        if(response.content.find("testuser")==-1):
            nt.assert_false