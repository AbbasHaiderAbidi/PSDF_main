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
    
    path('admin_control_panel/', views.control_panel, name="admin_control_panel"),
    
    path('approve_user/<str:userid>',views.approve_user, name='approve_user' ),
    path('reject_user/<str:userid>',views.reject_user, name='reject_user' ),
    path('ban_user/<str:userid>',views.ban_user, name='ban_user' ),
    path('allow_user/<str:userid>',views.allow_user, name='allow_user' ),
    path('downloadformat/<str:thisdoc>', views.downloadformat, name="downloadformat"),
    path('uploadformat/', views.uploadformat, name="uploadformat"),
    
    #Project_handling
    path('download_temp_project/<str:projid>', views.download_temp_project, name="download_temp_project"),
    path('acceptdpr/<str:projid>', views.acceptdpr, name="acceptdpr"),
    path('rejectdpr/<str:projid>', views.rejectdpr, name="rejectdpr"),
    path('notificationread/<str:userid>', views.notificationread, name="notificationread")
    
    
]