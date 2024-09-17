from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import *
from django.contrib.auth import *
from django.shortcuts import redirect
from django.contrib import messages
import datetime
# Create your views here.

def home(request):
    return render(request, 'home.html')

def user_dashboard(request):
    jobs = Job.objects.all().order_by('-start_date')
    user = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=user)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "jobs.html", {'jobs':jobs,'user':user, 'data':data})
    # return render(request, 'user_dashboard.html')

def user_home(request):
    if not request.user.is_authenticated:
        return redirect('/user-home')
    applicant = Applicant.objects.get(user=request.user)
    if request.method=="POST":   
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']
 
        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()
 
        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()
        except:
            pass
        alert = True
        return render(request, "user_home.html", {'alert':alert})
    return render(request, "user_home.html", {'applicant':applicant})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("/user-login")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
 
            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("/user-dashboard")
            else:
                thank = False
                return render(request, "login.html", {"thank":thank})
    return render(request, "login.html")

        
def signup(request):
    if request.method=="POST":   
        username = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone = request.POST['phone']
        gender = request.POST['gender']
        image = request.FILES['image']
 
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=password1)
        applicants = Applicant.objects.create(user=user, phone=phone, gender=gender, image=image, type="applicant")
        user.save()
        applicants.save()
        return render(request, "login.html")
    return render(request, "signup.html")

def all_jobs(request):
    jobs = Job.objects.all().order_by('-start_date')
    applicant = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, "jobs.html", {'jobs':jobs, 'data':data})

def job_detail(request, id):
    job = Job.objects.get(id=id)
    return render(request, "job_detail.html", {'job':job})

def job_apply(request, id):
    if not request.user.is_authenticated:
        return redirect("/user-login")
    applicant = Applicant.objects.get(user=request.user)
    job = Job.objects.get(id=id)
    date1 = datetime.date.today()
    if job.end_date < date1:
        closed=True
        return render(request, "job_apply.html", {'closed':closed})
    elif job.start_date > date1:
        notopen=True
        return render(request, "job_apply.html", {'notopen':notopen})
    else:
        if request.method == "POST":
            resume = request.FILES['resume']
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume, apply_date=datetime.date.today())
            alert=True
            return redirect("/user-dashboard")
        
    return render(request, "job_apply.html", {'job':job})

