from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name = ""),
    path('register/', views.register , name = "register"),
    path('newdpr/', views.newdpr , name = "newdpr"),
    path('logout/', views.logout, name="logout"),
]
