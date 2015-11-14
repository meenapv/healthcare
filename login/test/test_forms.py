from django.test import Client
import nose.tools as nt
from login import views
from login.views import *
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.db import models
from login.forms import *
    
class TestForms(TestCase):

    def test_register_form(self):
        form_data = {'username': 'registereduser', "password1":"password", "password2": "password","email":"register@gmail.com"}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

