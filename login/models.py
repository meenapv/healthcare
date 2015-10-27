from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserRole(models.Model):
    user = models.OneToOneField(User)
    role = models.CharField(max_length=15)
    
User.roles = property(lambda u:UserRole.objects.get_or_create(user=u)[0])
if User.objects.all().count() == 0:
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 1, username = "pavan", email = "p@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'doctor');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar", email = "p1@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'patient');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar1", email = "p2@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'staff');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar2", email = "p3@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'patient');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar3", email = "p4@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'patient');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar4", email = "p5@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'patient');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "kumar5", email = "p6@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'patient');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "vasudev", email = "p6@p.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'admin');
    user = User.objects.create(password = "pbkdf2_sha256$20000$PPSdjDUtdk6F$kfGsx7QOL93LcJBwk41ZxR+Iihh/vAWxIRMCPaCA6cQ=", is_superuser = 0, username = "vasudev1", email = "p6@p1.com", is_staff = 1, is_active = 1);
    UserRole.objects.create(user_id = user.id, role = 'admin');