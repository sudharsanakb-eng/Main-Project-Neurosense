from django.urls import path

from neurosense.app_councellor import views


app_name="councellor"

urlpatterns =  [
 path('vhome/', views.vhome, name='vhome'),
 path('vcusto/',views.vcusto,name='vcusto'),
 path('view_report/<int:id>/',views.report_view,name='view_report'),
 
 
]