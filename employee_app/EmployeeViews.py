import datetime

from django.shortcuts import render

from employee_app.models import *


def employee_home(request):
    return render(request,"employee_template/employee_home_template.html")

def employee_view_attendence(request):
    employee=Employee.objects.get(admin=request.user.id)
    position=employee.position_id

    return render(request,"employee_template/employee_view_attendance.html",{'position':position})

def employee_view_attendance_post(request):
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse=datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data_parse=datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    user_object=CustomUser.objects.get(id=request.user.id)
    emp_obj=Employee.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse))
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,employee_id=emp_obj)
    return render(request,"employee_template/employee_attendance_data.html",{"attendance_reports":attendance_reports})
