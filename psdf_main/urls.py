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
    path('update_boq/<str:projectid>', views.update_boq, name="update_boq"),
    path('admin_control_panel/', views.control_panel, name="admin_control_panel"),

    path('approve_user/<str:userid>',views.approve_user, name='approve_user' ),
    path('reject_user/<str:userid>',views.reject_user, name='reject_user' ),
    path('ban_user/<str:userid>',views.ban_user, name='ban_user' ),
    path('allow_user/<str:userid>',views.allow_user, name='allow_user' ),
    path('downloadformat/<str:thisdoc>', views.downloadformat, name="downloadformat"),
    path('uploadformat/', views.uploadformat, name="uploadformat"),

    #Project_handling
    path('download_temp_project/<str:projid>', views.download_temp_project, name="download_temp_project"),
    path('download_project/<str:projid>', views.download_project, name="download_project"),
    path('acceptdpr/<str:projid>', views.acceptdpr, name="acceptdpr"),
    path('rejectdpr/<str:projid>', views.rejectdpr, name="rejectdpr"),
    path('notificationread/<str:userid>', views.notificationread, name="notificationread"),

    #pending_projects
    path('under_examination/', views.underexamination, name="under_examination"),

    #view Users
    path('view_user/<str:userid>', views.view_user, name="view_user/"),

    #TESG
    path('TESG_chain/<str:project_id>', views.TESG_chain, name = "TESG_chain"),
    path('tesgchain_form/', views.tesgchain_form, name = "tesgchain_form"),
    path('TESG_projects/', views.TESG_projects, name="TESG_projects"),
    path('TESG_upload/', views.TESG_upload, name="TESG_upload"),
    path('rejectproject/<str:projid>', views.rejectproject, name="rejectproject"),
    path('acceptTESG/', views.acceptTESG, name="acceptTESG"),
    path('rejectTESG/', views.rejectTESG, name="rejectTESG"),
    path('user_tesg/', views.user_tesg, name="user_tesg"),
    path('downloadTESGresponse/<str:tesgid_projid>', views.downloadTESGresponse, name = "downloadTESGresponse"),
    path('downloadTESGrequest/<str:tesgid_projid>', views.downloadTESGrequest, name = "downloadTESGrequest"),
    path('user_TESG_chain/<str:projid>', views.user_TESG_chain, name = "user_TESG_chain"),
    path('user_tesg_response', views.user_tesg_response, name = "user_tesg_response"),
    path('approveTESG/<str:projid>', views.approveTESG, name = "approveTESG"),
    path('download_tesg_user_outcome/<str:tesg_str>', views.download_tesg_user_outcome, name = "download_tesg_user_outcome"),
    path('download_tesg_user_response/<str:tesg_str>', views.download_tesg_user_response, name = "download_tesg_user_response"),
    path('admin_project_details/<str:projectid>', views.admin_project_details, name = "admin_project_details"),
    path('view_TESGs', views.view_TESGs, name = "view_TESGs"),
    path('download_tesg_report/<str:tesgid>', views.download_tesg_report, name = "download_tesg_report"),
    path('update_appraisal/<str:projid>', views.update_appraisal, name = "update_appraisal"),

    #Appraisal
    path('appraisal_projects/', views.appraisal_projects, name="appraisal_projects"),
    path('approve_appraisal/<str:projectid>', views.approve_appraisal, name="approve_appraisal"),
    path('delete_appr_doc/<str:projid>', views.delete_appr_doc, name = 'delete_appr_doc'),
    path('send_to_tesg/<str:projid>', views.send_to_tesg, name = 'send_to_tesg'),
    path('update_appraisal/<str:projid>', views.update_appraisal, name = 'update_appraisal'),
    path('create_appraisal/<str:projid>', views.create_appraisal, name = 'create_appraisal'),
    
    path('user_appraisal_projects/', views.user_appraisal_projects, name="user_appraisal_projects"),
    
    
    #monitoring
    path('monitoring_projects/', views.monitoring_projects, name="monitoring_projects"),
    path('approve_monitoring/<str:projectid>', views.approve_monitoring, name="approve_monitoring"),
    path('send_to_appr/<str:projid>', views.send_to_appr, name="send_to_appr"),
    path('send_to_tesg/<str:projid>', views.send_to_tesg, name="send_to_tesg"),
    path('user_monitoring_projects/', views.user_monitoring_projects, name="user_monitoring_projects"),

 
 
    
]