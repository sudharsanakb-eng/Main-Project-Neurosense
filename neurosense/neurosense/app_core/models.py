from django.db import models


from neurosense.users.models import User

# Create your models here.
class district(models.Model):
    Name=models.CharField()

class location(models.Model):
    Name=models.CharField()
    dist=models.ForeignKey(district, on_delete=models.CASCADE,default=1)

class category(models.Model):
    Name=models.CharField()
    desc=models.CharField()
    img=models.ImageField(upload_to="media/",null=True)

class councellor(models.Model):
    special=models.CharField()
    exp=models.CharField()
    gender=models.CharField()
    number=models.CharField()
    user=models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    contact=models.CharField()
    photo=models.ImageField(upload_to="media/",null=True,blank=True)
    desc=models.CharField(blank=True,null=True)
    count=models.CharField(blank=True,null=True)
    statuschoices=[('Accept','Accept'),('Reject','Reject'),]
    status=models.CharField(choices=statuschoices,null=False,blank=False,default='Processing')
    fee=models.CharField(blank=True,null=True)

class Question(models.Model):
    question=models.CharField()

