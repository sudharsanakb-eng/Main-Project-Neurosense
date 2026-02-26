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
    report=Result.objects.filter(patient_id=c.customer)
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

    return render(request ,'result.html',{'app':c,"report":report})

