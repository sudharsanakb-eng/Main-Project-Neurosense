from django.db import models


from neurosense.users.models import User

# Create your models here.
class customer(models.Model):
    address=models.CharField()
    dob=models.CharField()
    gender=models.CharField()
    age=models.CharField()
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    contact=models.CharField()

