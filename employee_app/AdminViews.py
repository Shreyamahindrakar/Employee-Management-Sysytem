
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AddEmployeeForm,EditEmployeeForm
# from employee_app.forms import AddStudentForm, EditStudentForm
from .models import CustomUser, Position, Employee



def admin_home(request):
    return render(request,"Main_Admin_template/home_content.html")

def add_position(request):
    return render(request,"Main_Admin_template/add_position_template.html")

def add_position_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        position=request.POST.get("position")
        try:
            position_model=Position(position_name=position)
            position_model.save()
            messages.success(request,"Successfully Added position")
            return HttpResponseRedirect(reverse("add_position"))
        except:
            messages.error(request,"Failed To Add Position")
            return HttpResponseRedirect(reverse("add_position"))



def add_employee(request):
    form=AddEmployeeForm()
    return render(request,"Main_Admin_template/add_employee_template.html",{"form":form})

def add_employee_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        form=AddEmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            address=form.cleaned_data["address"]
            session_start=form.cleaned_data["session_start"]
            session_end=form.cleaned_data["session_end"]
            position_id=form.cleaned_data["position"]
            sex=form.cleaned_data["sex"]

            profile_pic=request.FILES['profile_pic']
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)

            try:
                user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
                user.employee.address=address
                position_obj=Position.objects.get(id=position_id)
                user.employee.position_id=position_obj
                user.employee.session_start_year=session_start
                user.employee.session_end_year=session_end
                user.employee.gender=sex
                user.employee.profile_pic=profile_pic_url
                user.save()
                messages.success(request,"Successfully Added Employee")
                return HttpResponseRedirect(reverse("add_employee"))
            except:
                messages.error(request,"Failed to Add Employee")
                return HttpResponseRedirect(reverse("add_employee"))
        else:
            form=AddEmployeeForm(request.POST)
            return render(request, "Main_Admin_template/add_employee_template.html", {"form": form})

def manage_employee(request):
    employee=Employee.objects.all()
    return render(request,"Main_Admin_template/manage_employee_template.html",{"employee":employee})

def manage_position(request):
    position=Position.objects.all()
    return render(request,"Main_Admin_template/manage_position_template.html",{"position":position})


def edit_employee(request,employee_id):
    request.session['employee_id']=employee_id
    employee=Employee.objects.get(admin=employee_id)
    form=EditEmployeeForm()
    form.fields['email'].initial=employee.admin.email
    form.fields['first_name'].initial=employee.admin.first_name
    form.fields['last_name'].initial=employee.admin.last_name
    form.fields['username'].initial=employee.admin.username
    form.fields['address'].initial=employee.address
    form.fields['position'].initial=employee.position_id.id
    form.fields['sex'].initial=employee.gender
    form.fields['session_start'].initial=employee.session_start_year
    form.fields['session_end'].initial=employee.session_end_year
    return render(request,"Main_Admin_template/edit_employee_template.html",{"form":form,"id":employee_id,"username":employee.admin.username})

def edit_employee_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        employee_id=request.session.get("employee_id")
        if employee_id==None:
            return HttpResponseRedirect(reverse("manage_employee"))

        form=EditEmployeeForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            address = form.cleaned_data["address"]
            session_start = form.cleaned_data["session_start"]
            session_end = form.cleaned_data["session_end"]
            position_id = form.cleaned_data["position"]
            sex = form.cleaned_data["sex"]

            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs=FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url=None


            try:
                user=CustomUser.objects.get(id=employee_id)
                user.first_name=first_name
                user.last_name=last_name
                user.username=username
                user.email=email
                user.save()

                employee=Employee.objects.get(admin=employee_id)
                employee.address=address
                employee.session_start_year=session_start
                employee.session_end_year=session_end
                employee.gender=sex
                position=Position.objects.get(id=position_id)
                employee.position_id=position
                if profile_pic_url!=None:
                    employee.profile_pic=profile_pic_url
                employee.save()
                del request.session['employee_id']
                messages.success(request,"Successfully Edited employee")
                return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
            except:
                messages.error(request,"Failed to Edit employee")
                return HttpResponseRedirect(reverse("edit_employee",kwargs={"employee_id":employee_id}))
        else:
            form=EditEmployeeForm(request.POST)
            employee=Employee.objects.get(admin=employee_id)
            return render(request,"Main_Admin_template/edit_employee_template.html",{"form":form,"id":employee_id,"username":employee.admin.username})


def edit_position(request,position_id):
    position=Position.objects.get(id=position_id)
    return render(request,"Main_Admin_template/edit_position_template.html",{"position":position,"id":position_id})

def edit_position_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        position_id=request.POST.get("position_id")
        position_name=request.POST.get("position")

        try:
            position=Position.objects.get(id=position_id)
            position.position_name=position_name
            position.save()
            messages.success(request,"Successfully Edited position")
            return HttpResponseRedirect(reverse("edit_position",kwargs={"position_id":position_id}))
        except:
            messages.error(request,"Failed to Edit position")
            return HttpResponseRedirect(reverse("edit_position",kwargs={"position_id":position_id}))


