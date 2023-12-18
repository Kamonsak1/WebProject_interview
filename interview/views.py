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
import pandas as pd
import random
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
import string
from django.contrib.auth.hashers import make_password
from datetime import datetime
from django.http import JsonResponse
from django.core.mail import send_mail
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.hashers import check_password
from collections import defaultdict
import re
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
    user = User.objects.get(username='1')
    rounds_participated = user.rounds_participated.all()
    majors_participated = [round_obj.major for round_obj in rounds_participated]
    return render(request,"html/test.html",{'user':user,'rounds_participated':rounds_participated,'majors_participated':majors_participated})

#Admin_path
@login_required
@user_passes_test(is_admin)
def admin_page(request):
    Announcement_all = Announcement.objects.filter(role__name='Admin')
    return render(request,'admin/Admin_page.html',{'am':Announcement_all})
@login_required
@user_passes_test(is_admin)
def Announcement_page(request):
    Announcement_all= Announcement.objects.all()
    round = Round.objects.all()
    return render(request,'admin/Announcement.html',{'a':Announcement_all,'round':round})
@login_required
@user_passes_test(is_admin)
def FacultyMajor(request):
    faculty_all = Faculty.objects.all()
    users = User.objects.filter(roles__name='Manager')

    return render(request,'admin/FacultyMajor.html',{"faculty":faculty_all,'users':users})
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
    score_topics = ScoreTopic.objects.all()
    grouped_topics = defaultdict(list)
    for topic in score_topics:
        if re.match('^\d+$', topic.pattern_id):
            grouped_topics[topic.pattern_id].append(topic)

    sorted_grouped_topics = dict(sorted(grouped_topics.items()))

    context = {
        'grouped_topics': sorted_grouped_topics,
    }
    return render(request, 'admin/Score.html', context)
@login_required
@user_passes_test(is_admin)
def TemporaryUser_path(request):
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.all()
    major_all = Major.objects.all()
    round_active = Round.objects.filter(active='True')

    return render(request,'admin/TemporaryUser.html', {'users': users,'faculty_all':faculty_all,"major_all":major_all,'round_active':round_active})
@login_required
@user_passes_test(is_admin)
def User_path(request):
    users = User.objects.all()
    faculty_all = Faculty.objects.all()
    major_all = Major.objects.all()
    round_active = Round.objects.filter(active='True')
    return render(request,'admin/User.html', {'users': users,'faculty_all':faculty_all,"major_all":major_all,'round_active':round_active})

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
def manager_page(request,id):
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.filter(users=id)
    majors = Major.objects.filter(default_manager=id)
    request.session['myuser_id'] = id
    major_from_session = request.session.get('major')
    if  major_from_session:
        


        return render(request,'manager/Manager_page.html',{'users': users,"s_major":major_from_session,'faculty_all':faculty_all,'majors':majors})
    return render(request,'manager/Manager_page.html',{'users': users,'faculty_all':faculty_all,'majors':majors})
@login_required
@user_passes_test(is_Manager)
def manage_profile(request):
    return render(request,'manager/manage_profile.html')
@login_required
@user_passes_test(is_Manager)
def Manage_personnel(request):
    myuser_id = request.session.get('myuser_id')
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    if  major_from_session:
        users = User.objects.filter(roles__name='Manager')
        return render(request,'manager/Manage_personnel.html',{'users': users,"s_major":major_from_session,'faculty_all':faculty_all,'majors':majors})
    return render(request,'manager/Manage_personnel.html',{'users': users,'faculty_all':faculty_all,'majors':majors})

@login_required
@user_passes_test(is_Manager)
def Manage_User(request):
    myuser_id = request.session.get('myuser_id')
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    if  major_from_session:
        users = User.objects.filter(roles__name='Student',major__major=major_from_session)
        return render(request,'manager/Manage_User.html',{'users': users,"s_major":major_from_session,'faculty_all':faculty_all,'majors':majors})
    return render(request,'manager/Manage_User.html',{'users': users,'faculty_all':faculty_all,'majors':majors,})

@login_required
@user_passes_test(is_Manager)
def Manager_Announcement(request):
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.all()
    faculty_from_session = request.session.get('faculty')
    major_from_session = request.session.get('major')
    if faculty_from_session  and  major_from_session:


        return render(request,'manager/Manager_Announcement.html',{'users': users,'s_faculty':faculty_from_session,"s_major":major_from_session,'faculty_all':faculty_all})
    return render(request,'manager/Manager_Announcement.html',{'users': users,'faculty_all':faculty_all})
@login_required
@user_passes_test(is_Manager)
def Manager_interview(request):
    user_rounds = Round.objects.filter(manager=request.user)

    return render(request,'manager/Manager_interview.html',{'rounds': user_rounds})
@login_required
@user_passes_test(is_Manager)
def Manager_Score(request):
    user_rounds = Round.objects.filter(manager=request.user)
    return render(request,'manager/Manager_Score.html',{'rounds': user_rounds})
@login_required
@user_passes_test(is_Manager)
def Manager_Print_Interview(request):
    return render(request,'manager/Manager_Print_Interview.html')
@login_required
@user_passes_test(is_Manager)
def Manager_Status(request):
    user_rounds = Round.objects.filter(manager=request.user)
    return render(request,'manager/Manager_Status.html', {'rounds': user_rounds})

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
    user_rounds = Round.objects.filter(users=request.user)
    user_majors = Major.objects.filter(users=request.user)
    related_rounds = Round.objects.filter(major__in=user_majors)
    combined_rounds = user_rounds | related_rounds
    registered_rounds = InterviewStatus.objects.filter(user=request.user).values_list('round', flat=True)

    return render(request,'student/Student_register.html',{'rounds': combined_rounds.distinct(),'registered_rounds': registered_rounds})
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
        temporary_user_id = request.session.get('temporary_user_id')

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
                            tem_user = TemporaryUser.objects.get(pk=temporary_user_id)
                            #faculty_TemporaryUser = list(temporary_user.faculty_set.all())
                            #major_TemporaryUser = list(temporary_user.major_set.all())
                            if created:
                                # กำหนดรหัสผ่านโดยตรง
                                user.set_password(password)
                                user.email = email
                                user.first_name = temporary_user.first_name
                                user.last_name = temporary_user.last_name
                                user.birth_date = temporary_user.birth_date
                                user.citizen_id = temporary_user.citizen_id
                                role_model = Role.objects.get(name='Student')
                                role_model.users.add(user)
                                round_names = []
                                major_names = []
                                faculty_names=[]
                                for round_obj in tem_user.rounds_participated.all():
                                    round_names.append(round_obj.round_name)
                                    major_names.append(round_obj.major.major)  
                                    faculty_names.append(round_obj.major.faculty.faculty)                                  
                                    round_obj.users.add(user)
                                for major_name in major_names:
                                    major_instance = Major.objects.get(major=major_name)
                                    major_instance.users.add(user)
                                for faculty_name in faculty_names:
                                    faculty_instance = Faculty.objects.get(faculty=faculty_name)
                                    faculty_instance.users.add(user)
 
                                # for faculty in faculty_TemporaryUser:
                                #     faculty.users.add(user)
                                # for  major in major_TemporaryUser:
                                #      major.users.add(user)
                                user.save()
                                return redirect('social:begin', backend='google-oauth2')
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
                request.session['temporary_user_id'] = temporary_user.id
    
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
        birth_date_str = request.POST.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date() 
        round_sel = request.POST.get('round') 
        round = Round.objects.get(pk=round_sel)

        try:
            check_user = User.objects.get(citizen_id=citizen_id)
            return redirect('TemporaryUser') 
        except User.DoesNotExist:
            pass

        try:
            check_temporary_user = TemporaryUser.objects.get(citizen_id=citizen_id)
            round.TemporaryUser.add(check_temporary_user)
            faculty_instance = Faculty.objects.get(faculty=round.major.faculty.faculty)
            faculty_instance.TemporaryUser.add(check_temporary_user)
            major_instance = Major.objects.get(major=round.major.major)
            major_instance.TemporaryUser.add(check_temporary_user)
            return redirect('TemporaryUser') 
        except TemporaryUser.DoesNotExist:
            check_temporary_user = TemporaryUser.objects.create(
                citizen_id=citizen_id,
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
            )
            round.TemporaryUser.add(check_temporary_user)
            role_model, _ = Role.objects.get_or_create(name='Student')
            role_model.TemporaryUser.add(check_temporary_user)
            faculty_instance = Faculty.objects.get(faculty=round.major.faculty.faculty)
            faculty_instance.TemporaryUser.add(check_temporary_user)
            major_instance = Major.objects.get(major=round.major.major)
            major_instance.TemporaryUser.add(check_temporary_user)
            check_temporary_user.save()
            
            return redirect('TemporaryUser')    
            
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

@login_required
@user_passes_test(is_admin)
def add_ScoreTopic(request):
    if request.method == "POST":
        round_value = request.POST.get("round")
        if round_value:
            template_num = request.POST.get('template_num')
            topic_name = request.POST.get('topic_name')
            max_score = request.POST.get('max_score')
            score_detail = request.POST.get('score_detail')
            score_topic, _ = ScoreTopic.objects.get_or_create( pattern_id=template_num,
                                                                topic_name=topic_name,
                                                                max_score=max_score,
                                                                score_detail=score_detail)
            score_topic.save()
            round = Round.objects.get(id=round_value)
            Score_Round = RoundScore(topic=score_topic,Round=round)
            Score_Round.save()
            return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
        else:
            template_num = request.POST.get('template_num')
            topic_name = request.POST.get('topic_name')
            max_score = request.POST.get('max_score')
            score_detail = request.POST.get('score_detail')
            score_topic, _ = ScoreTopic.objects.get_or_create( pattern_id=template_num,
                                                                topic_name=topic_name,
                                                                max_score=max_score,
                                                                score_detail=score_detail)
            score_topic.save()
            return redirect(f"/Score")

@login_required
@user_passes_test(is_admin)
def View_ScoreTopic(request,id):
    Topics = ScoreTopic.objects.filter(pattern_id=id)
    context = {
        "Topics" : Topics
    }
            
    return render(request , 'admin/Score_Template.html', context)

@login_required
@user_passes_test(is_admin)
def delete_ScoreTopic(request,id):
    object = ScoreTopic.objects.get(pk=id)
    pattern = object.pattern_id
    object.delete()
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
@user_passes_test(is_admin)
def edit_TemporaryUser(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
        birth_date_str = request.POST.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        checkboxgroup = request.POST.getlist('checkboxgroup')
        tem_user = TemporaryUser.objects.get(pk=user_id)
        role = Role.objects.filter(TemporaryUser=tem_user)
        for role in role:
            role.TemporaryUser.remove(tem_user)
        tem_user.first_name=first_name
        tem_user.last_name=last_name
        tem_user.citizen_id=citizen_id
        tem_user.birth_date=birth_date
        for role_name in checkboxgroup:
            role_model, _ = Role.objects.get_or_create(name=role_name)
            role_model.TemporaryUser.add(tem_user)
        tem_user.save()
        
    return redirect('TemporaryUser')

@login_required
@user_passes_test(is_admin)
def edit_ScoreTopic(request):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        topic = request.POST.get('topic_name')
        max_score = request.POST.get('max_score')
        detail = request.POST.get('score_detail')
        score_topic = ScoreTopic.objects.get(pk=topic_id)
        score_topic.topic_name=topic
        score_topic.max_score=max_score
        score_topic.score_detail=detail
        score_topic.save()
        
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
@user_passes_test(is_admin)
def edit_InterviewRound(request):
    if request.method == "POST":
        id = request.POST.get('round_id')
        name = request.POST.get('round_name')
        year = request.POST.get('academic_year')
        docs = request.POST.get('documets')
        time = request.POST.get('interview_time')
        major_name = request.POST.get('major')
        manager_name = request.POST.get('manager_name')
        major = Major.objects.get(major=major_name)

        r_mn = Role.objects.get(name="Manager")
        manager = r_mn.users.get(first_name=manager_name)
        round_edited = Round.objects.get(pk=id)
        round_edited.najor=major
        round_edited.academic_year=year
        round_edited.round_name=name
        round_edited.manager=manager
        round_edited.documents=docs
        round_edited.interview_time=time
        round_edited.save()
        
    return redirect('/Interview')

@login_required
@user_passes_test(is_admin)
def add_TemporaryUser_by_file(request):
    if request.method == 'POST':
        data = request.FILES.get('fileInputa')
        if data.name.endswith('.xlsx'):
            df = pd.read_excel(data)
        elif data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            pass
        try:
            data = df[['เลขบัตรประชาชน','ชื่อ','วว/ดด/ปป','รอบที่สมัคร']]
        except Exception as e:
            return HttpResponse('คอลัมไม่ตรงตามที่ต้องการ')
        try:
            data['คำนำหน้า'] = data['ชื่อ'].str.extract(r'(นาย|นางสาว)')
        except Exception as e:
            return HttpResponse('ชื่อไม่ถูกต้อง')
        try:
            data['นามสกุล'] = data['ชื่อ'].str.split(expand=True)[1]
        except Exception as e:
            return HttpResponse('นามสกุลไม่ถูกต้อง')
        try:
            data['first_name'] = data['ชื่อ'].str.split(expand=True)[0]
        except Exception as e:
            return HttpResponse('first_name ไม่ถูกต้อง')
        



        user_old = []
        TemporaryUser_old = []
        
        for i in range(len(data)):
            try:
                citizen_id = str(data.iloc[i]['เลขบัตรประชาชน']).strip()
            except Exception as e:
                citizen_id = str(data.iloc[i]['เลขบัตรประชาชน']).strip()
                return HttpResponse('เลขบัตรประชาชนไม่ถูกต้อง',citizen_id)
            try:
                first_name=(data.iloc[i]['first_name'].strip())
            except Exception as e:
                return HttpResponse('first_name ไม่ถูกต้อง')
            try:
                round=(data.iloc[i]['รอบที่สมัคร'].strip())
            except Exception as e:
                return HttpResponse('round ไม่ถูกต้อง')
            try:
                last_name=(data.iloc[i]['นามสกุล'].strip())
            except Exception as e:
                return HttpResponse('last_name ไม่ถูกต้อง')
            try:
                birth_date_str=(data.iloc[i]['วว/ดด/ปป'].strip())
                birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
            except Exception as e:
                return HttpResponse('วว/ดด/ปป ไม่ถูกต้อง')           
            checkuser = User.objects.filter(citizen_id=citizen_id)
            if not checkuser.exists():
                checkTemporaryUser = TemporaryUser.objects.filter(citizen_id=citizen_id)
                
                if not checkTemporaryUser.exists():
                    Temporary_User = TemporaryUser.objects.create(citizen_id=citizen_id,first_name=first_name,last_name=last_name,birth_date=birth_date)
                    role=Role.objects.filter(name='Student').first()
                    role.TemporaryUser.add(Temporary_User)
                    Round_db = Round.objects.filter(round_name=round).first()
                    Round_db.TemporaryUser.add(Temporary_User)  
                    faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                    faculty_instance.TemporaryUser.add(Temporary_User)
                    major_instance = Major.objects.get(major=Round_db.major.major)
                    major_instance.TemporaryUser.add(Temporary_User) 
                    
                else:
                    TemporaryUser_old.append(data.iloc[i]['ชื่อ'])
                    user_id = checkTemporaryUser.first().id
                    checkRound = Round.objects.filter(round_name=round,TemporaryUser=user_id)
                    if not checkRound.exists():
                        Round_db = Round.objects.filter(round_name=round).first()
                        Round_db.TemporaryUser.add(user_id)  
                        faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                        faculty_instance.TemporaryUser.add(Temporary_User)
                        major_instance = Major.objects.get(major=Round_db.major.major)
                        major_instance.TemporaryUser.add(Temporary_User)                   
                    else:
                        pass
                        #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')
            else:
                user_old.append(data.iloc[i]['ชื่อ'])
                user_id = checkuser.first().id
                checkRound = Round.objects.filter(round_name=round,users=user_id)
                if not checkRound.exists():
                    Round_db = Round.objects.filter(round_name=round).first()
                    Round_db.users.add(user_id)
                    faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                    faculty_instance.users.add(Temporary_User)
                    major_instance = Major.objects.get(major=Round_db.major.major)
                    major_instance.users.add(Temporary_User)                     
                else:
                    pass
                    #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')

        print('เจอข้อมูลเดิม',user_old)
        print('เจอข้อมูลเดิม',TemporaryUser_old)
    return redirect('TemporaryUser')

@login_required
@user_passes_test(is_admin)
def delete_User(request,id):
    
    user_del = User.objects.get(pk=id)
    user_del.delete()
    return redirect('User')

def delete_User_in_manager(request,id):
    user_del = User.objects.get(pk=id)
    user_del.delete()
    return redirect('Manage_User')

@login_required
@user_passes_test(is_admin)
def add_User(request):
    if request.method == "POST":     
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
        email =  request.POST.get('email')
        #birth_date_str = request.POST.get('birth_date')
        #birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        faculty_name = request.POST.get('faculty')  
        major_name = request.POST.get('major')  
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        checkboxgroup = request.POST.getlist('checkboxgroup')
        faculty = Faculty.objects.get(faculty=faculty_name)
        major= Major.objects.get(major=major_name, faculty=faculty)
        try:
            check_user = User.objects.get(email=email)
            faculty.users.add(check_user)
            major.users.add(check_user)
            return redirect('User')
        except User.DoesNotExist:
            new_user = User.objects.create(
                                           first_name= first_name,
                                           last_name= last_name,
                                           email= email ,
                                           username=email,
                                           password= make_password(password))
            faculty.users.add(new_user)
            major.users.add(new_user)
            faculty.users.add(new_user)
            major.users.add(new_user)
            for role_name in checkboxgroup:
                role_model, _ = Role.objects.get_or_create(name=role_name)
                role_model.users.add(new_user)
            send_registration_email(email)
            return redirect('User')
        
    return redirect("User")

def send_registration_email(email):
    subject = 'รหัสผ่านของเว็บจัดคิวสัมภาษณ์',email
    message = f'สามารถเข้าสู่ระบบทาง google ด้วย email: {email}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
@login_required
@user_passes_test(is_admin)
def add_User_by_file(request):
    if request.method == 'POST':
        data = request.FILES.get('fileInputa')
        checkboxgroup = request.POST.getlist('checkboxgroup')
        if data.name.endswith('.xlsx'):
            df = pd.read_excel(data)
        elif data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            pass
        try:
            data = df[['ชื่อ','คณะ','สาขา','email']]
        except Exception as e:
            return HttpResponse('คอลัมไม่ตรงตามที่ต้องการ')
        try:
            data['คำนำหน้า'] = data['ชื่อ'].str.extract(r'(นาย|นางสาว)')
        except Exception as e:
            return HttpResponse('ชื่อไม่ถูกต้อง')
        try:
            data['นามสกุล'] = data['ชื่อ'].str.split(expand=True)[1]
        except Exception as e:
            return HttpResponse('นามสกุลไม่ถูกต้อง')
        try:
            data['first_name'] = data['ชื่อ'].str.split(expand=True)[0]
        except Exception as e:
            return HttpResponse('first_name ไม่ถูกต้อง')
        



        user_old = []
        
        for i in range(len(data)):
            try:
                faculty = (data.iloc[i]['คณะ'].strip())
            except Exception as e:
                return HttpResponse('ชื่อคณะไม่ถูกต้อง')
            try:
                major = (data.iloc[i]['สาขา'].strip())
            except Exception as e:
                return HttpResponse('ชื่อสาขาไม่ถูกต้อง')
            try:
                first_name=(data.iloc[i]['first_name'].strip())
            except Exception as e:
                return HttpResponse('first_name ไม่ถูกต้อง')
            try:
                last_name=(data.iloc[i]['นามสกุล'].strip())
            except Exception as e:
                return HttpResponse('last_name ไม่ถูกต้อง')
            try:
                email=(data.iloc[i]['email'].strip())
            except Exception as e:
                return HttpResponse('email ไม่ถูกต้อง') 
                    
            checkuser = User.objects.filter(email=email)
            if not checkuser.exists():
                #password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
                create_User = User.objects.create(first_name=first_name,last_name=last_name,email=email)
                create_User.username = email
                create_User.save()
                #send_registration_email(email)
                Faculty_add = Faculty.objects.filter(faculty=faculty).first()
                Faculty_add.users.add(create_User)
                Major_add = Major.objects.filter(major=major).first()
                Major_add.users.add(create_User)
                for role_name in checkboxgroup:
                    role_model, _ = Role.objects.get_or_create(name=role_name)
                    role_model.users.add(create_User)
            else:
                user_old.append(data.iloc[i]['ชื่อ'])
                user_id = checkuser.first().id
                checkFaculty = Faculty.objects.filter(faculty=faculty,users=user_id)
                if not checkFaculty.exists():
                    faculty_db = Faculty.objects.filter(faculty=faculty).first()
                    faculty_db.users.add(user_id)                    
                else:
                    pass
                        #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')
                checkMajor = Major.objects.filter(major=major,users=user_id)
                if not checkMajor.exists():
                    Major_db = Major.objects.filter(major=major).first()
                    Major_db.users.add(user_id)                    
                else:
                    pass


        print('เจอข้อมูลเดิม',user_old)
    return redirect('User')
@login_required
@user_passes_test(is_admin)
def edit_User(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        citizen_id = request.POST.get('citizen_id')
        email = request.POST.get('email')
        birth_date_str = request.POST.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        checkboxgroup = request.POST.getlist('checkboxgroup')
        edit_user = User.objects.get(pk=user_id)
        role = Role.objects.filter(users=edit_user)
        for role in role:
            role.users.remove(edit_user)
        edit_user.first_name=first_name
        edit_user.last_name=last_name
        edit_user.citizen_id=citizen_id
        edit_user.birth_date=birth_date
        edit_user.email=email
        for role_name in checkboxgroup:
            role_model, _ = Role.objects.get_or_create(name=role_name)
            role_model.users.add(edit_user)
        edit_user.save()
        
    return redirect('User')


def search_user(request):
    if request.method == "POST":
        search = request.POST.get('search')
        faculty = request.POST.get('faculty')
        major = request.POST.get('major')
        faculty_all = Faculty.objects.all()
        
        users = User.objects.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(faculty__faculty__icontains=search) |
            Q(major__major__icontains=search) )
        if faculty and major:
            users_filtered = User.objects.filter(faculty__faculty=faculty, major__major=major,).filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(email__icontains=search))
            return render(request,'admin/form_search/search.html',{'users': users_filtered,'faculty_all':faculty_all})
        elif faculty:
            users_filtered = User.objects.filter(faculty__faculty=faculty).filter(Q(username__icontains=search) | Q(first_name__icontains=search) | Q(email__icontains=search))
            return render(request,'admin/form_search/search.html',{'users': users_filtered,'faculty_all':faculty_all})
        else: 
            return render(request,'admin/form_search/search.html',{'users': users,'faculty_all':faculty_all})
            

    return HttpResponse("ไม่พบข้อมูล")
    

    
def search_TemporaryUser(request):
    if request.method == "POST":
        search = request.POST.get('search')
        faculty = request.POST.get('faculty')
        major = request.POST.get('major')
        faculty_all = Faculty.objects.all()
        
        users = TemporaryUser.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(citizen_id__icontains=search) |
            Q(faculty__faculty__icontains=search) |
            Q(major__major__icontains=search) )
        if faculty and major:
            users_filtered = TemporaryUser.objects.filter(faculty__faculty=faculty, major__major=major,).filter( Q(first_name__icontains=search)|Q(citizen_id__icontains=search) |Q(last_name__icontains=search)  )
            return render(request,'admin/form_search/search_tem.html',{'users': users_filtered,'faculty_all':faculty_all})
        elif faculty:
            users_filtered = TemporaryUser.objects.filter(faculty__faculty=faculty).filter( Q(first_name__icontains=search)|Q(citizen_id__icontains=search) |Q(last_name__icontains=search)  )
            return render(request,'admin/form_search/search_tem.html',{'users': users_filtered,'faculty_all':faculty_all})

        else: 
            return render(request,'admin/form_search/search_tem.html',{'users': users,'faculty_all':faculty_all})
            

    return HttpResponse("ไม่พบข้อมูล")
    
@login_required
def edit_password_in_profile(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password2 = request.POST.get('new_password2')

        user = User.objects.get(pk=user_id)
        if check_password(old_password, user.password):
            if new_password == new_password2:
                user.set_password(new_password)
                user.save()
            else:
                return HttpResponse('รหัสผ่านใหม่ไม่เหมือนกัน')
        else:
            return HttpResponse('รหัสยืนยันไม่ถูกต้อง')


        #update_session_auth_hash(request, user)  

    return redirect('index')
    
    #return render(request,'admin/admin_profile.html')

@login_required
@user_passes_test(is_admin)
def ajax_load_cities(request):
    faculty_name = request.GET.get('faculty')  
    faculty_object = Faculty.objects.get(faculty=faculty_name)
    majors = faculty_object.major_set.all()
    return render(request, 'admin/dropdown-list.html', {"majors": majors})
def ajax_load_major(request):
    #faculty_name = request.GET.get('faculty')  
    #faculty_object = Faculty.objects.get(faculty=faculty_name)
    myuser_id = request.session.get('myuser_id')
    majors = Major.objects.filter(default_manager=myuser_id)
    return render(request, 'admin/dropdown-list.html', {"majors": majors})

@login_required
@user_passes_test(is_Manager)
def toggle_round_active(request, round_id):
    round = get_object_or_404(Round, id=round_id)
    round.active = not round.active
    round.save()
    return redirect('/Manager_interview')


@login_required
@user_passes_test(is_Student)
def register_interview(request, round_id):
    round = get_object_or_404(Round, id=round_id)
    # สร้างหรืออัปเดต InterviewStatus
    InterviewStatus.objects.update_or_create(
        user=request.user, round=round,
        defaults={'status': 'พร้อมสอบ'}
    )
    return redirect('/Student_register')

def add_Major_manager(request):
    if request.method =='POST':
        major_id = request.POST.get('major_id')
        user_id = request.POST.get('user_id')
        serach_major = Major.objects.get(pk=major_id)
        serach_major.default_manager.add(user_id)
        return redirect('FacultyMajor')
    
def delete_manage_in_major(request):
    if request.method =='POST':
        major_id = request.POST.get('major_id')
        user_id = request.POST.get('manager_id')
        serach_major = Major.objects.get(pk=major_id)
        serach_major.default_manager.remove(user_id)
        return redirect('FacultyMajor')
    
def chang_major(request):
    myuser_id = request.session.get('myuser_id')
    if request.method =="POST":
        ma = request.POST.get('major')
        request.session['major'] = ma
        return redirect('Manager_page',id=myuser_id)
    
    return render(request, 'manager/Manager_page.html')

def ajax_searchText(request):
    if request.method == 'POST':
        inputText = request.POST.get('query')
        users = User.objects.filter(Q(first_name__icontains=inputText))
        return render(request, 'admin/form_search/searchinputtext.html', {"listusers": users})

@login_required
@user_passes_test(is_Interviewer)
def add_meetlink(request):
    if request.method == "POST":
        link = request.POST.get("link")
        user = request.user
        if InterviewLink(user=user):
            change_link = InterviewLink.objects.get(user=user)
            change_link.link = link
            change_link.save()
        else:
            add_link = InterviewLink(user=user,link=link)
            add_link.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

    return redirect('/Interviewer_page')


@login_required
@user_passes_test(is_Manager)
def Manager_ScoreTopic(request,id):
    round = Round.objects.get(id=id)
    if request.method == "POST":
        pattern_id = request.POST.get("pattern")
        pattern_name = request.POST.get("round_name")

        Topic_in_Pattern = ScoreTopic.objects.filter(pattern_id=pattern_id)
        for t in Topic_in_Pattern:
            new_topic = ScoreTopic(pattern_id=pattern_name,topic_name=t.topic_name,max_score=t.max_score,score_detail=t.score_detail)
            new_topic.save()
            round_score = RoundScore(topic=new_topic,Round=round)
            round_score.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    if RoundScore.objects.filter(Round=round):
        text = True
    else:
        text = False

    round_name = f"{round.round_name}_{round.academic_year}_{round.major.major}"
    round_id = round.id
    score_topics = ScoreTopic.objects.all()
    grouped_topics = defaultdict(list)
    for topic in score_topics:
        if re.match('^\d+$', topic.pattern_id):
            grouped_topics[topic.pattern_id].append(topic)

    topics = dict(sorted(grouped_topics.items()))

    template = ScoreTopic.objects.filter(pattern_id=round_name)
    context = {
        "text" : text,
        "no_topic" : topics,
        "round" : round_name,
        "round_id" : round,
        "topics" : template,
    }
    
    return render(request,"manager/Manager_ScoreTopic.html",context)


def profile_changname(request):
    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        source_page = request.POST.get('page')
        user = User.objects.get(pk=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')
        


def profile_send_otp(request):
    if request.method == 'POST':
        email_profile = request.POST.get('email')
        confirmation_code_profile = ''.join(random.choices(string.digits, k=7))
        source_page = request.POST.get('page')
        request.session['confirmation_code_profile'] = confirmation_code_profile
        request.session['email_profile'] = email_profile
        subject = 'ยืนยันอีเมลของคุณ ',email_profile
        message = f'โปรดใช้รหัสนี้เพื่อยืนยันอีเมลของคุณ: {confirmation_code_profile} '
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email_profile]
        send_mail(subject, message, from_email, recipient_list)
        if source_page == 'Admin':
            return render(request, 'admin/admin_profile.html', {'email': email_profile})
        if source_page == 'Manager':
            return render(request, 'manager/manage_profile.html', {'email': email_profile})
        if source_page == 'Interviewer':
            return render(request, 'interviewer/Interviewer_Profile.html', {'email': email_profile})
        if source_page == 'Student':
            return render(request, 'student/Student_profile.html', {'email': email_profile})
        

def profile_changemail(request):
    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        email = request.POST.get('email')
        confirmemail  = request.POST.get('confirmemail')
        otp = request.session.get('confirmation_code_profile')
        source_page = request.POST.get('page')
        if  confirmemail ==  otp:
            user = User.objects.get(pk=user_id)
            user.email = email
            user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')
        
def profile_changecitizen_id(request):
    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        citizen_id = request.POST.get('citizen_id')
        source_page = request.POST.get('page')
        user = User.objects.get(pk=user_id)
        user.citizen_id = citizen_id
        user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')
        
def profile_changephone_number(request):
    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        phone_number = request.POST.get('phone_number')
        source_page = request.POST.get('page')
        user = User.objects.get(pk=user_id)
        user.phone_number = phone_number
        user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')

def profile_changeaddress(request):

    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        source_page = request.POST.get('page')
        user = User.objects.get(pk=user_id)
        user.address = address
        user.postcode = postcode
        user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')
        
def profile_hbd(request):
    if request.method == 'POST':
        user_id   = request.POST.get('user_id')
        birth_date_str = request.POST.get('birth_date')
        birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        source_page = request.POST.get('page')
        user = User.objects.get(pk=user_id)
        user.birth_date = birth_date
        user.save()
        if source_page == 'Admin':
            return redirect('admin_profile')
        if source_page == 'Manager':
            return redirect('manage_profile')
        if source_page == 'Interviewer':
            return redirect('Interviewer_Profile')
        if source_page == 'Student':
            return redirect('Student_profile')
        
def add_announcement(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        details = request.POST.get('details')
        date_str = request.POST.get('expire_date')
        date_object = datetime.strptime(date_str, '%d/%m/%Y')
        adjusted_year = date_object.year - 543
        adjusted_date = date_object.replace(year=adjusted_year)
        formatted_date = adjusted_date.strftime('%Y-%m-%d')
        selected_rounds_str = request.POST.get('selectedRounds').split(',')
        checkboxgroup = request.POST.getlist('checkboxgroup')
        add_announcement =Announcement.objects.create(title=topic,announcement_content=details,expire_date=formatted_date)
        for rounds in selected_rounds_str:
            round = Round.objects.get(pk=rounds)
            add_announcement.round.add(round)
        for role in checkboxgroup:
            role = Role.objects.get(name=role)
            add_announcement.role.add(role)
        return redirect('Announcement_page')
    
def delete_Announcement(request,id):
    delete_Am = Announcement.objects.get(pk=id)
    delete_Am.delete()
    return redirect('Announcement_page')

def Manager_StatusRound(request,id):
    round = Round.objects.get(id=id)
    UserInRound = InterviewStatus.objects.filter(round=round)
    context = {
        "Users" : UserInRound,
        "round" : round,
    }
    return render(request, "manager/Manager_StatusRound.html", context)