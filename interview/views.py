from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render  
from django.urls import reverse
from interview.models import *
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect
from social_core.backends.google import GoogleOAuth2
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import get_object_or_404
import random
import string
from django.http import JsonResponse
from django.core.mail import send_mail
# Create your views here.

def is_admin(user):
    if isinstance(user, User):
        return user.roles.filter(name='Admin').exists()
    else:
        return False
def is_Interviewer(user):
    if isinstance(user, User):
        return user.roles.filter(name='Interviewer').exists()
    else:
        return False
def is_Manager(user):
    if isinstance(user, User):
        return user.roles.filter(name='Manager').exists()
    else:
        return False
def is_Student(user):
    if isinstance(user, User):
        return user.roles.filter(name='Student').exists()
    else:
        return False

def index(request):
    return render(request,"html/index.html")

def test(request):
    return render(request,"html/test.html")

#Admin_path
@login_required
@user_passes_test(is_admin)
def admin_page(request):
    return render(request,'admin/Admin_page.html')
@login_required
@user_passes_test(is_admin)
def Announcement(request):
    return render(request,'admin/Announcement.html')
@login_required
@user_passes_test(is_admin)
def FacultyMajor(request):
    faculty_all = Faculty.objects.all()
    

    return render(request,'admin/FacultyMajor.html',{"faculty":faculty_all})
@login_required
@user_passes_test(is_admin)
def Interview(request):
    Manager_roles = Role.objects.get(name="Manager")
    context = {
        "rounds" : Round.objects.all(),
        "Manager" : Manager_roles.users.all(),
        "faculty_all" : Faculty.objects.all(),
        "major_all" : Major.objects.all(),
    }
    return render(request,'admin/Interview.html',context)
@login_required
@user_passes_test(is_admin)
def Score(request):
    return render(request,'admin/Score.html')
@login_required
@user_passes_test(is_admin)
def TemporaryUser_path(request):
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.all()
    major_all = Major.objects.all()
    return render(request,'admin/TemporaryUser.html', {'users': users,'faculty_all':faculty_all,"major_all":major_all})
@login_required
@user_passes_test(is_admin)
def User_path(request):
    users = User.objects.all()
    return render(request,'admin/User.html', {'users': users})

# @login_required
# @user_passes_test(is_admin)
# def form_interview(request):
#     return render(request,'admin/form_interview.html')

@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request,'admin/admin_profile.html')

#Manager
@login_required
@user_passes_test(is_Manager)
def manager_page(request):
    return render(request,'manager/Manager_page.html')
@login_required
@user_passes_test(is_Manager)
def manage_profile(request):
    return render(request,'manager/manage_profile.html')
@login_required
@user_passes_test(is_Manager)
def Manage_personnel(request):
    return render(request,'manager/Manage_personnel.html')
@login_required
@user_passes_test(is_Manager)
def Manager_Announcement(request):
    return render(request,'manager/Manager_Announcement.html')
@login_required
@user_passes_test(is_Manager)
def Manager_interview(request):
    return render(request,'manager/Manager_interview.html')
@login_required
@user_passes_test(is_Manager)
def Manager_Score(request):
    return render(request,'manager/Manager_Score.html')
@login_required
@user_passes_test(is_Manager)
def Manager_Print_Interview(request):
    return render(request,'manager/Manager_Print_Interview.html')
@login_required
@user_passes_test(is_Manager)
def Manager_Status(request):
    return render(request,'manager/Manager_Status.html')

#Interviewer
@login_required
@user_passes_test(is_Interviewer)
def interviewer_page(request):
    return render(request,'interviewer/Interviewer_page.html')
@login_required
@user_passes_test(is_Interviewer)
def Interviewer_Profile(request):
    return render(request,'interviewer/Interviewer_Profile.html')
@login_required
@user_passes_test(is_Interviewer)
def Interviewer_room(request):
    return render(request,'interviewer/Interviewer_room.html')





#Student
@login_required
@user_passes_test(is_Student)
def student_page(request):
    return render(request,'student/Student_page.html')
@login_required
@user_passes_test(is_Student)
def Student_profile(request):
    return render(request,'student/Student_profile.html')
@login_required
@user_passes_test(is_Student)
def Student_register(request):
    return render(request,'student/Student_register.html')
@login_required
@user_passes_test(is_Student)
def Student_room(request):
    return render(request,'student/Student_room.html')
@login_required
@user_passes_test(is_Student)
def Student_evidence(request):
    return render(request,'student/Student_evidence.html')


def confirm_otp(request):
    return render(request,'student/confirm_otp.html')

def send_email_password(request):
    if request.method == "POST":
        username = request.session.get('username')
        password = request.session.get('password')
        email = request.POST.get('email')
        request.session['email'] = email
        confirmation_code = ''.join(random.choices(string.digits, k=7))
        request.session['confirmation_code'] = confirmation_code
        subject = 'ยืนยันอีเมลของคุณ ',email
        message = f'โปรดใช้รหัสนี้เพื่อยืนยันอีเมลของคุณ: {confirmation_code} ชื่อผู้ใช้ {username}  รหัสผ่าน {password}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return redirect('confirm_otp')

    return render(request,'student/confirm_email.html')

def confirm_email(request):
    if request.method == "POST":
        passemail = request.POST.get('passemail')
        username = request.session.get('username')
        password = request.session.get('password')
        confirmation_code = request.session.get('confirmation_code')
        email = request.session.get('email')
        
        if username is not None and password is not None:
            try:
                temporary_user = TemporaryUser.objects.get(citizen_id=username, password=password)
                if temporary_user is not None:
                    if str(passemail) == str(confirmation_code):
                        # ตรวจสอบว่า email นี้ถูกใช้งานแล้วหรือไม่
                        if User.objects.filter(email=email).exists():
                            return HttpResponse("อีเมลถูกใช้งานไปแล้ว")
                        else:
                            user, created = User.objects.get_or_create(username=username)
                            if created:
                                # กำหนดรหัสผ่านโดยตรง
                                user.set_password(password)
                                user.email = email
                                user.phone_number = temporary_user.phone_number
                                user.first_name = temporary_user.first_name
                                user.last_name = temporary_user.last_name
                                user.birth_date = temporary_user.birth_date
                                user.citizen_id = temporary_user.citizen_id
                                user.save()
                                return redirect('changepassword')
                            else:
                                return redirect('confirm_email')
                    else:
                        return redirect('confirm_email')
                else:
                    return redirect('confirm_email')
            except TemporaryUser.DoesNotExist:
                return redirect('confirm_email')
        else:
            return redirect('confirm_email')
    
    return render(request,'student/confirm_email.html')

def changepassword(request):
    if request.method == "POST":
        password_old = request.POST.get('password_old')
        password_new1 = request.POST.get('password_new1')
        password_new2 = request.POST.get('password_new2')
        username = request.session.get('username')
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return HttpResponse("หาผู้ใช้ไม่เจอ กรุณาล็อกอินด้วยรหัสผ่านเก่าเข้าสู่ระบบได้เลย")

        if user.check_password(password_old):
            if password_new1 == password_new2:
                user.set_password(password_new1)
                user.save()
                return redirect('index')
            else:
                return HttpResponse("รหัสผ่านใหม่ไม่ตรงกัน")
        else:
            return HttpResponse("รหัสผ่านเก่าผิด")

    return render(request, 'student/changepassword.html')

def log_in(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'roles'):
                # ตรวจสอบ Role ของผู้ใช้ที่ล็อกอิน
                if user.roles.filter(name='Admin').exists():
                    return redirect('Admin_page')
                elif user.roles.filter(name='Manager').exists():
                    return redirect('Manager_page')         
                elif user.roles.filter(name='Interviewer').exists():
                    return redirect('Interviewer_page') 
                elif user.roles.filter(name='Student').exists():
                    return redirect('Student_page')      
                else :
                    return redirect('index')
            else:
                return redirect('index')
        else:
            # กรณีที่ไม่สามารถล็อกอินได้ คุณอาจจะจัดการผลลัพธ์ที่ต้องการที่นี่
            return render(request, 'html/index.html')
    return render(request, 'html/index.html')

def log_out(request):
    # sign user out
    logout(request)

    # Redirect to sign-in page
    return redirect('log_in')


def first_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            temporary_user = TemporaryUser.objects.get(citizen_id=username,password=password)
            if temporary_user is not None:
                request.session['username'] = username
                request.session['password'] = password
                return redirect('confirm_email')
        except TemporaryUser.DoesNotExist:
            pass

    return render(request, 'html/first_login.html')

@login_required
@user_passes_test(is_admin)
def add_Faculty(request):
    if request.method == "POST":
        add_Faculty = request.POST.get('faculty')
        if add_Faculty:
            try:
                faculty_exists = Faculty.objects.get(faculty=add_Faculty)
                return redirect("FacultyMajor")
            except Faculty.DoesNotExist:
                new_faculty = Faculty(faculty=add_Faculty)
                new_faculty.save()
                return redirect("FacultyMajor")
        else:
            return redirect("FacultyMajor")

@login_required
@user_passes_test(is_admin)
def delete_Faculty(request,id):
    object = Faculty.objects.get(pk=id)
    object.delete()
    return redirect("FacultyMajor")

@login_required
@user_passes_test(is_admin)
def add_Major(request):
    if request.method == "POST":
        
        add_Major = request.POST.get('Major')
        faculty_id = request.POST.get('faculty_id')
        faculty = get_object_or_404(Faculty, pk=int(faculty_id))
        
        if add_Major:
            try:
                Major_exists = Major.objects.get(major=add_Major, faculty=faculty)
                return redirect("FacultyMajor")
            except Major.DoesNotExist:
                new_Major = Major(major=add_Major, faculty=faculty)
                new_Major.save()
                return redirect("FacultyMajor")
        else:
            return redirect("FacultyMajor")

@login_required
@user_passes_test(is_admin)
def delete_Major(request,id):
    object = Major.objects.get(pk=id)
    object.delete()
    return redirect("FacultyMajor")

@login_required
@user_passes_test(is_admin)
def add_TemporaryUser(request):
    if request.method == "POST":     
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
        birth_date = request.POST.get('birth_date')
        faculty_name = request.POST.get('faculty')  
        major_name = request.POST.get('major')  
        checkboxgroup = request.POST.getlist('checkboxgroup')
        faculty, _ = Faculty.objects.get_or_create(faculty=faculty_name)
        major, _ = Major.objects.get_or_create(major=major_name, faculty=faculty)
        temporary_user, _ = TemporaryUser.objects.get_or_create(citizen_id=citizen_id,
            defaults={
                        'first_name': first_name,
                        'last_name': last_name,
                        'birth_date': birth_date,
                        })
        faculty.TemporaryUser.add(temporary_user)
        major.TemporaryUser.add(temporary_user)
        for role_name in checkboxgroup:
            role_model, _ = Role.objects.get_or_create(name=role_name)
            role_model.TemporaryUser.add(temporary_user)

        temporary_user.save()
            
        return redirect("TemporaryUser")
    
@login_required
@user_passes_test(is_admin)    
def delete_TemporaryUser(request,id):
    object = TemporaryUser.objects.get(pk=id)
    object.delete()
    return redirect("TemporaryUser")

@login_required
@user_passes_test(is_admin)
def add_InterviewRound(request):
    if request.method == "POST":     
        major_name = request.POST.get('major')
        academic_year = request.POST.get('academic_year')
        round_name = request.POST.get('round_name')
        manager_name = request.POST.get('manager_name')
        major = Major.objects.get(major=major_name)

        r_mn = Role.objects.get(name="Manager")
        manager = r_mn.users.get(first_name=manager_name)
        interview_round, _ = Round.objects.get_or_create(major=major,
                                                         academic_year=academic_year,
                                                         round_name=round_name,
                                                         manager=manager)
        interview_round.save()
            
    return redirect("Interview")
    
@login_required
@user_passes_test(is_admin)
def delete_InterviewRound(request,id):
    object = Round.objects.get(pk=id)
    object.delete()
    return redirect("Interview")