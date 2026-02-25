from django.http import HttpResponse
from django.shortcuts import render

from app_core.models import Question, category, councellor, district, location
from app_dashboard.models import customer
from app_patient.models import Payment
from neurosense.users.models import User


# Create your views here.
def dis_entry(request):
    if request.method=='POST' :
        print ("submission successfull")
        name= request.POST.get('Name')
        print (name)
        if district.objects.filter(Name=name).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/district/';</script>")
        dis=district()
        dis.Name=name
        dis.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/district/';</script>" )
    else:
        return render(request,"disreg.html")
def vdis(request):
    d=district.objects.all()
    return render(request ,'disview.html',{'vdi':d})
def ddel(request, ddel):
   de=district.objects.get(id=ddel)
   de.delete()
   return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/disview/';</script>" )
def dedit(request,dedit):
   s=district.objects.get(id=dedit)
   if request.method=='POST' :
        print ("submission successfull")
        name= request.POST.get('Name')
        print (name)
        if district.objects.filter(Name=name).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/disview/';</script>")
        
        s.Name=name
        s.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/disview/';</script>" )
   else:
        
#  return HttpResponse("<script>alert('Deleted Successfully');window.location='/home/vcat';</script>" )
    return render(request,'editdis.html',{'dedit':s})
def loc(request):
    if request.method=='POST' :
        print ("submission success")
        name= request.POST.get('Name')
        dist=request.POST.get('district')
        print (name,dist)
        if location.objects.filter(Name=name ,dist=dist ).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/location/';</script>")
        loc=location()
        loc.Name=name
        loc.dist=district.objects.get(id=dist)
        loc.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/location/';</script>" )
    else:
        d=district.objects.all()
        return render(request,"location.html",{'vdi':d})
def vloc(request):
    l=location.objects.all()
    return render(request ,'viewloc.html',{'vdi':l})

def ldel(request, Id):
   lo=location.objects.get(id=Id)
   lo.delete()
   return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/locview/';</script>" )

def ledit(request,ledit):
    loc=location.objects.get(id=ledit)
    if request.method=='POST' :
        print ("submission success")
        name= request.POST.get('Name')
        dist=request.POST.get('district')
        print (name,dist)
        loc.Name=name
        loc.dist=district.objects.get(id=dist)
        loc.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/locview/';</script>" )
    else:
         
         dis=district.objects.all()
         return render(request,"editloc.html",{'loc':loc,'dist':dis})


def cate(request):
    if request.method=='POST' :
        name = request.POST.get("Name")
        print ("submission successfull")
        desc = request.POST.get('desc')
        if category.objects.filter(Name=name).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/district/';</script>")
        
        catobj = category()
        catobj.Name = name
        catobj.desc = desc
        print (name)
        if len(request.FILES) != 0:
            catimg = request.FILES['img']
        else:
            catimg = 'images/default.jpg'
        catobj.img=catimg
        catobj.save()
        
     
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/category/';</script>" )
    else:
        return render(request,"category.html")
    

def viewcat(request):
    c=category.objects.all()
    return render(request ,'catview.html',{'vdi':c})

def cdel(request, Id):
   lo=category.objects.get(id=Id)
   lo.delete()
   return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/viewcat/';</script>" )

def cedit(request,cedit):
   c=category.objects.get(id=cedit)
   if request.method=='POST' :
        print ("submission successfull")
        name= request.POST.get('Name')
        desc=request.POST.get('desc')
        img=request.FILES['img']
        print (name)
        if category.objects.filter(Name=name).exclude(id=cedit).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/viewcat/';</script>")
        c.Name=name
        c.desc=desc
        if img:
            c.img=img
        c.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/viewcat/';</script>" )
   else:
        
#  return HttpResponse("<script>alert('Deleted Successfully');window.location='/home/vcat';</script>" )
    return render(request,'editcat.html',{'cedit':c})
   






# def con(request):
#     if request.method=='POST' :
#         print ("submission success")
#         name= request.POST.get('name')
#         special=request.POST.get('special')
#         exp=request.POST.get('exp')
#         number=request.POST.get('number')
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         mail=request.POST.get('mail')
#         contact=request.POST.get('contact')
#         gender=request.POST.get('gender')
#         print (name,special,exp,number,number,username,password,mail,contact,gender)
#         if councellor.objects.filter(Name=name,).exists():
#             return HttpResponse("<script>alert('Already Exists');window.location='/core/con/';</script>")
#         loc=councellor()
#         loc.name=name
#         loc.dist=User.objects.get(id=dist)
#         loc.save()
#         return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/con/';</script>" )
#     else:
#         d=User.objects.all()
#         return render(request,"councillor.html",{'vdi':d})
   

def vcon(request):
    c=councellor.objects.filter(status='Processing')
    return render(request ,'viewcon.html',{'vdi':c})

def vacc(request):
    c=councellor.objects.filter(status='Accept')
    return render(request ,'accepted.html',{'vdi':c})



def delete(request,id):
    r=councellor.objects.get(id=id)
    r.status="Reject" 
    r.save()
    return HttpResponse("<script>alert('Removed Successfully');window.location='/core/vcon/';</script>")

def accept(request,id):
    c =councellor.objects.get(id =id)
    c.status="Accept"
    c.save()
    return HttpResponse("<script>alert('Counselor Approved Successfully');window.location='/core/vcon/';</script>")

def vcust(request):
    c=customer.objects.all()
    return render(request ,'viewcus.html',{'vdi':c})


def ques(request):
    if request.method=='POST' :
        print ("submission successfull")
        question= request.POST.get('question')
        print (question)
        if Question.objects.filter(question=question).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/question/';</script>")
        q=Question()
        q.question=question
        q.save()
        return HttpResponse("<script>alert('Inserted Successfully');window.location='/core/question/';</script>" )
    else:
        return render(request,"question.html")



def qview(request):
    d=Question.objects.all()
    return render(request ,'qview.html',{'vdi':d})


def qdel(request, ddel):
   de=Question.objects.get(id=ddel)
   de.delete()
   return HttpResponse("<script>alert('Deleted Successfully');window.location='/core/qview/';</script>" )
def qedit(request,qedit):
   s=Question.objects.get(id=qedit)
   if request.method=='POST' :
        print ("submission successfull")
        question= request.POST.get('question')
        print (question)
        if Question.objects.filter(question=question).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/core/qview/';</script>")
        
        s.question=question
        s.save()
        return HttpResponse("<script>alert('Edited Successfully');window.location='/core/qview/';</script>" )
   else:
        
#  return HttpResponse("<script>alert('Deleted Successfully');window.location='/home/vcat';</script>" )
    return render(request,'qedit.html',{'qedit':s})
   

def vappoint(request):
    c=Payment.objects.all()
    return render(request ,'appoint.html',{'vdi':c})