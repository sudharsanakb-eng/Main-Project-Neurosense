from django.db import models

# Create your models here.
from neurosense.users.models import User

# Create your models here.
class Appointment(models.Model):
    customer=models.ForeignKey(User, on_delete=models.CASCADE,related_name='appointment_customer')
    councellor=models.ForeignKey(User, on_delete=models.CASCADE,related_name='appontment_councellor')
    currentdate= models.DateField(auto_now_add=True)
    appointmentdate= models.DateField()
    appointmenttime=models.TimeField(null=True, blank=True)
    statuschoices=[('Pending','Pending'),('Booked','Booked'),]
    status=models.CharField(choices=statuschoices,null=False,blank=False,default='Processing')
    meeting_link=models.URLField(max_length=500,null=True,blank=True)

class Payment(models.Model):
    appointmentid=models.ForeignKey(Appointment, on_delete=models.CASCADE,related_name='appontment_id')
    paymentdate=models.DateField()
    amount=models.IntegerField()

class Result(models.Model):
    patient_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name="patient_result")
    result=models.FileField()
