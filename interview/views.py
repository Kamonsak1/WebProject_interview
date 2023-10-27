from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render  
from django.urls import reverse
from interview.models import *
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from social_core.backends.google import GoogleOAuth2
from allauth.socialaccount.models import SocialAccount
import random
import string
from django.core.mail import send_mail
# Create your views here.
def index(request):
    return render(request,"html/index.html")

def test(request):
    return render(request,"html/test.html")

#Admin_path
@login_required
def admin_page(request):
    return render(request,'admin/Admin_page.html')
@login_required
def Announcement(request):
    return render(request,'admin/Announcement.html')
@login_required
def FacultyMajor(request):
    return render(request,'admin/FacultyMajor.html')
@login_required
def Interview(request):
    return render(request,'admin/Interview.html')
@login_required
def Score(request):
    return render(request,'admin/Score.html')
@login_required
def TemporaryUser_path(request):
    users = TemporaryUser.objects.all()
    return render(request,'admin/TemporaryUser.html', {'users': users})
@login_required
def User_path(request):
    users = User.objects.all()
    return render(request,'admin/User.html', {'users': users})
@login_required
def form_interview(request):
    return render(request,'admin/form_interview.html')
@login_required
def admin_profile(request):
    return render(request,'admin/admin_profile.html')

#Manager
@login_required
def manager_page(request):
    return render(request,'manager/Manager_page.html')
@login_required
def manage_profile(request):
    return render(request,'manager/manage_profile.html')
@login_required
def Manage_personnel(request):
    return render(request,'manager/Manage_personnel.html')
@login_required
def Manager_Announcement(request):
    return render(request,'manager/Manager_Announcement.html')
@login_required
def Manager_interview(request):
    return render(request,'manager/Manager_interview.html')
@login_required
def Manager_Score(request):
    return render(request,'manager/Manager_Score.html')
@login_required
def Manager_Print_Interview(request):
    return render(request,'manager/Manager_Print_Interview.html')
@login_required
def Manager_Status(request):
    return render(request,'manager/Manager_Status.html')

#Interviewer
@login_required
def interviewer_page(request):
    return render(request,'interviewer/Interviewer_page.html')
@login_required
def Interviewer_Profile(request):
    return render(request,'interviewer/Interviewer_Profile.html')
@login_required
def Interviewer_room(request):
    return render(request,'interviewer/Interviewer_room.html')





#Student
@login_required
def student_page(request):
    return render(request,'student/Student_page.html')
@login_required
def Student_profile(request):
    return render(request,'student/Student_profile.html')
@login_required
def Student_register(request):
    return render(request,'student/Student_register.html')
@login_required
def Student_room(request):
    return render(request,'student/Student_room.html')
@login_required
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




    