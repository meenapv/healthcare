"""myapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from login import views
from login.views import *
from django.conf import settings
#include('password_reset.urls')


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]

from django.conf.urls import patterns, include, url
from login.views import *
 
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', logout_page),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'), # If user is not login it will redirect to login page
    url(r'^register/$', register),
    url(r'^register/success/$', register_success),
    url(r'^home/$', home),
    
    url(r'^user/password/reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'post_reset_redirect' : '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'post_reset_redirect' : '/user/password/done/'}),
    url(r'^user/password/done/$', 
        'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
        
    url(r'^user/bookappt/$','login.views.appointment'),
    url(r'^user/bookappt_success/$','login.views.apptsuccess'),
    url(r'^user/medical_history/$','login.views.medical'),
    url(r'^user/billing_history/$','login.views.billing'),
    url(r'^user/viewappointments/$','login.views.viewappointments'),
    #url(r'^media/$',settings.MEDIA_URL),
    url(r'^user/appts_history/$','login.views.doctor_appts'),
    url(r'^user/appts_history/upload/$','login.views.upload_prescription'),
    url(r'^download/(?P<file_name>.+)$', 'login.views.download'),
    
    url(r'^user/leaverequest/$','login.views.doctor_leave_req'),
    url(r'^user/leaverequest_success/$','login.views.doctor_leave_success'),
    url(r'^user/leavehistory/$','login.views.doctor_list_leaves'),
    url(r'^user/sanction_leave/$','login.views.staff_views_leaves')
 
)