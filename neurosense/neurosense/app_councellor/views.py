from django.http import HttpResponse
from django.shortcuts import render

from app_dashboard.models import customer
from app_patient.models import Appointment,Result
import uuid
# Create your views here.
from django.core.mail import send_mail


def vhome(request):
    return render(request, "home.html")

def vcusto(request):
    c=Appointment.objects.filter(councellor=request.user)
    return render(request ,'customer.html',{'vdi':c})


def report_view(request,id):
        
    c=Appointment.objects.get(id=id)
    report = Result.objects.filter(patient_id=c.customer).order_by('-id')[:10]

    report_list = []

    for r in report:
        probability = float(r.result)

        if probability < 40:
            risk_level = "Low"
            
        elif probability < 70:
            risk_level = "Moderate"
          
        else:
            risk_level = "High"
           
        report_list.append({
            "id": r.id,
            "result": r.result,
            "risk_level": risk_level,
           
        })


    if request.method=="POST":
        # 1. Create the Doctor Appointment
        meeting_link = None

        meeting_id = uuid.uuid4().hex[:8]
        meeting_link = f"https://meet.jit.si/neurosense-{meeting_id}"

        
        c.meeting_link=meeting_link
        c.save()
        


        # ✅ Send confirmation email
        email_message = (
            f"Hi {c.customer.name},\n\n"
            f"Your consultation with {c.councellor.name} is scheduled for "
            f"{c.appointmentdate} at {c.appointmenttime.strftime('%H:%M')}.\n"
        )
        email_message += f"Since this is an online consultation, please join the meeting using this link: {meeting_link}\n\nThank you for choosing Neurosense!"
        
        send_mail(
            subject="Doctor Appointment Confirmed!",
            
            message=email_message,
            from_email=None,
            recipient_list=[c.customer.email],
        )
        return HttpResponse("<script>alert('Meeting Scheduled Successfully');window.location='/councellor/vhome/';</script>" )

    return render(request ,'customer_result.html',{'app':c,"report": report_list,})

def report_detail_view(request,id):
    data=Result.objects.get(id=id)
    score = float(data.result)

    if score < 40:
        risk = "Low"
    elif score < 70:
        risk = "Moderate"
    else:
        risk = "High"
    return render(request,"result_detail.html",{"data":data,"risk":risk})