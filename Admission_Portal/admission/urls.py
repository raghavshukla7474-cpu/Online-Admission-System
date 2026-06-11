from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('apply/', views.apply_view, name='apply'),
    path('upload/', views.upload_view, name='upload'),
    path('status/', views.status_view, name='status'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/application/<int:app_id>/', views.admin_application_detail, name='admin_application_detail'),
    path('admin/application/<int:app_id>/update/', views.admin_application_update, name='admin_application_update'),
    path('admin/reports/', views.admin_reports, name='admin_reports'),
    path('admin/student/<int:student_id>/delete/', views.admin_delete_student, name='admin_delete_student'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('admin/inquiries/', views.contact_messages_view, name='contact_messages'),
    path('admin/inquiries/<int:msg_id>/toggle-resolved/', views.contact_message_toggle_resolved, name='contact_message_toggle_resolved'),
    path('admin/inquiries/<int:msg_id>/delete/', views.contact_message_delete, name='contact_message_delete'),
]

