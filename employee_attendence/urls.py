"""employee_attendence URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employee_app import AdminViews, views,EmployeeViews
from employee_attendence import settings
from django.conf.urls.static import static

urlpatterns = [
    path('demo',views.demo),
    path('admin/', admin.site.urls),
    path('',views.ShowLoginPage,name="show_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',AdminViews.admin_home,name="admin_home"),
    path('add_position', AdminViews.add_position,name="add_position"),
    path('add_position_save', AdminViews.add_position_save,name="add_position_save"),
    path('add_employee', AdminViews.add_employee,name="add_employee"),
    path('add_employee_save', AdminViews.add_employee_save,name="add_employee_save"),
    path('manage_employee', AdminViews.manage_employee,name="manage_employee"),
    path('manage_position', AdminViews.manage_position,name="manage_position"),
    path('edit_employee/<str:employee_id>', AdminViews.edit_employee,name="edit_employee"),
    path('edit_employee_save', AdminViews.edit_employee_save,name="edit_employee_save"),
    path('edit_position/<str:position_id>', AdminViews.edit_position,name="edit_position"),
    path('edit_position_save', AdminViews.edit_position_save,name="edit_position_save"),
    #employee view
    path('employee_home', EmployeeViews.employee_home, name="employee_home"),
    path('employee_view_attendance', EmployeeViews.employee_view_attendence, name="employee_view_attendance"),
    path('employee_view_attendance_post', EmployeeViews.employee_view_attendance_post, name="employee_view_attendance_post"),
   
    

    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
