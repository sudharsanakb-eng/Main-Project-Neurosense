from datetime import date
from django.http import HttpResponse
from django.shortcuts import redirect, render

from app_core.models import councellor
from app_dashboard.models import customer
from app_patient.models import Appointment,Payment
from django.shortcuts import render, get_object_or_404
from neurosense.users.models import User
from app_dashboard.models import customer

# Create your views here.
def vcon(request):
    c=councellor.objects.filter(status='Accept')
    return render(request ,'conview.html',{'vdi':c})
def vdetail(request,id):
    c=councellor.objects.get(id=id)
    return render(request ,'details.html',{'vdi':c})

def app(request, id):
    
    # 1. Fetch the specific counsellor
    counc = get_object_or_404(councellor, id=id)

    # 2. Fetch the customer profile of logged-in user
    try:
        profile = customer.objects.get(user=request.user)
    except customer.DoesNotExist:

        profile = None

    if request.method == "POST":
        selected_date = request.POST.get("date")  # from <input type="date" name="date">

        # 3. Create appointment
        appoint = Appointment.objects.create(
            councellor=counc.user,          # counsellor is a User
            customer=request.user,          # logged-in User
            appointmentdate=selected_date   # DateField accepts YYYY-MM-DD
        )

        return redirect('user:payments', appoint.id)

    # 4. Pass data to template
    return render(
        request,
        "appoinment.html",
        {
            "councellor": counc,   # {{ councellor.user.username }}
            "customer": profile ,  # {{ customer.age }}
            "id":id
        }
    )
def payments(request,id):
    c=Appointment.objects.get(id=id)
    return render(request  ,'payment.html',{'vdi':c})

def payentry(request, id):
    if request.method == 'POST':
        appointment_obj = Appointment.objects.get(id=id)
        amt=request.POST.get("amount")
        councellor_obj = appointment_obj.councellor

        Payment.objects.create(
            appointmentid=appointment_obj,
            paymentdate=date.today(),
            amount=amt
        )

        return HttpResponse(
            "<script>alert('Payment Successful');window.location='/dashboard/userdash/';</script>"
        )