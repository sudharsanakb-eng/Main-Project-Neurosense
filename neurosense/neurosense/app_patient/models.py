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
    result=models.CharField(null=True,blank=True)
    What_is_your_gender=models.CharField(null=True,blank=True)
    What_is_your_age=models.FloatField(null=True,blank=True)
    Which_city_do_you_currently_live_in=models.CharField(null=True,blank=True)
    working_professional_or_student=models.CharField(null=True,blank=True)
    What_is_your_profession=models.CharField(null=True,blank=True)
    How_would_you_rate_your_work_pressure_level=models.FloatField(null=True,blank=True)
    How_satisfied_are_you_with_your_job_or_studies=models.FloatField(null=True,blank=True)
    How_many_hours_do_you_sleep_on_average_per_day=models.CharField(null=True,blank=True)
    How_would_you_describe_your_dietary_habits=models.CharField(null=True,blank=True)
    What_is_your_highest_educational_qualification=models.CharField(null=True,blank=True)
    Have_you_ever_experienced_suicidal_thoughts=models.CharField(null=True,blank=True)
    How_many_hours_per_day_do_you_spend_working_or_studying=models.FloatField(null=True,blank=True)
    How_would_you_rate_your_current_financial_stress_level=models.FloatField(null=True,blank=True)
    Is_there_any_history_of_mental_illness_in_your_family=models.CharField(null=True,blank=True)



