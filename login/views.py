from django.shortcuts import render

# Create your views here.
#views.py
from login.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db import models
from .models import UserRole
from .models import Appt
from .models import Billing
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from dateutil.parser import parse as parse_date
import datetime
from datetime import datetime, timedelta

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            UserRole.objects.create(user_id = user.id, role = 'patient');
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )
 
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
    if request.user.userrole.role == 'doctor':
        return render_to_response(
        'doctor_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'patient':
        return render_to_response(
        'patient_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'staff':
        return render_to_response(
        'staff_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'admin':
        return render_to_response(
        'admin_home.html',
        { 'user': request.user }
        )

@csrf_exempt
@login_required
def appointment(request):
    doctor_list=[]
    for doctor in User.objects.raw('SELECT * FROM auth_user a join login_userrole b on a.id=b.user_id where b.role="doctor";'):
            doctor_list.append(doctor)
    return render_to_response('patient/appointment.html',{'user': request.user, 'doctor': doctor_list})



@login_required
#@csrf_protect
@csrf_exempt
def apptsuccess(request):
    flag =True
    p_name = request.user.id
    p_user = User.objects.get(id=p_name)
    d_name = request.POST.get("Doctor_name", "")
    d_user = User.objects.get(id=d_name)
    medProblem = request.POST.get("Medical_problem", "")
    date_unicode = request.POST.get("date", "")
    time_unicode = request.POST.get("time1", "")
    

    if(p_name!=None and p_name!="" and d_name!=None and d_name!='' and medProblem!=None and medProblem!='' and date_unicode!=None and date_unicode!='' and time_unicode!=None and time_unicode!="" and parse_date(date_unicode) > datetime.now()):
        time_list=[]
        db_date_list=[]
        timedelta_list=[]
        date_list=[]
        date = datetime.strptime(date_unicode, "%Y-%m-%d")
        time = datetime.strptime(time_unicode, "%H:%M")
        calendar_date = datetime.strptime(date_unicode+" " +time_unicode, "%Y-%m-%d %H:%M")
        for a in User.objects.raw('SELECT * FROM login_appt;'):
            if(a.doctor_id == long(d_name)):
                time_list.append(a.time)
                date_list.append(a.date)
                db_date_list.append(datetime.combine(a.date,a.time))
              
        if(calendar_date in db_date_list):
            flag=False
        else:
            for d in db_date_list:
                time_added = d + timedelta(minutes=15)
                if(calendar_date<time_added and calendar_date>d):
                    flag=False
                    break
                else:
                    flag=True
                    continue
                                    
        if flag==False:
            doctor_list=[]
            for doctor in User.objects.raw('SELECT * FROM auth_user a join login_userrole b on a.id=b.user_id where b.role="doctor";'):
                doctor_list.append(doctor)
            return render_to_response('patient/appointment.html',{'user': request.user, 'doctor': doctor_list, 'message':'Sorry, There is a time clash, please select a different time.'})
        else:
            d = Appt.objects.create(patient=p_user,doctor=d_user,medical_problem=medProblem,date=date,time=time)
            d.save()
            return render_to_response('patient/success.html',{'user': request.user})
        
    else:
        doctor_list=[]
        for doctor in User.objects.raw('SELECT * FROM auth_user a join login_userrole b on a.id=b.user_id where b.role="doctor";'):
            doctor_list.append(doctor)
        return render_to_response('patient/appointment.html',{'user': request.user, 'doctor': doctor_list, 'message':'Either the information you have filled is incorrect or empty. Please check.'})
    d = Appt.objects.create(patient=p_user,doctor=d_user,medical_problem=medProblem,date=date,time=time)
    d.save()
    return render_to_response('patient/success.html',{'user': request.user})


@login_required
def medical(request):
    appts_list=[]
    for appts in Appt.objects.raw('SELECT * FROM login_appt where patient_id=' + str(request.user.id)  + ';'):
            appts_list.append(appts)
    list_count = len(appts_list)
    return render_to_response('patient/medical.html',{'user': request.user, 'appts': appts_list, 'count': list_count})


@login_required
def billing(request):
    billing_list=[]
    for billings in Billing.objects.raw('SELECT * FROM login_billing where patient_id=' + str(request.user.id)  + ';'):
            billing_list.append(billings)
    list_count = len(billing_list)
    return render_to_response('patient/billing.html',{'user': request.user, 'billings': billing_list, 'count': list_count})

@login_required
def doctor_appts(request):
    appts_list=[]
    for appts in Appt.objects.raw('SELECT * FROM login_appt where doctor_id=' + str(request.user.id)  + ';'):
            appts_list.append(appts)
    return render_to_response('patient/doc_appts.html',{'user': request.user, 'appts': appts_list})
