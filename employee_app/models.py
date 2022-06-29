from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# superuser: Username:Admin,Email:Admin@gmail.com,Password:1234

# Create your models here.
class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Employee"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class AdminMain(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


class Position(models.Model):
    id=models.AutoField(primary_key=True)
    position_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()
    
    def __str__(self):
        return self.position_name


class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    position_id=models.ForeignKey(Position,on_delete=models.DO_NOTHING)
    session_start_year=models.DateField()
    session_end_year=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    
    # def __str__(self):
    #     return self.admin
attendance_choices = (
    ('absent', 'Absent'),
    ('present', 'Present')
)
class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    position=models.ForeignKey(Position,on_delete=models.CASCADE)
    attendance = models.CharField(max_length=8, choices=attendance_choices, blank=True)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    employee=models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminMain.objects.create(admin=instance)
        if instance.user_type==2:
            Employee.objects.create(admin=instance,position_id=Position.objects.get(id=1),session_start_year="2020-01-01",session_end_year="2021-01-01",address="",profile_pic="",gender="")

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminmain.save()
    if instance.user_type==2:
        instance.employee.save()
