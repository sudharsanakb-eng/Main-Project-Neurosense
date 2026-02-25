from django.urls import path

from neurosense.app_councellor import views


app_name="councellor"

urlpatterns =  [
 path('vcusto/',views.vcusto,name='vcusto'),

]