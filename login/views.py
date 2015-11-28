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
from .models import Leave
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Document

import MySQLdb
from dateutil.parser import parse as parse_date
import datetime
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response


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
    print request.user.userrole.role
    if request.user.userrole.role == 'Doctor' or request.user.userrole.role == 'doctor':
        return render_to_response(
        'doctor_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'Patient' or request.user.userrole.role == 'patient':
        return render_to_response(
        'patient_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'Staff' or request.user.userrole.role == 'staff':
        return render_to_response(
        'staff_home.html',
        { 'user': request.user }
        )
        
    if request.user.userrole.role == 'Admin' or request.user.userrole.role == 'admin':
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
def viewappointments(request):
    viewappointments_list=[]
    doc_list = []
    leaves_list = []
    for viewappts in Appt.objects.raw('SELECT * FROM login_appt where patient_id=' + str(request.user.id)  + ';'):
            viewappointments_list.append(viewappts)
            doc_list.append(viewappts.doctor_id)
    list_count = len(viewappointments_list)
    for doc_id in set(doc_list):
        for leaves in Leave.objects.raw('SELECT * FROM login_leave where doctor_id=' + str(doc_id) + ' and status="approved";'):
            leaves_list.append(leaves.date_of_leave) 
    return render_to_response('patient/viewappointments.html',{'user': request.user, 'appts': viewappointments_list, 'count': list_count, 'leaves' : leaves_list})

@login_required
def billing(request):
    billing_list=[]
    for billings in Billing.objects.raw('SELECT * FROM login_billing where patient_id=' + str(request.user.id)  + ';'):
            billing_list.append(billings)
    list_count = len(billing_list)
    return render_to_response('patient/billing.html',{'user': request.user, 'billings': billing_list, 'count': list_count})

@login_required
@csrf_exempt
def doctor_appts(request):
    appts_list=[]
    for appts in Appt.objects.raw('SELECT * FROM login_appt where doctor_id=' + str(request.user.id)  + ';'):
            appts_list.append(appts)
    
    leaves_list=[]
    for leaves in Leave.objects.raw('SELECT * FROM login_leave where doctor_id=' + str(request.user.id) + ' and status="approved";'):
        leaves_list.append(leaves.date_of_leave)
    return render_to_response('patient/doc_appts.html',{'user': request.user, 'appts': appts_list, 'leaves': leaves_list})
    
@login_required
def doctor_leave_req(request):
    return render_to_response('doctor/leave_req.html',{'user': request.user})

@csrf_exempt
@login_required
def doctor_leave_success(request):
    user_id = request.user.id
    doctor = User.objects.get(id=user_id)
    reason = request.POST.get("Leave_reason", "")
    date_unicode = request.POST.get("date", "")
    if(parse_date(date_unicode) > datetime.now()):
        date = datetime.strptime(date_unicode, "%Y-%m-%d")
        year = datetime.now().year
        status = "pending"
        leave_object = Leave.objects.filter(doctor=doctor, current_year=year, is_latest=True)
        if leave_object:
            for object in leave_object:
                if(date.date()==object.date_of_leave):
                    return render_to_response('doctor/leave_req.html',{'user': request.user,'message':'You have already requested for leave for the particular date.'})  
                else:
                    limit = object.leave_limit
                    if(limit!=0):    
                        Leave.objects.filter(id=object.id).update(is_latest=False)
                        Leave.objects.create(doctor=doctor, reason=reason, date_of_leave=date, current_year=year, leave_limit=limit-1,status="pending",is_latest=True)
                    else:
                        return render_to_response('doctor/leave_req.html',{'user': request.user,'message':'You have exceeded the leave quota for the year.'})  
        else:
            Leave.objects.create(doctor=doctor, reason=reason, date_of_leave=date, current_year=year, leave_limit=6, status="pending",is_latest=True)
        return render_to_response('doctor/success.html')
    else:
        return render_to_response('doctor/leave_req.html',{'user': request.user,'message':'Please check the date. The system does not accept past dates.'})  

@login_required
def doctor_list_leaves(request):
    leave_list=[]
    for req in Leave.objects.raw('SELECT * FROM login_leave where doctor_id=' + str(request.user.id)  + ';'):
            leave_list.append(req)
    return render_to_response('doctor/leave_list.html',{'user': request.user, 'reqs': leave_list})

@login_required
def staff_views_leaves(request):
    leave_list=[]
    for req in Leave.objects.raw('SELECT * FROM login_leave where doctor_id=' + str(request.user.id)  + ';'):
            leave_list.append(req)
    return render_to_response('staff/leave_list.html',{'user': request.user, 'reqs': leave_list})
    
def download(request,file_name):
    file_path = 'C:/Users/kala\ suresh/Desktop/Django/ssdi_proj/myapp/media/documents/'+ file_name
    file_wrapper = FileWrapper(file(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name) 
    return response

def upload_prescription(request):
    document_success=0

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            path=''#"C:/Users/kala\ suresh/Desktop/Django/ssdi_proj/myapp/media/documents"
            path+=str(request.POST['appt_id'])+request.FILES['docfile'].name[-5:]
            
            newdoc.save()
            id = str(request.POST['appt_id'])
            Appt.objects.filter(id=id).update(prescription=path)
            document_success=1
        appts_list=[]
        for appts in Appt.objects.raw('SELECT * FROM login_appt where doctor_id=' + str(request.user.id)  + ';'):
                appts_list.append(appts)
        return render_to_response('patient/doc_appts.html',{'user': request.user, 'appts': appts_list,'document_success':document_success})
        #return render_to_response('patient/doc_appts.html',{'user': request.user, 'appts': appts_list})
    else:
        form = DocumentForm() # A empty, unbound form
    documents = Document.objects.all()
    
    return render_to_response(
        'patient/doc_appts.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
     #       print "Request method is post"
      #  form = upff(request.POST, request.FILES)
       # print "\n after importing the form\n"
        #if form.is_valid():
         #   print "before uploading"
          #  handle_uploaded_file(request.FILES['file'])
           # print "After uploading"
        #return render_to_response('patient/doc_appts.html',{'user': request.user, 'appts': appts_list})
        
#def handle_uploaded_file(f):
 #   with open('C:\Users\kala suresh\Desktop\Django\ssdi_proj\myapp\login\templates\prescriptions'+str('hello'), 'wb+') as destination:
  #      for chunk in f.chunks():
   #         destination.write(chunk)
    #    f.save()
