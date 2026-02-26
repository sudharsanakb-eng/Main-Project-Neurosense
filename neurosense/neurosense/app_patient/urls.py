from django.urls import path

from neurosense.app_patient import views


app_name="user"



urlpatterns = [
path('vcon/',views.vcon,name='vcon'),
path('vdetail/<int:id>',views.vdetail,name='vdetail'),
path('app/<int:id>',views.app,name='app'),
path('payments/<int:id>',views.payments,name='payments'),
path('payentry/<int:id>',views.payentry,name='payentry'),
path('booking-history/', views.booking_history, name='booking_history'),
]