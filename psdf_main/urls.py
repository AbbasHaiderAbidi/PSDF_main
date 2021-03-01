from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginPage, name = ""),
    path('register/', views.register , name = "register"),
    path('newdpr/', views.newdpr , name = "newdpr"),
    path('logout/', views.logout, name="logout"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_pending_users/', views.admin_pending_users, name="admin_pending_users"),
    path('admin_pending_projects/', views.admin_pending_projects, name="admin_pending_projects"),
    path('admin_users/', views.admin_users, name="admin_users"),
    path('approve_user/<str:userid>',views.approve_user, name='approve_user' ),
    path('reject_user/<str:userid>',views.reject_user, name='reject_user' ),
    path('ban_user/<str:userid>',views.ban_user, name='ban_user' ),
    path('allow_user/<str:userid>',views.allow_user, name='allow_user' ),
    path('downloadformat/', views.downloadformat, name="downloadformat"),
    path('download_temp_project/<str:projid>', views.download_temp_project, name="download_temp_project"),
    path('reject_project/<str:projid>', views.reject_project, name="reject_project"),
    path('approve_project/<str:projid>', views.approve_project, name="approve_project"),
    
]