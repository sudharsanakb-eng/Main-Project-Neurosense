from datetime import date, datetime, timedelta
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

    # 1️⃣ Get selected counsellor
    counc = get_object_or_404(councellor, id=id)

    # 2️⃣ Get logged-in customer profile
    try:
        profile = customer.objects.get(user=request.user)
    except customer.DoesNotExist:
        return HttpResponse(
            "<script>alert('Customer profile not found.');window.history.back();</script>"
        )

    # 3️⃣ Handle Form Submission
    if request.method == "POST":

        selected_date = request.POST.get("date")

        if not selected_date:
            return HttpResponse(
                "<script>alert('Please select a date.');window.history.back();</script>"
            )

        # ✅ Duplicate Check (Same user, same date, same counsellor)
        if Appointment.objects.filter(
                appointmentdate=selected_date,
                customer=request.user,
                councellor=counc.user
        ).exists():

            return HttpResponse(
                f"<script>alert('You already booked on {selected_date}.');window.history.back();</script>"
            )
        booking=councellor.objects.get(id=id)
        capacity=int(booking.count)
        # ✅ Capacity Check (Max 5 bookings per day per counsellor)

        booked_count = Appointment.objects.filter(
                appointmentdate=selected_date,
                councellor=counc.user
        ).count()

        if booked_count >= capacity:
            return HttpResponse(
                f"<script>alert('No slots available on {selected_date}.');window.history.back();</script>"
            )

        # ✅ Time Slot Calculation (Optional - not stored unless model has TimeField)
        start_time = datetime.strptime("09:00", "%H:%M")
        duration_minutes = 45  # Fixed session duration

        total_minutes = booked_count * duration_minutes
        appointment_time = start_time + timedelta(minutes=total_minutes)
        appointment_time = appointment_time.time()

        # ⚠️ If you want to store appointment_time,
        # add TimeField in Appointment model

        # ✅ Create Appointment
        appoint = Appointment.objects.create(
            customer=request.user,
            councellor=counc.user,
            appointmentdate=selected_date,
            appointmenttime=appointment_time,

            status='Booked'
        )

        # Redirect to payment
        return redirect('user:payments', appoint.id)

    # 4️⃣ Render Page
    return render(
        request,
        "appoinment.html",
        {
            "councellor": counc,
            "customer": profile,
            "id": id
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
            "<script>alert('Payment Successful');window.location='/patient/booking-history/';</script>"
        )
    




def booking_history(request):

    history = Appointment.objects.filter(
        customer=request.user
    ).select_related('councellor')

    # Attach counsellor profile manually
    for i in history:
        try:
            i.counsellor_profile = councellor.objects.get(user=i.councellor)
        except councellor.DoesNotExist:
            i.counsellor_profile = None

    return render(request, "history.html", {
        "history": history
    })