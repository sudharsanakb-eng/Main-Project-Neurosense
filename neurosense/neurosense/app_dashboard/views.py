from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login

from app_dashboard.models import customer
from app_core.models import Question, councellor
from neurosense.users.models import User
from django.core.mail import send_mail
# Create your views here.
def appdash(request):
    return render(request,"admin.html")

def guest(request):
    return render(request,"guest.html")

def userdash2(request):
    return render(request,"userdash2.html") 


def login_view(request):
    if request.method =='POST':
        name=request.POST.get("Name")
        password=request.POST.get("password")
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            if user.role=="councillor":
                con=councellor.objects.get(user=user)
                if con.status=="Accept":
                    return HttpResponse("<script>alert('Login Successfully');window.location='/councellor/vcusto/';</script>" )
                else:
                    return HttpResponse("<script>alert('Verification pending..PLease wait!!!!!');window.location='/dashboard/counsellor/';</script>" )

            elif user.role=="User":
                return HttpResponse("<script>alert('Login Successfully');window.location='/dashboard/userdash2';</script>" )
            elif user.role=="admin":
                return HttpResponse("<script>alert('Login Successfully');window.location='/dashboard/admin';</script>" )
        else:
            return HttpResponse("<script>alert('Login Invalid');window.location='/dashboard/login';</script>" )
    return render(request,"login.html")


def cust(request):
    if request.method=="POST":
        name=request.POST.get("name")
        address=request.POST.get("address")
        dob=request.POST.get("dob")
        age=request.POST.get("age")
        uname=request.POST.get("username")
        passwd=request.POST.get("password")
        mail=request.POST.get("email")
        contact_no=request.POST.get("contact")
        gender=request.POST.get("gender")
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/dashboard/cust';</script>")
        u=User()
        u.name=name
        u.username=uname
        u.set_password(passwd)
        u.email=mail
        u.role="User"
        u.save()
        # id=User.objects.get(id,username=uname)

        c=customer()
        c.address=address
        c.dob=dob
        c.age=age
        c.contact=contact_no
        c.gender=gender
        c.user=User.objects.get(username=uname)
        c.save()
        send_mail(subject="Regististration success", message=f"hii {name},\n Your account has created successfully..",from_email=None,recipient_list=[mail])
        return HttpResponse("<script>alert('Insertion sucessfull');window.location='/dashboard/login';</script>")
    else:
        return render(request, "cuslogin.html")
    
def counsellor(request):
    return render(request,"counsellordash.html")

def userdash(request):
    return render(request,"userdash.html")


def qview(request):
    d=Question.objects.all()
    return render(request ,'ques.html',{'vdi':d})



def con(request):
    if request.method=="POST":
        name=request.POST.get("name")
        specialisation=request.POST.get("special")
        exp=request.POST.get("exp")
        doc_no=request.POST.get("number")
        uname=request.POST.get("username")
        passwd=request.POST.get("password")
        mail=request.POST.get("email")
        contact_no=request.POST.get("contact")
        gender=request.POST.get("gender")
        about=request.POST.get("desc")
        count=request.POST.get("count")
        fee=request.POST.get("fee")
        
        if User.objects.filter(username=uname).exists():
            return HttpResponse("<script>alert('Already Exist');window.location='/dashboard/con';</script>")
        u=User()
        u.name=name
        u.username=uname
        u.set_password(passwd)
        u.email=mail
        u.role="councillor"
        u.save()
        # id=User.objects.get(id,username=uname)

        c=councellor()
        c.special=specialisation
        c.exp=exp
        c.number=doc_no
        c.contact=contact_no
        c.gender=gender
        c.user=User.objects.get(username=uname)
        c.desc=about
        c.fee=fee
        if len(request.FILES) != 0:
            photo = request.FILES['img']
        else:
            photo = 'images/default.jpg'
        c.photo=photo
        c.count=count
        c.save()
        
        return HttpResponse("<script>alert('Insertion sucessfull');window.location='/dashboard/con';</script>")
    else:
        return render(request, "councillor.html")