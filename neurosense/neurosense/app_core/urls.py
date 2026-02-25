from django.urls import path

from neurosense.app_core import views


app_name="core"

urlpatterns = [
    path("district/", views.dis_entry, name='dis'),
    path("disview/", views.vdis),
    path('ddel/<int:ddel>',views.ddel,name='ddel'),
    path('dedit/<int:dedit>',views.dedit,name='dedit'),
    path('location/',views.loc,name='loc'),
    path("locview/", views.vloc),
    path('ldel/<int:Id>',views.ldel,name='ldel'),
    path('ledit/<int:ledit>',views.ledit,name='ledit'),
    path('category/',views.cate,name='cate'),
    path('viewcat/',views.viewcat,name='viewcat'),
    path('cdel/<int:Id>',views.cdel,name='cdel'),
    path('cedit/<int:cedit>',views.cedit,name='cedit'),
    path('vcon/',views.vcon,name='vcon'),
    path('vacc/',views.vacc,name='vacc'),
    path("delete/<int:id>/",views.delete,name='delete'),
    path("accept/<int:id>",views.accept,name='accept'),
    path("vcust/",views.vcust,name='cust'),
    path("question/", views.ques, name='question'),
    path("qview/", views.qview,name='qview'),
    path('qdel/<int:ddel>',views.qdel,name='qdel'),
    path('qedit/<int:qedit>',views.qedit,name='qedit'),
    path('vappoint/',views.vappoint,name='vappoint'),

]