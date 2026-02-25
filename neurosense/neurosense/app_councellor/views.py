from django.http import HttpResponse
from django.shortcuts import render

from app_dashboard.models import customer
from app_patient.models import Appointment

# Create your views here.


def vcusto(request):
    c=Appointment.objects.filter(councellor=request.user)
    return render(request ,'customer.html',{'vdi':c})