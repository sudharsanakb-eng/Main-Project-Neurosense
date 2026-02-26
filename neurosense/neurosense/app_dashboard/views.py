from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate,login

from app_dashboard.models import customer
from app_core.models import Question, councellor
from neurosense.users.models import User
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib.auth import logout


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
                    return HttpResponse("<script>alert('Login Successfully');window.location='/councellor/vhome/';</script>" )
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

def logout_view(request):
    logout(request)
    return HttpResponse(
        "<script>alert('Logged out successfully');window.location='/dashboard/login/';</script>"
    )

import os
import json
import time
import pandas as pd
from django.shortcuts import render
from catboost import CatBoostClassifier, Pool


# -------------------------------------------------
# Load Model & Feature Columns (Load Once)
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "depression_model.cbm")
FEATURE_PATH = os.path.join(BASE_DIR, "feature_columns.json")

model = CatBoostClassifier()
model.load_model(MODEL_PATH)

with open(FEATURE_PATH, "r") as f:
    feature_columns = json.load(f)


# -------------------------------------------------
# Prediction View
# -------------------------------------------------

def predict_view(request):

    print("RAW POST DATA:")
    for key, value in request.POST.items():
      print(f"{key} → {value} ({type(value)})")

    if request.method == "POST":
        start_time = time.time()

        try:
            # -----------------------------
            # 1️⃣ Collect Form Data (MUST MATCH TRAINING EXACTLY)
            # -----------------------------
            print('inside')
            person = {
                "Gender": request.POST.get("Gender"),
                "Age": float(request.POST.get("Age")),
                "City": request.POST.get("City"),
                "Working Professional or Student": request.POST.get("Working Professional or Student"),
                "Profession": request.POST.get("Profession"),
                "Work Pressure": float(request.POST.get("Work Pressure")),
                "Job Satisfaction": float(request.POST.get("Job Satisfaction")),
                "Sleep Duration": request.POST.get("Sleep Duration"),
                "Dietary Habits": request.POST.get("Dietary Habits"),
                "Degree": request.POST.get("Degree"),
                "Have you ever had suicidal thoughts ?": request.POST.get("Have you ever had suicidal thoughts ?"),
                "Work/Study Hours": float(request.POST.get("Work/Study Hours")),
                "Financial Stress": float(request.POST.get("Financial Stress")),
                "Family History of Mental Illness": request.POST.get("Family History of Mental Illness")
            }
            print('person details')
            print(person)

            # -----------------------------
            # 2️⃣ Convert to DataFrame
            # -----------------------------
            df = pd.DataFrame([person])

            # Ensure correct feature order
            df = df[feature_columns]

            

            # Identify categorical columns
            cat_cols = df.select_dtypes(include="object").columns.tolist()

            test_pool = Pool(data=df, cat_features=cat_cols)

            # -----------------------------
            # 3️⃣ Get Probability of Depression (class 1)
            # -----------------------------
            prob = model.predict_proba(test_pool)[0][1]

            # -----------------------------
            # 4️⃣ Custom Threshold (Screening Friendly)
            # -----------------------------
            threshold = 0.35
            prediction = 1 if prob >= threshold else 0

            # -----------------------------
            # 5️⃣ Risk Classification
            # -----------------------------
            if prob < 0.40:
                risk_level = "Low"
                risk_color = "green"
                interpretation = "No significant depressive indicators detected."
            elif prob < 0.70:
                risk_level = "Moderate"
                risk_color = "orange"
                interpretation = "Moderate depressive indicators detected. Monitoring is recommended."
            else:
                risk_level = "High"
                risk_color = "red"
                interpretation = "High depressive risk detected. Professional consultation is strongly advised."

            end_time = time.time()

            context = {
                "risk_level": risk_level,
                "risk_color": risk_color,
                "probability": round(prob * 100, 2),
                "interpretation": interpretation,
                "duration": round(end_time - start_time, 3)
            }

            return render(request, "result.html", context)

        except Exception as e:
            return render(request, "result.html", {
                "risk_level": "Error",
                "risk_color": "black",
                "probability": 0,
                "interpretation": f"Prediction failed: {str(e)}"
            })

    return render(request, "analysis.html")