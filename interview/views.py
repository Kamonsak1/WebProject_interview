from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render  
from django.urls import reverse
import requests
from interview.models import *
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.decorators import login_required,user_passes_test
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import quote
#For Calendar Test
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pickle
import os.path

from social_core.backends.google import GoogleOAuth2
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import get_object_or_404
import pandas as pd
import random
import csv
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q,F
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
from .forms import *
import os
import shutil
import zipfile
from django.http import HttpResponse
from io import BytesIO
# Create your views here.
def google_LOGIN_URL(request):
    roles = set(request.user.roles.values_list('name', flat=True))
    user_id = request.user.id
    user = User.objects.get(pk=user_id)
    user.first_name = user.first_name2
    user.last_name = user.last_name2
    user.save()
    if 'Admin' in roles:
        return redirect('Admin_page')
    elif 'Manager' in roles:
        return redirect('Manager_page', id=user_id)
    elif 'Interviewer' in roles:
        return redirect('Interviewer_room')
    elif 'Student' in roles:
        return redirect('Student_register')
    return  HttpResponse('ไม่มีบทบาท')
    
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
    mode = login_mode.objects.all()
    for i in mode:
        if i.mode == '0':
            return render(request,"html/index.html")
        else:
            return render(request,"html/index2.html")

def test(request):
    user = User.objects.get(username='1')
    rounds_participated = user.rounds_participated.all()
    majors_participated = [round_obj.major for round_obj in rounds_participated]
    return render(request,"admin/test.html",{'user':user,'rounds_participated':rounds_participated,'majors_participated':majors_participated})

#Admin_path
@login_required
@user_passes_test(is_admin)
def admin_page(request):
    Announcement_all = Announcement.objects.filter(role__name='Admin')
    Schedule_all = Schedule.objects.filter(role__name='Admin')
    return render(request,'admin/Admin_page.html',{'Announcement':Announcement_all,'Schedule':Schedule_all})


SCOPES = ['https://www.googleapis.com/auth/calendar']
def get_calendar_service():
    creds = None
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './client_secret_50020983181-gvqbj8kho3jrmpeo81iskq7prpo27gsm.apps.googleusercontent.com.json', SCOPES)
            creds = flow.run_local_server(port=40000)
        with open('token.pkl', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event_with_attendees(start_time_str, end_time_str, summary, attendees, description=None, location=None):
    service = get_calendar_service()

    event = {
        "summary": summary,
        "description": description,
        "location": location,
        "start": {"dateTime": start_time_str, "timeZone": 'Asia/Bangkok'},
        "end": {"dateTime": end_time_str, "timeZone": 'Asia/Bangkok'},
        "attendees": [{"email": attendee} for attendee in attendees],
    }

    event_result = service.events().insert(calendarId='primary', body=event, sendNotifications=True).execute()



@login_required
@user_passes_test(is_admin)
def Announcement_page(request):
    Announcement_all= Announcement.objects.all()
    Schedule_all = Schedule.objects.all()
    round = Round.objects.all()
    if request.method == "POST" and "test_calendar" in request.POST:
        create_event_with_attendees('2024-02-13T09:00:00', '2024-02-13T10:00:00', 'Team Meeting', ['kamonsak.ba.64@ubu.ac.th','ronnapong.pi.64@ubu.ac.th'])
        print("Success!!!!")
    return render(request,'admin/Announcement.html',{'a':Announcement_all,'round':round,'s':Schedule_all})
@login_required
@user_passes_test(is_admin)
def FacultyMajor(request):
    faculty_all = Faculty.objects.all()
    users = User.objects.filter(roles__name='Manager')

    return render(request,'admin/FacultyMajor.html',{"faculty":faculty_all,'users':users})

def report_TemporaryUser(request):
    data_list=report_temporaryUser.objects.all()
    duplicate_register_id = request.session.get('duplicate_register_id', [])
    users_with_duplicates = []
    users_without_duplicates = []
    for user in data_list:
        if user.citizen_id in duplicate_register_id:
            users_with_duplicates.append(user)
        else:
            users_without_duplicates.append(user)
    return render(request,'admin/report_user/report_TemporaryUser.html',{"data_list":users_without_duplicates,"data_duplicates":users_with_duplicates})

@login_required
@user_passes_test(is_admin)
def Interview(request):
    if request.method == "POST" and "add_round_doc" in request.POST:
        if Required_doc.objects.filter(doc_name=request.POST.get("new_doc")):
            new_doc = Required_doc.objects.get(doc_name=request.POST.get("new_doc"))
            round = Round.objects.get(id=int(request.POST.get("add_round_doc")))
            round.documents.add(new_doc)
            redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
        else:
            new_doc = Required_doc(doc_name=request.POST.get("new_doc"))
            new_doc.save()
            round = Round.objects.get(id=int(request.POST.get("add_round_doc")))
            round.documents.add(new_doc)
            redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "remove_round_doc" in request.POST:
        remove_doc = Required_doc.objects.get(doc_name=request.POST.get("remove_doc"))
        round = Round.objects.get(id=int(request.POST.get("remove_round_doc")))
        round.documents.remove(remove_doc)
        redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
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
def Admin_Score(request):
    main_pattern = ScorePattern.objects.filter(main_pattern=True)
    context = {
        'main_pattern': main_pattern,
    }
    return render(request, 'admin/Score.html', context)
@login_required
@user_passes_test(is_admin)
def TemporaryUser_path(request):
    users = TemporaryUser.objects.all()
    faculty_all = Faculty.objects.all()
    major_all = Major.objects.all()
    round_active = Round.objects.all().order_by('-academic_year')
    instances_mode = login_mode.objects.all()
    mode = None
    for i in instances_mode:
        mode = i.mode

    return render(request,'admin/TemporaryUser.html', {'users': users,'faculty_all':faculty_all,"major_all":major_all,'round_active':round_active, 'mode': mode})
@login_required
@user_passes_test(is_admin)
def User_path(request):
    users = User.objects.all()
    faculty_all = Faculty.objects.all()
    major_all = Major.objects.all()
    round_active = Round.objects.filter(active='True')
    return render(request,'admin/User.html', {'users': users,'faculty_all':faculty_all,"major_all":major_all,'round_active':round_active})

@login_required
@user_passes_test(is_admin)
def admin_profile(request):
    return render(request,'admin/admin_profile.html')

#Manager
@login_required
@user_passes_test(is_Manager)
def manager_page(request,id):
    users = User.objects.all()
    faculty_all = Faculty.objects.filter(users=id)
    majors = Major.objects.filter(default_manager=id)
    request.session['myuser_id'] = id
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        Announcement_all = Announcement.objects.filter(role__name='Manager',major__major=major_from_session)
        Schedule_all = Schedule.objects.filter(role__name='Manager',major__major=major_from_session)
        return render(request,'manager/Manager_page.html',{'users': users,"s_major":major_from_session,"s_round":round_from_session,'faculty_all':faculty_all,'majors':majors,'am':Announcement_all,'s':Schedule_all})
    return render(request,'manager/Manager_page.html',{'faculty_all':faculty_all,'majors':majors })
@login_required
@user_passes_test(is_Manager)
def manage_profile(request):
    return render(request,'manager/manage_profile.html')
@login_required
@user_passes_test(is_Manager)
def Manage_personnel(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        users_Manager = User.objects.filter(roles__name='Manager', major__major=major_from_session)
        users_Interviewer = User.objects.filter(roles__name='Interviewer', major__major=major_from_session)
        users_Admin = User.objects.filter(roles__name='Admin', major__major=major_from_session)
        users = users_Manager.union(users_Interviewer)
        users_admin_ids = users_Admin.values_list('id', flat=True)
        users = [user for user in users if user.id not in users_admin_ids]
        context = {
        "s_major" : major_from_session,
        "users" : users,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        }
        return render(request,'manager/Manage_personnel.html',context)
    return render(request,'manager/Manage_personnel.html',{'faculty_all':faculty_all,'majors':majors})

@login_required
@user_passes_test(is_Manager)
def Manage_User(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        users = User.objects.filter(roles__name='Student',major__major=major_from_session,round_user__round_name=round_from_session)
        context = {
        "s_major" : major_from_session,
        "users" : users,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        }
        return render(request,'manager/Manage_User.html',context)
    return render(request,'manager/Manage_User.html',{'faculty_all':faculty_all,'majors':majors,})

@login_required
@user_passes_test(is_Manager)
def Manager_Announcement(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        context = {
        "s_major" : major_from_session,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        }

        return render(request,'manager/Manager_Announcement.html',context)
    return render(request,'manager/Manager_Announcement.html',{'faculty_all':faculty_all,'majors':majors})
@login_required
@user_passes_test(is_Manager)
def Manager_interview(request):
    if request.method == "POST" and "add_round_doc" in request.POST:
        if Required_doc.objects.filter(doc_name=request.POST.get("new_doc")):
            new_doc = Required_doc.objects.get(doc_name=request.POST.get("new_doc"))
            round = Round.objects.get(id=int(request.POST.get("add_round_doc")))
            round.documents.add(new_doc)
            redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
        else:
            new_doc = Required_doc(doc_name=request.POST.get("new_doc"))
            new_doc.save()
            round = Round.objects.get(id=int(request.POST.get("add_round_doc")))
            round.documents.add(new_doc)
            redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "remove_round_doc" in request.POST:
        remove_doc = Required_doc.objects.get(doc_name=request.POST.get("remove_doc"))
        round = Round.objects.get(id=int(request.POST.get("remove_round_doc")))
        round.documents.remove(remove_doc)
        redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        user_rounds = Round.objects.filter(manager=request.user)
        context = {
        "s_major" : major_from_session,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        'rounds': user_rounds
        }
        return render(request,'manager/Manager_interview.html',context)

    return render(request,'manager/Manager_interview.html',{'faculty_all':faculty_all,'majors':majors})
def Manager_data_investigator(request,id):
    round = Round.objects.get(id=id)
    UserInRound = InterviewStatus.objects.filter(round=round).order_by("reg_at")
    context = {
        "Users" : UserInRound,
        "round" : round,
    }
    return render(request,'manager/Manager_data_investigator.html',context)
@login_required
@user_passes_test(is_Manager)
def Manager_Score(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        user_rounds = Round.objects.filter(manager=request.user)
        context = {
        "s_major" : major_from_session,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        'rounds': user_rounds
        }
        return render(request,'manager/Manager_Score.html',context)
    return render(request,'manager/Manager_Score.html',{'faculty_all':faculty_all,'majors':majors})
@login_required
@user_passes_test(is_Manager)
def Manager_Print_Interview(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        student = User.objects.filter(major__major=major_from_session,round_user__round_name=round_from_session,roles__name='Student')

        context = {
        "student":student,
        "s_major" : major_from_session,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        }
        return render(request,'manager/Manager_Print_Interview.html',context)
    return render(request,'manager/Manager_Print_Interview.html',{'faculty_all':faculty_all,'majors':majors})

def form_student(request, id):
    scores = 0
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    topic_list = []
    score_list = []
    topic_all = [ ]
    if  major_from_session and round_from_session:
        student = User.objects.get(pk=id)
        round_score = RoundScore.objects.filter(Round__round_name=round_from_session).select_related('pattern').first()
        scores_topic = ScoreTopic.objects.filter(pattern_id=round_score.pattern)
        student_info = {
            'scores': [], 
            'interviewer':'-'
        }
        for topic in scores_topic:
            topic_scores_all = Score.objects.filter(topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)
            topic_scores = Score.objects.filter(student=student,topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)
            for i in topic_scores_all:
                if i.topic.topic_name not in topic_all:
                    topic_all.append(i.topic.topic_name)

        for topic in scores_topic:      
            topic_scores = Score.objects.filter(student=student,topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)  
            for i in topic_scores:
                topic_list.append(i.topic.topic_name)
                if student_info['interviewer'] == '-':
                    interviewer_name = i.interviewer.prefix+i.interviewer.first_name+' '+i.interviewer.last_name
                    student_info['interviewer'] = interviewer_name
        for item in topic_all:
            if item in topic_list:
                topic_scores = Score.objects.filter(student=student,topic__topic_name=item,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)  
                for i in topic_scores:
                    student_info['scores'].append({'topic_name': item, 'score': i.score,'scores_max': i.topic.max_score})
            else:
                student_info['scores'].append({'topic_name': item, 'score': 0,'scores_max': i.topic.max_score})
        print(student_info)
        context = {
            "student":student,
            'score': student_info,
            'score_list':score_list,
            "s_major" : major_from_session,
            "faculty_all" : faculty_all,
            "majors" : majors,
            "s_round" : round_from_session,
        }
        return render(request, 'manager/form_student/student.html', context)
    return render(request, 'manager/form_student/student.html',{'faculty_all':faculty_all,'majors':majors})
def export_to_csv(request):
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['Column 1', 'Column 2', 'Column 3'])
    writer.writerow(['Data 1', 'Data 2', 'Data 3'])
    return response

@login_required
@user_passes_test(is_Manager)
def Manager_Status(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if  major_from_session and round_from_session:
        user_rounds = Round.objects.filter(manager=request.user)
        context = {
        "s_major" : major_from_session,
        "faculty_all" : faculty_all,
        "majors" : majors,
        "s_round" : round_from_session,
        'rounds': user_rounds
        }
        return render(request,'manager/Manager_Status.html', context)
    return render(request,'manager/Manager_Status.html', {'faculty_all':faculty_all,'majors':majors})

#Interviewer
@login_required
@user_passes_test(is_Interviewer)
def interviewer_page(request):

    Announcement_all = Announcement.objects.filter(role__name='Interviewer')
    Schedule_all = Schedule.objects.filter(role__name='Interviewer')
    return render(request,'interviewer/Interviewer_page.html',{'am':Announcement_all,'s':Schedule_all})
@login_required
@user_passes_test(is_Interviewer)
def Interviewer_Profile(request):
    return render(request,'interviewer/Interviewer_Profile.html')
@login_required
@user_passes_test(is_Interviewer)
def Interviewer_room(request):
    if InterviewLink.objects.filter(user=request.user):
        pass
    else:
        new_link = InterviewLink(user=request.user,link="")
        new_link.save()
    if InterviewNow.objects.filter(interviewer=request.user):
        pass
    else:
        now = InterviewNow(interviewer=request.user)
        now.save()


    user_rounds = Round.objects.filter(users=request.user)
    user_majors = Major.objects.filter(users=request.user)
    related_rounds = Round.objects.filter(major__in=user_majors)
    combined_rounds = (user_rounds | related_rounds).distinct().order_by("-academic_year")

    not_selected_round = True
    link = InterviewLink.objects.get(user=request.user)
    if link.round:
        not_selected_round = False

    if request.method == "POST" and "round" in request.POST:
        r = request.POST.get("round")
        round = Round.objects.get(id=r)
        link = InterviewLink.objects.get(user=request.user)
        link.round = round
        link.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    
    elif request.method == "POST" and "round_exit" in request.POST:
        id = int(request.POST.get("round_exit"))
        round = Round.objects.get(id=link.round.id)
        link = InterviewLink.objects.get(id=id)
        interviewing_now = InterviewNow.objects.filter(interviewer=request.user)
        if interviewing_now:
            now = InterviewNow.objects.filter(interviewer=request.user).first()
            student_status = InterviewStatus.objects.filter(user=now.student,round=round)
            now.student = None
            now.save()
            if student_status:
                status = student_status.first()
                status.status = "พร้อมสอบ"
                status.save()
        link.round = None
        link.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "upload" in request.POST:
        user_id = int(request.POST.get("upload"))
        user = User.objects.get(id=user_id)
        file = request.FILES.get('file_name')
        if Evidence.objects.filter(student=user,round=link.round,interviewer=link.user):
            evidence = Evidence.objects.get(student=user,round=link.round,interviewer=link.user)
            evidence.document = file
            evidence.save()
        else:
            evidence = Evidence(student=user,round=link.round,interviewer=link.user,document=file)
            evidence.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "finish" in request.POST:
        user_id = int(request.POST.get("finish"))
        user = User.objects.get(id=user_id)
        Shortnote = request.POST.get("Shortnote")
        evidence = Evidence.objects.get(student=user,round=link.round,interviewer=link.user)
        evidence.Shortnote = Shortnote
        evidence.save()
        pattern = RoundScore.objects.filter(Round=link.round).first()
        all_scoretopic = ScoreTopic.objects.filter(pattern_id=pattern.pattern)
        for score in all_scoretopic:
            value = request.POST.get("input"+str(score.id))
            print(score,user,link.user,value)
            if value: 
                save_score = Score(topic=score, student=user, interviewer=link.user, score=int(value))
                save_score.save()
        interviewing_now = InterviewNow.objects.get(interviewer=request.user)
        interviewing_now.student = None
        interviewing_now.save()
        round = Round.objects.get(id=link.round.id)
        student_status = InterviewStatus.objects.get(user=user,round=round)
        student_status.status = "สอบเสร็จแล้ว"
        student_status.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "finish_leave" in request.POST:
        
        user_id = int(request.POST.get("finish_leave"))
        Shortnote = request.POST.get("Shortnote")
        user = User.objects.get(id=user_id)
        evidence = Evidence.objects.get(student=user,round=link.round,interviewer=link.user)
        evidence.Shortnote = Shortnote
        evidence.save()
        pattern = RoundScore.objects.filter(Round=link.round).first()
        all_scoretopic = ScoreTopic.objects.filter(pattern_id=pattern.pattern)
        for score in all_scoretopic:
            value = request.POST.get("input"+str(score.id))
            if value: 
                score_point = int(value)
                save_score = Score(topic=score, student=user, interviewer=link.user, score=score_point)
                save_score.save()
        interviewing_now = InterviewNow.objects.get(interviewer=request.user)
        interviewing_now.student = None
        interviewing_now.save()
        round = Round.objects.get(id=link.round.id)
        student_status = InterviewStatus.objects.get(user=user,round=round)
        student_status.status = "สอบเสร็จแล้ว"
        student_status.save()
        link.round = None
        link.active = False
        link.save()
        interviewing_now.student = None
        interviewing_now.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "skip" in request.POST:
        user_id = int(request.POST.get("skip"))
        user = User.objects.get(id=user_id)
        interviewing_now = InterviewNow.objects.get(interviewer=request.user)
        interviewing_now.student = None
        interviewing_now.save()
        round = Round.objects.get(id=link.round.id)
        student_status = InterviewStatus.objects.get(user=user,round=round)
        student_status.status = "ข้าม"
        student_status.reg_at = datetime.now()
        student_status.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    elif request.method == "POST" and "notify" in request.POST:
        user_id = int(request.POST.get("notify"))
        user = User.objects.get(id=user_id)
        token = link.round.line_Token
        meet = link.link
        send_line_notify(f'{user.first_name} {user.last_name}',token,meet)
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

    link = InterviewLink.objects.get(user=request.user)

    interviewer_interviewing = InterviewNow.objects.get(interviewer=request.user)
    interviewing = False
    if interviewer_interviewing.student:
        interviewing = True

    student = None
    all_scoretopic = None
    need_docs = None
    have_docs = []
    temp_remove_list = []
    if link.round and interviewing :
        interviewing_now = InterviewNow.objects.get(interviewer=request.user)
        student = InterviewStatus.objects.get(round=link.round,user=interviewing_now.student)
        need_docs = list(link.round.documents.all())
        for d in need_docs:
            if Document.objects.filter(user=student.user,doc_name=d.doc_name,round=link.round):
                have_docs.append(Document.objects.get(user=student.user,doc_name=d.doc_name,round=link.round))
                temp_remove_list.append(d)
        for d in temp_remove_list:
            need_docs.remove(d)
        if RoundScore.objects.filter(Round=link.round):
            pattern = RoundScore.objects.filter(Round=link.round).first()
            all_scoretopic = ScoreTopic.objects.filter(pattern_id=pattern.pattern)
        

    elif link.round and link.active:
        ready_student = InterviewStatus.objects.filter(round=link.round, status="พร้อมสอบ")
        skip_student = InterviewStatus.objects.filter(round=link.round, status="ข้าม")
        student = (ready_student | skip_student).distinct().order_by("reg_at").first()
        need_docs = link.round.documents.all()
        if student:
            interviewing_now = InterviewNow.objects.get(interviewer=request.user)
            student_status = InterviewStatus.objects.get(round=link.round,user=student.user)
            interviewing_now.student = student.user
            interviewing_now.save()
            student_status.status = "กำลังสอบ"
            student_status.save()

    data_student = None
    data_interviewer = None
    number_of_student = InterviewStatus.objects.filter(round=link.round).count()
    number_of_interviewer = InterviewLink.objects.filter(round=link.round).count()
    if link.round:
        data_student = {
            'labels': ["สอบเสร็จแล้ว", "กำลังสอบ", "พร้อมสอบ"],
            'data': [InterviewStatus.objects.filter(round=link.round,status="สอบเสร็จแล้ว").count(),
                    InterviewStatus.objects.filter(round=link.round,status="กำลังสอบ").count(),
                    InterviewStatus.objects.filter(round=link.round,status__in=["พร้อมสอบ","ข้าม"]).count()],
        }
        data_interviewer = {
                'labels': ["พร้อมสัมภาษณ์", "ไม่พร้อมสัมภาษณ์"],
                'data': [InterviewLink.objects.filter(round=link.round,active=True).count(),
                        InterviewLink.objects.filter(round=link.round,active=False).count(),],
                }

    context = {
        "docs" : student,
        "rounds" : combined_rounds,
        "link" : link,
        "not_selected" : not_selected_round,
        "have_docs" : have_docs,
        "need_docs" : need_docs,
        "all_scoretopic" : all_scoretopic,
        'data_student': data_student,
        'data_interviewer': data_interviewer,
        "number_of_student" : number_of_student,
        "number_of_interviewer" : number_of_interviewer,
    }
    return render(request,'interviewer/Interviewer_room.html', context)





#Student
@login_required
@user_passes_test(is_Student)
def student_page(request):
    Announcement_all = Announcement.objects.filter(role__name='Student')
    Schedule_all = Schedule.objects.filter(role__name='Student')
    return render(request,'student/Student_page.html',{'am':Announcement_all,'s':Schedule_all})
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
    
    uploaded_docs = Document.objects.filter(user=request.user).values_list('round', flat=True)

    all_round = []
    for r in combined_rounds.distinct():
        all_round.append({
            "round" : r,
            "uploaded" : Document.objects.filter(round=r, user=request.user).values_list('doc_name', flat=True)
        })
    if request.method == 'POST':
        user = request.user
        round = Round.objects.get(id=request.POST.get("round_id"))
        doc_name = request.POST.get("doc_name")
        file = request.FILES.get('file_name')
        if Document.objects.filter(user=user,doc_name=doc_name,round=round):
            document = Document.objects.get(user=user,doc_name=doc_name,round=round)
            document.document = file
            document.save()
        else:
            document = Document(user=user,round=round,doc_name=doc_name,document=file)
            document.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

    context = {
        'rounds': combined_rounds.distinct(),
        'registered_rounds': registered_rounds,
        'uploaded_docs': uploaded_docs,
        'all_round' : all_round,
        }
    return render(request,'student/Student_register.html',context)
@login_required
@user_passes_test(is_Student)
def Student_room(request):
    if request.method == "POST" and "skip" in request.POST:
        round_split = request.POST.get("skip").split('|')
        round = Round.objects.get(round_name=round_split[0],academic_year=round_split[1])
        student_status = InterviewStatus.objects.get(user=request.user,round=round)
        student_status.status = "ข้าม"
        student_status.reg_at = datetime.now()
        student_status.save()
        if InterviewNow.objects.filter(student=request.user):
            interviewing = InterviewNow.objects.get(student=request.user)
            interviewing.student = None
            interviewing.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    test = test = InterviewNow.objects.filter(student=request.user)

    context = {
        "test" : test
    }
    return render(request,'student/Student_room.html', context)

def convert_to_datetime(time_str):
    date_str, time_str = time_str.split()
    day, month, year = map(int, date_str.split('/'))
    start_time = time_str.split('-')[0]
    return datetime(year, month, day, int(start_time[:2]), int(start_time[3:]))

def interview_status(request):
    queue_time = "คุณยังไม่ได้มีการลงทะเบียน"
    user_position = None
    reg= None
    round_now = "ยังไม่มีการลงทะเบียน"
    if InterviewStatus.objects.filter(user=request.user):
        time_string_id = []
        current_round = None
        all_time = InterviewStatus.objects.filter(user=request.user, status__in=["พร้อมสอบ", "กำลังสอบ", "ข้าม"])
        if all_time:
            for time in all_time:
                time_string_id.append((time.id,time.round.interview_time))
            datetimes_with_id = [(id, convert_to_datetime(ts)) for id, ts in time_string_id]
            sorted_datetimes_with_id = sorted(datetimes_with_id, key=lambda x: x[1])
            sorted_id = sorted_datetimes_with_id[0][0]
            current_round = InterviewStatus.objects.filter(user=request.user,id=sorted_id)
        elif InterviewStatus.objects.filter(user=request.user, status__in=["สอบเสร็จแล้ว"]):
            for time in InterviewStatus.objects.filter(user=request.user, status__in=["สอบเสร็จแล้ว"]):
                time_string_id.append((time.id,time.round.interview_time))
            datetimes_with_id = [(id, convert_to_datetime(ts)) for id, ts in time_string_id]
            sorted_datetimes_with_id = sorted(datetimes_with_id, key=lambda x: x[1],reverse=True)
            sorted_id = sorted_datetimes_with_id[0][0]
            current_round = InterviewStatus.objects.get(user=request.user,id=sorted_id)
            round_now = f"{current_round.round.round_name}|{current_round.round.academic_year}"
            queue_time = "สอบเสร็จแล้ว"

        if current_round:
            r = InterviewStatus.objects.get(user=request.user,id=sorted_id)
            reg = InterviewStatus.objects.filter(status__in=["พร้อมสอบ", "กำลังสอบ", "ข้าม"],user=request.user,round=r.round)
            if reg:
                reg = InterviewStatus.objects.get(status__in=["พร้อมสอบ", "กำลังสอบ", "ข้าม"],user=request.user,round=r.round)
                interview_statuses = InterviewStatus.objects.filter(status__in=["พร้อมสอบ", "ข้าม"],round=reg.round).order_by('reg_at')
                check = InterviewStatus.objects.filter(round=reg.round).order_by('reg_at').first()
                round_now = f"{reg.round.round_name}|{reg.round.academic_year}"
                if check.status == "พร้อมสอบ":
                    queue_time = "ยังไม่เริ่มสอบ"
                else:
                    for index, status in enumerate(interview_statuses):
                        if status.user == request.user:
                            user_position = index + 1
                            queue_time = user_position*10
                            break
                    if InterviewStatus.objects.filter(status="กำลังสอบ",user=request.user,round=r.round):
                        queue_time = 0
    link = None
    interviewing = InterviewNow.objects.filter(student=request.user)
    if interviewing:
        student = InterviewNow.objects.get(student=request.user)
        link = InterviewLink.objects.get(user=student.interviewer)
        link = link.link
    data = []
    data.append({
        'link': link,
        'queue_time': queue_time,
        'queue_position': user_position,
        'round' : round_now,
    })
    return JsonResponse(data, safe=False)

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
        message = f'โปรดใช้รหัสนี้เพื่อยืนยันอีเมลของคุณ: {confirmation_code}'
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
                            
                            tem_user = TemporaryUser.objects.get(pk=temporary_user_id)
                            user = User.objects.filter(email=email).first()
                            role_model = Role.objects.get(name='Student')
                            role_model.users.add(user)
                            round_names = []
                            major_names = []
                            faculty_names=[]
                            for round_obj in tem_user.round_temp_user.all():
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
                            user.set_password(password)
                            user.save()
                            tem_user.delete()
                            send_registration_email(email,password,user.username)
                            return redirect('/')
 
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
                                user.first_name2 = temporary_user.first_name
                                user.last_name2 = temporary_user.last_name
                                user.birth_date = temporary_user.birth_date
                                user.citizen_id = temporary_user.citizen_id
                                role_model = Role.objects.get(name='Student')
                                role_model.users.add(user)
                                round_names = []
                                major_names = []
                                faculty_names=[]
                                for round_obj in tem_user.round_temp_user.all():
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
                                tem_user.delete()
                                send_registration_email(email,password,user.username)
                                return redirect('/')
                                #return redirect('social:begin', backend='google-oauth2')
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
        prefix = request.POST.get('prefix')
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        round = request.POST.get('round') 
        round = Round.objects.get(round_name=round)
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
                prefix=prefix,
                citizen_id=citizen_id,
                first_name=first_name,
                last_name=last_name,
                #birth_date=birth_date,
                password = citizen_id
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
        interview_time = request.POST.get('interview_time')
        major = Major.objects.get(major=major_name)

        r_mn = Role.objects.get(name="Manager")
        manager = r_mn.users.get(first_name=manager_name)
        interview_round, _ = Round.objects.get_or_create(major=major,
                                                         academic_year=academic_year,
                                                         round_name=round_name,
                                                         manager=manager,
                                                         interview_time=interview_time)
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
def add_ScorePattern(request):
    if request.method == "POST":
        round_value = request.POST.get("round")
        if round_value:
            template_num = request.POST.get('template_num')
            score_pattern = ScorePattern( pattern_name=template_num)
            score_pattern.save()
            round = Round.objects.get(id=round_value)
            Score_Round = RoundScore(pattern=score_pattern,Round=round)
            Score_Round.save()
            return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
        else:
            pattern_name = request.POST.get('pattern_name')
            pattern = ScorePattern(pattern_name=pattern_name,main_pattern=True)
            pattern.save()
            return redirect(f"/Score")

@login_required
@user_passes_test(is_admin)
def add_ScoreTopic(request):
    if request.method == "POST":
        round_value = request.POST.get("round")
        if round_value:
            template_num = request.POST.get('template_num')
            score_pattern = ScorePattern.objects.get(pattern_name=template_num)
            topic_name = request.POST.get('topic_name')
            max_score = request.POST.get('max_score')
            score_detail = request.POST.get('score_detail')
            score_topic, _ = ScoreTopic.objects.get_or_create( pattern_id=score_pattern,
                                                                topic_name=topic_name,
                                                                max_score=max_score,
                                                                score_detail=score_detail)
            score_topic.save()
            return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
        else:
            template_num = request.POST.get('template_num')
            print(template_num)
            template = ScorePattern.objects.get(id=template_num)
            topic_name = request.POST.get('topic_name')
            max_score = request.POST.get('max_score')
            score_detail = request.POST.get('score_detail')
            score_topic, _ = ScoreTopic.objects.get_or_create( pattern_id=template,
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
def delete_ScoreTemplate(request,id):
    object = ScorePattern.objects.get(pk=id)
    object.delete()
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
@login_required
@user_passes_test(is_admin)
def delete_ScoreTopic(request,id):
    object = ScoreTopic.objects.get(pk=id)
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
        round_edited = Round.objects.get(pk=id)

        name = request.POST.get('round_name')
        year = request.POST.get('academic_year')
        time = request.POST.get('interview_time')
        token = request.POST.get('line_Token')
        print(token)
        if "major" and 'manager_name' in request.POST:
            major_name = request.POST.get('major')
            manager_id = int(request.POST.get('manager_name'))
            major = Major.objects.get(major=major_name)
            r_mn = Role.objects.get(name="Manager")
            manager = r_mn.users.get(id=manager_id)
            round_edited.major=major
            round_edited.manager=manager
        round_edited.academic_year=year
        round_edited.round_name=name
        round_edited.interview_time=time
        round_edited.line_Token = token
        round_edited.save()
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

def confirm_add_TUser(request):
    if request.method == 'POST':
        data_list=report_temporaryUser.objects.all()
        for item in data_list:
            if not TemporaryUser.objects.filter(citizen_id=item.citizen_id).exists():
                new_user = TemporaryUser(
                    citizen_id=item.citizen_id,
                    first_name=item.first_name,
                    last_name=item.last_name,
                    prefix=item.prefix
                )
                new_user.save()
                Round_db = Round.objects.get(round_name=item.round_name)
                Round_db.TemporaryUser.add(new_user)  
                faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                faculty_instance.TemporaryUser.add(new_user)
                major_instance = Major.objects.get(major=Round_db.major.major)
                major_instance.TemporaryUser.add(new_user) 
            else:
                old_user = TemporaryUser.objects.get(citizen_id=item.citizen_id)
                Round_db = Round.objects.get(round_name=item.round_name)
                Round_db.TemporaryUser.add(old_user)  
                faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                faculty_instance.TemporaryUser.add(old_user)
                major_instance = Major.objects.get(major=Round_db.major.major)
                major_instance.TemporaryUser.add(old_user) 
            

        return redirect('TemporaryUser')
@login_required
@user_passes_test(is_admin)
def add_TemporaryUser_by_file(request):
    if request.method == 'POST':
        round = request.POST.get('round') 
        data = request.FILES.get('fileInputa')
        if data.name.endswith('.xlsx'):
            df = pd.read_excel(data)
        elif data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            pass
        try:
            data = df[['เลขบัตรประชาชน','คำนำหน้า','ชื่อ','นามสกุล']]
            report_temporaryUser.objects.all().delete()
        except Exception as e:
            return HttpResponse('คอลัมไม่ตรงตามที่ต้องการ')
        duplicate_register_id = []
        for index, row in data.iterrows():    
            register_id = str(row['เลขบัตรประชาชน']).strip()    
            user_with_email = TemporaryUser.objects.filter(citizen_id=register_id).first()    
            if user_with_email:
                duplicate_register_id.append(register_id)   
            report_temporaryUser.objects.create(
                    citizen_id=row['เลขบัตรประชาชน'],
                    first_name=row['ชื่อ'],
                    last_name=row['นามสกุล'],
                    prefix=row['คำนำหน้า'],
                    round_name=round
                            )
        request.session['duplicate_register_id'] = duplicate_register_id
        return redirect('report_TemporaryUser')

        user_old = []
        TemporaryUser_old = []
        # for i in range(len(data)):
        #     try:
        #         citizen_id = str(data.iloc[i]['เลขบัตรประชาชน']).strip()
        #     except Exception as e:
        #         citizen_id = str(data.iloc[i]['เลขบัตรประชาชน']).strip()
        #         return HttpResponse('เลขบัตรประชาชนไม่ถูกต้อง',citizen_id)
        #     try:
        #         first_name=(data.iloc[i]['first_name'].strip())
        #     except Exception as e:
        #         return HttpResponse('first_name ไม่ถูกต้อง')
        #     try:
        #         last_name=(data.iloc[i]['นามสกุล'].strip())
        #     except Exception as e:
        #         return HttpResponse('last_name ไม่ถูกต้อง')
            # try:
            #     birth_date_str=(data.iloc[i]['วว/ดด/ปป'].strip())
            #     birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
            # except Exception as e:
            #     return HttpResponse('วว/ดด/ปป ไม่ถูกต้อง')           
            # checkuser = User.objects.filter(citizen_id=citizen_id)
            # if not checkuser.exists():
            #     checkTemporaryUser = TemporaryUser.objects.filter(citizen_id=citizen_id)
                
            #     if not checkTemporaryUser.exists():
            #         Temporary_User = TemporaryUser.objects.create(citizen_id=citizen_id,first_name=first_name,last_name=last_name,password=citizen_id)#birth_date=birth_date
            #         role=Role.objects.filter(name='Student').first()
            #         role.TemporaryUser.add(Temporary_User)
            #         Round_db = Round.objects.get(pk=round_sel)
            #         Round_db.TemporaryUser.add(Temporary_User)  
            #         faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
            #         faculty_instance.TemporaryUser.add(Temporary_User)
            #         major_instance = Major.objects.get(major=Round_db.major.major)
            #         major_instance.TemporaryUser.add(Temporary_User) 
                    
            #     else:
            #         TemporaryUser_old.append(data.iloc[i]['ชื่อ'])
            #         user_id = checkTemporaryUser.first().id
            #         checkRound = Round.objects.filter(round_name=round,TemporaryUser=user_id)
            #         if not checkRound.exists():
            #             Round_db = Round.objects.get(pk=round_sel)
            #             Round_db.TemporaryUser.add(user_id)  
            #             faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
            #             faculty_instance.TemporaryUser.add(Temporary_User)
            #             major_instance = Major.objects.get(major=Round_db.major.major)
            #             major_instance.TemporaryUser.add(Temporary_User)                   
            #         else:
            #             pass
            #             #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')
            # else:
            #     user_old.append(data.iloc[i]['ชื่อ'])
            #     user_id = checkuser.first().id
            #     checkRound = Round.objects.filter(round_name=round,users=user_id)
            #     if not checkRound.exists():
            #         Round_db = Round.objects.get(pk=round_sel)
            #         Round_db.users.add(user_id)
            #         faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
            #         faculty_instance.users.add(Temporary_User)
            #         major_instance = Major.objects.get(major=Round_db.major.major)
            #         major_instance.users.add(Temporary_User)                     
            #     else:
            #         pass
            #         #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')

    #return redirect('TemporaryUser')

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
        register_id = request.POST.get('register_id')
        email =  request.POST.get('email')
        faculty_name = request.POST.get('faculty')  
        major_name = request.POST.get('major')  
        round = request.POST.get('round')  
        password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        checkboxgroup = request.POST.getlist('checkboxgroup')
        faculty = Faculty.objects.get(faculty=faculty_name)
        major= Major.objects.get(major=major_name, faculty=faculty)
        round= Round.objects.get(major__major=major_name, round_name=round)
        try:
            check_user = User.objects.get(email=email)
            faculty.users.add(check_user)
            major.users.add(check_user)
            round.users.add(check_user)
            return redirect('User')
        except User.DoesNotExist:
            new_user = User.objects.create(
                                           first_name= first_name,
                                           last_name= last_name,
                                           first_name2= first_name,
                                           last_name2= last_name,
                                           email= email ,
                                           username=register_id,
                                           password= make_password(password))
            faculty.users.add(new_user)
            major.users.add(new_user)
            faculty.users.add(new_user)
            major.users.add(new_user)
            round.users.add(new_user)
            for role_name in checkboxgroup:
                role_model, _ = Role.objects.get_or_create(name=role_name)
                role_model.users.add(new_user)
            send_registration_email("kamonsakprj@gmail.com",password,register_id)
            return redirect('User')
        
    return redirect("User")

def send_registration_email(email,password,username):
    subject = 'รหัสผ่านของเว็บจัดคิวสัมภาษณ์',email
    message = f'สามารถเข้าสู่ระบบทาง google ด้วย email: {email} หรือusername: {username} password: {password}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
@login_required
@user_passes_test(is_admin)
def add_User_by_file(request):
    if request.method == 'POST':
        data = request.FILES.get('fileInputa')
        checkboxgroup = request.POST.getlist('checkboxgroup')
        faculty_name = request.POST.get('faculty')  
        major_name = request.POST.get('major')  
        round = request.POST.get('round')  
        if data.name.endswith('.xlsx'):
            df = pd.read_excel(data)
        elif data.name.endswith('.csv'):
            df = pd.read_csv(data)
        else:
            pass
        try:
            data = df[['APPLICANTCODE','PREFIXNAME','APPLICANTNAME','APPLICANTSURNAME','EMAIL']]
            report_User.objects.all().delete()
        except Exception as e:
            return HttpResponse('คอลัมไม่ตรงตามที่ต้องการ')
        duplicate_emails = []
        for index, row in data.iterrows():    
            email = row['EMAIL']     
            user_with_email = User.objects.filter(email=email).first()    
            checkuser = User.objects.filter(email=email)
            if user_with_email:
                duplicate_emails.append(email)    
            report_User.objects.create(
                citizen_id=row['APPLICANTCODE'],
                first_name=row['APPLICANTNAME'],
                last_name=row['APPLICANTSURNAME'],
                first_name2=row['APPLICANTNAME'],
                last_name2=row['APPLICANTSURNAME'],
                prefix=row['PREFIXNAME'],
                email=row['EMAIL'],
                round_name=round,
                role_name=checkboxgroup
                )
        request.session['user_duplicate_emails'] = duplicate_emails
            # if not checkuser.exists():
            #     password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            #     create_User = User.objects.create(first_name=first_name,last_name=last_name,email=email)
            #     create_User.username = email
            #     create_User.save()
            #     send_registration_email("kamonsakprj@gmail.com",password,register_id)
            #     Faculty_add = Faculty.objects.filter(faculty=faculty).first()
            #     Faculty_add.users.add(create_User)
            #     Major_add = Major.objects.filter(major=major).first()
            #     Major_add.users.add(create_User)
            #     for role_name in checkboxgroup:
            #         role_model, _ = Role.objects.get_or_create(name=role_name)
            #         role_model.users.add(create_User)
            # else:
            #     user_old.append(data.iloc[i]['ชื่อ'])
            #     user_id = checkuser.first().id
            #     checkFaculty = Faculty.objects.filter(faculty=faculty,users=user_id)
            #     if not checkFaculty.exists():
            #         faculty_db = Faculty.objects.filter(faculty=faculty).first()
            #         faculty_db.users.add(user_id)                    
            #     else:
            #         pass
            #             #return HttpResponse(usernames[0]+'อยู่ใน' + faculty + 'แล้ว')
            #     checkMajor = Major.objects.filter(major=major,users=user_id)
            #     if not checkMajor.exists():
            #         Major_db = Major.objects.filter(major=major).first()
            #         Major_db.users.add(user_id)                    
            #     else:
            #         pass

    return redirect('report_User_to_html')
@login_required
@user_passes_test(is_admin)
def edit_User(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # citizen_id = request.POST.get('citizen_id')
        # email = request.POST.get('email')
        # birth_date_str = request.POST.get('birth_date')
        # birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y").date()
        checkboxgroup = request.POST.getlist('checkboxgroup')
        edit_user = User.objects.get(pk=user_id)
        role = Role.objects.filter(users=edit_user)
        for role in role:
            role.users.remove(edit_user)
        # edit_user.first_name=first_name
        # edit_user.last_name=last_name
        # edit_user.citizen_id=citizen_id
        # edit_user.birth_date=birth_date
        # edit_user.email=email
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
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

@login_required
@user_passes_test(is_Interviewer)
def toggle_status_active(request, link_id):
    link = get_object_or_404(InterviewLink, id=link_id)
    link.active = not link.active
    link.save()
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))


@login_required
@user_passes_test(is_Student)
def register_interview(request, round_id):
    round = get_object_or_404(Round, id=round_id)

    InterviewStatus.objects.update_or_create(
        user=request.user, round=round,
        defaults={'status': 'พร้อมสอบ'}
    )
    return redirect('/Student_room')

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
        round = request.POST.get('round')
        request.session['major'] = ma
        request.session['round'] = round
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
        change_link, create = InterviewLink.objects.get_or_create(user=user)
        change_link.link = link
        change_link.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

    return redirect('/Interviewer_page')


@login_required
@user_passes_test(is_Manager)
def Manager_ScoreTopic(request,id):
    round = Round.objects.get(id=id)
    pattern_id = "None"

    round_name = f"{round.round_name}_{round.academic_year}_{round.major.major}"
    templates = ScorePattern.objects.filter(main_pattern=True)

    template = ScorePattern.objects.filter(pattern_name=round_name).first()
    topics = ScoreTopic.objects.filter(pattern_id=template)

    if request.method == "POST":
        pattern_id = request.POST.get("pattern")
        pattern_name = request.POST.get("round_name")

        Pattern = ScorePattern.objects.get(pattern_name=pattern_id)
        Topic_in_Pattern = ScoreTopic.objects.filter(pattern_id=Pattern)
        new_pattern = ScorePattern(pattern_name=pattern_name)
        new_pattern.save()
        for t in Topic_in_Pattern:
            new_topic = ScoreTopic(pattern_id=new_pattern,topic_name=t.topic_name,max_score=t.max_score,score_detail=t.score_detail)
            new_topic.save()
            round_score = RoundScore(pattern=new_pattern,Round=round)
            round_score.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    if RoundScore.objects.filter(Round=round):
        text = True
        pattern_id = template.id
    else:
        text = False

    context = {
        "text" : text,
        "no_topic" : templates,
        "round" : round_name,
        "round_id" : round,
        "topics" : topics,
        "pattern_id" : pattern_id
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
        user.first_name2 = first_name
        user.last_name2 = last_name
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
        try:
            selected_rounds_str = request.POST.get('selectedRounds').split(',')
        except ObjectDoesNotExist:
            pass
        checkboxgroup = request.POST.getlist('checkboxgroup')
        add_announcement =Announcement.objects.create(title=topic,announcement_content=details)
        try:
            if selected_rounds_str[0]:
                for rounds in selected_rounds_str:
                    round_name, year = rounds.rsplit(" (", 1)
                    year = year.strip(")")
                    round = Round.objects.get(round_name=round_name,academic_year=year)
                    add_announcement.round.add(round)
                    add_announcement.major.add(round.major)
        except ObjectDoesNotExist:
            pass
        try:
            for role in checkboxgroup:
                role = Role.objects.get(name=role)
                add_announcement.role.add(role)
        except ObjectDoesNotExist:
            pass
        return redirect('Announcement_page')
    
def delete_Announcement(request,id):
    delete_Am = Announcement.objects.get(pk=id)
    delete_Am.delete()
    return redirect('Announcement_page')

def Manager_StatusRound(request,id):
    round = Round.objects.get(id=id)
    Interviewers =  InterviewLink.objects.filter(round=round)
    StudentInRound = InterviewStatus.objects.filter(round=round).order_by("reg_at")

    interviewers_data = []
    for interviewer_link in Interviewers:
        interviewer = interviewer_link.user
        interview_now = InterviewNow.objects.filter(interviewer=interviewer).first()
        student = interview_now.student if interview_now else None
        interviewers_data.append({
            "interview_link": interviewer_link,
            "student": student
        })

    if request.method == "POST" and "round_exit" in request.POST:
        round_id = int(request.POST.get("round_exit"))
        interviewer_id = int(request.POST.get("interviewer_id"))
        round = Round.objects.get(id=round_id)
        interviewer = User.objects.get(id=interviewer_id)
        interviewing_now = InterviewNow.objects.filter(interviewer=interviewer)
        interviewer_link = InterviewLink.objects.get(user=interviewer)
        if interviewing_now:
            now = InterviewNow.objects.get(interviewer= interviewer)
            student_status = InterviewStatus.objects.filter(user=now.student,round=round)
            now.student = None
            now.save()
            if student_status:
                status = student_status.first()
                status.status = "พร้อมสอบ"
                status.save()
        interviewer_link.round = None
        interviewer_link.active = False
        interviewer_link.save()
        return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))
    
    context = {
        "Students" : StudentInRound,
        "Interviewers" : interviewers_data,
        "round" : round,
    }
    return render(request, "manager/Manager_StatusRound.html", context)

def edit_Announcement(request):
    if request.method == 'POST':
        Announcement_id = request.POST.get('Announcement_id')
        topic = request.POST.get('topic')
        details = request.POST.get('details')
        selected_rounds_str = request.POST.get('edit_selectedRounds').split(',')
        checkboxgroup = request.POST.getlist('checkboxgroup')
        edit_announcement = Announcement.objects.get(pk=Announcement_id)
        edit_announcement.title = topic
        edit_announcement.announcement_content = details
        edit_announcement.role.clear()
        edit_announcement.round.clear()
        edit_announcement.major.clear()
        try:
            for role_name in checkboxgroup:
                role_model = Role.objects.get(name=role_name)
                edit_announcement.role.add(role_model)
        except ObjectDoesNotExist:
            pass
        try:
            for round in selected_rounds_str:
                round_name, year = round.rsplit(" (",1)
                round_name = round_name.lstrip()
                year = year.strip(")")
                round_model = Round.objects.get(round_name=round_name,academic_year=year)
                edit_announcement.round.add(round_model)
                edit_announcement.major.add(round_model.major)

        except ObjectDoesNotExist:
            pass
        
        edit_announcement.save()
        return redirect('Announcement_page')
    
def addSchedule(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        details = request.POST.get('details')
        date_str = request.POST.get('expire_date')
        date_object = datetime.strptime(date_str, '%d/%m/%Y')
        try:
            selected_rounds_str = request.POST.get('selectedRounds').split(',')
        except ObjectDoesNotExist:
            pass
        checkboxgroup = request.POST.getlist('checkboxgroup')
        add_Schedule =Schedule.objects.create(schedule_name=topic,schedule_content=details,end_date=date_object)
        try:
            print(selected_rounds_str)
            if selected_rounds_str[0]:
                for rounds in selected_rounds_str:
                    round_name, year = rounds.rsplit(" (", 1)
                    year = year.strip(")")
                    round = Round.objects.get(round_name=round_name,academic_year=year)
                    add_Schedule.round.add(round)
                    add_Schedule.major.add(round.major)
        except ObjectDoesNotExist:
            pass
        try:
            for role in checkboxgroup:
                role = Role.objects.get(name=role)
                add_Schedule.role.add(role)
        except ObjectDoesNotExist:
            pass
        return redirect('Announcement_page')

def edit_Schedule(request):
    if request.method == 'POST':
        Schedule_id = request.POST.get('Schedule_id')
        topic = request.POST.get('topic')
        details = request.POST.get('details')

        selected_rounds_str = request.POST.get('edit_selectedRounds_schedule').split(',')
        print(selected_rounds_str)
        checkboxgroup = request.POST.getlist('checkboxgroup')
        edit_Schedule = Schedule.objects.get(pk=Schedule_id)
        edit_Schedule.schedule_name = topic
        edit_Schedule.schedule_content = details
        edit_Schedule.role.clear()
        edit_Schedule.round.clear()
        edit_Schedule.major.clear()
        try:
            date = request.POST.get('expire_date')
            ndate = datetime.strptime(date, "%d/%m/%Y").date()
            edit_Schedule.end_date = ndate
        except ObjectDoesNotExist:
            pass
        try:
            for role_name in checkboxgroup:
                role_model = Role.objects.get(name=role_name)
                edit_Schedule.role.add(role_model)
        except ObjectDoesNotExist:
            pass
        try:
            for round in selected_rounds_str:
                round_name, year = round.rsplit(" (",1)
                round_name = round_name.lstrip()
                year = year.strip(")")
                round_model = Round.objects.get(round_name=round_name,academic_year=year)
                edit_Schedule.round.add(round_model)
                edit_Schedule.major.add(round_model.major)

        except ObjectDoesNotExist:
            pass
        
        edit_Schedule.save()
        return redirect('Announcement_page')

def delete_Schedule(request,id):
    delete_Sd = Schedule.objects.get(pk=id)
    delete_Sd.delete()
    return redirect('Announcement_page')




def decrease_manager(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        major_name = request.POST.get('major')
        major  =  Major.objects.get(major=major_name)
        manager  =  User.objects.get(pk=user_id)
        major.default_manager.remove(manager)
        major.save()

    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))

def increase_manager(request):
    if request.method == 'POST':
        user_id = request.POST.get('id')
        major_name = request.POST.get('major')
        major  =  Major.objects.get(major=major_name)
        manager  =  User.objects.get(pk=user_id)
        major.default_manager.add(manager)
        major.save()

    return redirect(request.META.get('HTTP_REFERER', 'fallback-url'))


def send_line_notify(message,token,meet):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded', 'Authorization':'Bearer '+token}
    msg = message + " กรุณาเข้าห้องสอบสัมภาษณ์ ลิงค์ : " + meet + " ด้วยครับ"
    requests.post(url, headers=headers, data = {'message':msg})


def ajax_select_round(request):
    faculty_name = request.GET.get('faculty')  
    major_object = Major.objects.get(major=faculty_name)
    round = Round.objects.filter(major__major=major_object)
    return render(request, 'manager/dropdown-list.html', {"majors": round})

def backup_data(request):
        folder_path ="./backup_data"
        backup_folder = "./backup_data"
        os.makedirs(backup_folder, exist_ok=True) 
        folder_path1 = "./db/mydb" 
        folder_path2 = "./media"

        destination1 = os.path.join(backup_folder, 'mydb')
        shutil.copytree(folder_path1, destination1)
        destination2 = os.path.join(backup_folder, 'media')
        shutil.copytree(folder_path2, destination2)

        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=backup_data.zip'
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, subfolders, filenames in os.walk(backup_folder):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zip_path = os.path.relpath(file_path, backup_folder)
                    zipf.write(file_path, zip_path)

        buffer.seek(0)
        response.write(buffer.read())
        try:
            shutil.rmtree(folder_path)
        except FileNotFoundError:
            print(f"ไม่พบโฟลเดอร์ {folder_path}")
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการลบโฟลเดอร์ {folder_path}: {str(e)}")

        return response


def student_one_tocsv(request):
    myuser_id = request.session.get('myuser_id')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    if request.method == 'POST':
        checkbox_all = request.POST.get('checkbox_all') 
        checkbox_all_T = request.POST.get('checkbox_all_T') 
        checkbox = request.POST.getlist('checkbox')
        Evidence_check = request.POST.get('Evidence_check')
        score = request.POST.get('score') 
        score_max = request.POST.get('score_max') 
        interviewer_name = request.POST.get('interviewer_name') 
        student_name = request.POST.get('student_name') 
        total_score = request.POST.get('total_score') 
        email = request.POST.get('email') 
        topic_list = []
        data_list = []
        if student_name :
            topic_list.append('ชื่อนักเรียน')
            data_list.append(student_name)
        if interviewer_name :
            topic_list.append('ผู้สัมภาษณ์')
            data_list.append(interviewer_name)
        if checkbox_all == 'True':
            checkbox_split = checkbox_all_T.split(',')[0:-1]
            for i in range(len(checkbox_split)):
                topic_list.append('รายการที่ '+str(i+1))
                topic = checkbox_split[i].split('-')[0]
                data_list.append(topic)
        else:
            for i in range(len(checkbox)):
                topic_list.append('รายการที่'+str(i+1))
                topic = checkbox[i].split('-')[0]
                data_list.append(topic)

        if score == 'True':
            if checkbox_all == 'True':
                checkbox_split = checkbox_all_T.split(',')[0:-1]
                for i in range(len(checkbox_split)):
                    topic_list.append('คะแนนรายการที่ '+str(i+1))
                    topic = checkbox_split[i].split('-')[2]
                    data_list.append(topic)
            else:
                for i in range(len(checkbox)):
                    topic_list.append('คะแนนรายการที่'+str(i+1))
                    topic = checkbox[i].split('-')[2]
                    data_list.append(topic)

        if score_max == 'True':
            if checkbox_all == 'True':
                checkbox_split = checkbox_all_T.split(',')[0:-1]
                for i in range(len(checkbox_split)):
                    topic_list.append('คะแนนเต็มที่ '+str(i+1))
                    topic = checkbox_split[i].split('-')[1]
                    data_list.append(topic)
            else:
                for i in range(len(checkbox)):
                    topic_list.append('คะแนนเต็มที่'+str(i+1))
                    topic = checkbox[i].split('-')[1]
                    data_list.append(topic)

        score_plus = []
        if total_score:
            for i in range(len(topic_list)):
                if topic_list[i][0:11] == 'คะแนนรายการ':
                    if data_list[i] != '-':
                        score_plus.append(int(data_list[i]))
        score_max_plus = []
        if total_score:
            for i in range(len(topic_list)):
                if topic_list[i][0:9] == 'คะแนนเต็ม':
                    score_max_plus.append(int(data_list[i]))
        if total_score:
            topic_list.append('คะแนนรวมเต็ม')
            data_list.append(sum(score_max_plus))
        if total_score:
            topic_list.append('คะแนนรวม')
            data_list.append(sum(score_plus))
        if email:
            email_split = email.split('@')[0]
        response_csv = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{email_split}".csv'},
         )
        response_csv.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response_csv)
        writer.writerow(topic_list)
        writer.writerow(data_list)

    if Evidence_check :
        folder_path ="./Evidence"
        Evidence_folder = "./Evidence"
        data_file_path = f'./{student_name}.csv'
        with open(data_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
            writer = csv.writer(file)
            writer.writerow(topic_list)
            writer.writerow(data_list)
        year_round = Round.objects.filter(round_name=round_from_session).first()
        if year_round:
            year = year_round.academic_year
        else:
            year = None  
        link = f'./media/Evidence/{major_from_session}/{round_from_session}/{student_name}'
        os.makedirs(Evidence_folder, exist_ok=True) 
    

        try:
            destination2 = os.path.join(Evidence_folder, f'{student_name}')
            shutil.copytree(link, destination2)
        except FileNotFoundError:
            print(f"ไม่พบโฟลเดอร์ที่ทาง {link}")

        try:
            destination1 = os.path.join(Evidence_folder, f'{student_name}.csv')
            shutil.copy(data_file_path, destination1)
        except FileNotFoundError:
            print(f"ไม่พบไฟล์ที่ทาง {data_file_path}")

        filename = f'{major_from_session}_{round_from_session}_{year}_{student_name}_{interviewer_name}.zip'
        filename_encoded = quote(filename)
        response = HttpResponse(content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{filename_encoded}'
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for foldername, subfolders, filenames in os.walk(Evidence_folder):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zip_path = os.path.relpath(file_path, Evidence_folder)
                    zipf.write(file_path, zip_path)

        buffer.seek(0)
        response.write(buffer.read())
        try:
            shutil.rmtree(folder_path)
        except FileNotFoundError:
                print(f"ไม่พบโฟลเดอร์ {folder_path}")
        try:
            os.remove(data_file_path)
        except FileNotFoundError:
                print(f"ไม่พบไฟล์.csv {data_file_path}")
        return response
    else:
        return response_csv    


def form_student_all(request):
    myuser_id = request.session.get('myuser_id')
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    if request.method == 'POST':
        student_index = request.POST.get('index') 
        student_index_list = student_index.split(',')[0:-1]
        topic_scores_all = []
        column = []
        student_ex=[]
        index = 0
        processed_scores = set()
        for i in student_index_list:
            student = User.objects.get(pk=i)
            round_score = RoundScore.objects.filter(Round__round_name=round_from_session).select_related('pattern').first()
            scores_topic = ScoreTopic.objects.filter(pattern_id=round_score.pattern)
            student_info = {
                    'student': student.prefix+student.first_name+' '+ student.last_name,
                    'interviewer': '-',
                    'scores': [] ,
                    'scores_max': [] 
                }
            for i in scores_topic:
                student_info['scores'].append({
                    'topic_name': i.topic_name,
                    'score': '0'})
                student_info['scores_max'].append(
                    {'topic_name': i.topic_name,
                     'scores_max': i.max_score})
            for topic in scores_topic:
                topic_score = Score.objects.filter(student=student,topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)
                for score in topic_score:
                    for i in range(len(student_info['scores'])):
                        if student_info['scores'][i]['topic_name'] == score.topic.topic_name:
                            student_info['scores'][i]['score']=score.score
                    if score.topic.topic_name not in processed_scores: 
                        topic_scores_all.append(score)
                        column.append([index ,score.topic.topic_name])
                        processed_scores.add(score.topic.topic_name)
                        index = index+1
                    if student_info['interviewer'] == '-':
                        interviewer_name = score.interviewer.prefix+score.interviewer.first_name+' '+score.interviewer.last_name
                        student_info['interviewer'] = interviewer_name
            if len(student_ex) < 5:
                student_ex.append(student_info)
        context = {
            'student_ex':student_ex,
            "student":student,
            'index_student':student_index_list,
            'column_topic_name':column,
            'scores': topic_scores_all,
            "s_major" : major_from_session,
            "faculty_all" : faculty_all,
            "majors" : majors,
            "s_round" : round_from_session,
        }
        
        return render(request,'manager/form_student/student_all.html',context)

    return render(request, 'manager/form_student/student_all.html',{'faculty_all':faculty_all,'majors':majors})


def student_all_tocsv(request):
    myuser_id = request.session.get('myuser_id')
    major_from_session = request.session.get('major')
    round_from_session = request.session.get('round')
    faculty_all = Faculty.objects.filter(users=myuser_id)
    majors = Major.objects.filter(default_manager=myuser_id)
    if request.method == 'POST':
        checkbox_all = request.POST.get('checkbox_all') 
        checkbox = request.POST.getlist('checkbox')
        score_check = request.POST.get('score') 
        Evidence_check = request.POST.get('Evidence_check') 
        score_max = request.POST.get('score_max') 
        get_interviewer_name = request.POST.get('interviewer_name') 
        student_name = request.POST.get('student_name') 
        total_score = request.POST.get('total_score') 
        student_index = request.POST.get('index')
        student_index =eval(student_index)
        topic_scores_all = []
        column = []
        
        
        student_ex=[]
        index = 0
        interviewer_name = '-'
        processed_scores = set()
        column_to_csv = []
        data_to_csv = []
        if student_name == 'True':
            column_to_csv.append('ชื่อนักเรียน')
        if get_interviewer_name == 'True':
            column_to_csv.append('ชื่อผู้สัมภาษณ์')
        for i in student_index:
            list_score_max = []
            list_topic = []
            index_list = 1
            data = []
            student = User.objects.get(pk=i)
            round_score = RoundScore.objects.filter(Round__round_name=round_from_session).select_related('pattern').first()
            scores_topic = ScoreTopic.objects.filter(pattern_id=round_score.pattern)
            if student_name == 'True':
                data.append(student.prefix+student.first_name+' '+ student.last_name)
            student_info = {
                    'student': student.prefix+student.first_name+' '+ student.last_name,
                    'interviewer': 'ไม่มีผู้สัมภาษณ์',
                    'scores': [] ,
                    'scores_max': [] 
                }
            list_score = []
            if checkbox_all == 'True':
                list_score = []
                for i in scores_topic:
                    if i.topic_name not in list_topic:
                        list_topic.append(i.topic_name)
                        list_score_max.append(i.max_score)
                    student_info['scores'].append({
                        'topic_name': i.topic_name,
                        'score': '-'})
                    student_info['scores_max'].append(
                        {'topic_name': i.topic_name,
                        'scores_max': i.max_score})
                    index_list = int(index_list)+1
                    

                for topic in scores_topic:
                    topic_score = Score.objects.filter(student=student,topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)
                    if topic_score:
                        for i in topic_score:
                            list_score.append(i.score)
                    else:
                        list_score.append('-')
                    for score in topic_score:

                        for i in range(len(student_info['scores'])):
                            if student_info['scores'][i]['topic_name'] == score.topic.topic_name:
                                student_info['scores'][i]['score']=score.score
                        if score.topic.topic_name not in processed_scores: 
                            topic_scores_all.append(score)
                            column.append([index ,score.topic.topic_name])
                            processed_scores.add(score.topic.topic_name)
                            index = index+1
                        if student_info['interviewer'] == 'ไม่มีผู้สัมภาษณ์':
                            interviewer_name = score.interviewer.prefix+score.interviewer.first_name+' '+score.interviewer.last_name
                            student_info['interviewer'] = interviewer_name
            else:
                for i in scores_topic:
                    list_score = []
                    if i.topic_name  in checkbox:
                        if i.topic_name not in list_topic:
                            list_topic.append(i.topic_name)
                            list_score_max.append(i.max_score)
                        student_info['scores'].append({
                            'topic_name': i.topic_name,
                            'score': '-'})
                        student_info['scores_max'].append(
                            {'topic_name': i.topic_name,
                            'scores_max': i.max_score})
                        index_list = int(index_list)+1


                    for topic in scores_topic:
                        if topic.topic_name  in checkbox:
                            topic_score = Score.objects.filter(student=student,topic__topic_name=topic,topic__pattern_id__pattern_name=round_score.pattern.pattern_name)
                            if topic_score:
                                for i in topic_score:
                                    list_score.append(i.score)
                            else:
                                list_score.append('-')
                            for score in topic_score:

                                for i in range(len(student_info['scores'])):
                                    if student_info['scores'][i]['topic_name'] == score.topic.topic_name:
                                        student_info['scores'][i]['score']=score.score
                                if score.topic.topic_name not in processed_scores: 
                                    topic_scores_all.append(score)
                                    column.append([index ,score.topic.topic_name])
                                    processed_scores.add(score.topic.topic_name)
                                    index = index+1
                                if student_info['interviewer'] == 'ไม่มีผู้สัมภาษณ์':
                                    interviewer_name = score.interviewer.prefix+score.interviewer.first_name+' '+score.interviewer.last_name
                                    student_info['interviewer'] = interviewer_name                
            if get_interviewer_name == 'True':
                data.append(interviewer_name)
            
            data.extend(list_topic)
            if score_check == 'True':
                data.extend(list_score)
            if score_max == 'True':
                data.extend(list_score_max)
            if total_score == 'True':
                sum_list_score =0
                sum_list_score_max = 0
                for i in list_score:
                    if i != '-':
                        sum_list_score = sum_list_score + int(i) 
                for i in list_score_max:
                    if i != '-':
                        sum_list_score_max = sum_list_score_max + int(i) 
                data.append(sum_list_score_max)
                data.append(sum_list_score)

            if len(student_ex) < 5:
                student_ex.append(student_info)

            data_to_csv.append(data) 
            

        for i in range(len(list_topic)):
            column_to_csv.append('รายการที่ '+(str(i+1)))
        if score_check == 'True':
            for i in range(len(list_topic)):
                column_to_csv.append('คะแนนรายการ '+(str(i+1)))
        if score_max == 'True':
            for i in range(len(list_topic)):
                column_to_csv.append('คะแนนเต็มที่ '+(str(i+1)))
        if total_score == 'True':
                column_to_csv.append('คะแนนรวมเต็ม')
                column_to_csv.append('คะแนนรวม')
        response_csv = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{round_from_session}".csv'},
         )
        response_csv.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response_csv)
        writer.writerow(column_to_csv)

        
        if Evidence_check :
            folder_path ="./Evidence"
            Evidence_folder = "./Evidence"
            data_file_path = f'./data.csv'
            with open(data_file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(column_to_csv)
                for i in data_to_csv:
                    writer.writerow(i)
            year_round = Round.objects.filter(round_name=round_from_session).first()
            if year_round:
                year = year_round.academic_year
            else:
                year = None  
            os.makedirs(Evidence_folder, exist_ok=True) 
        
            for i in student_index:
                student = User.objects.get(pk=i)
                name = student.first_name+' '+student.last_name
                link = f'./media/Evidence/{major_from_session}/{round_from_session}/{name}'
                try:
                    count = 1
                    destination2 = os.path.join(Evidence_folder, f'หลักฐานการสัมภาษณ์')
                    shutil.copytree(link, destination2)
                    files = os.listdir(destination2)
                    for file in files:
                        new_name = f"{name}_{count}.png"
                        old_file_path = os.path.join(destination2, file)
                        new_file_path = os.path.join(destination2, new_name)
                        os.rename(old_file_path, new_file_path)
                        print(f"เปลี่ยนชื่อ {file} เป็น {new_name}")
                    
                    # เพิ่มนับเลขไฟล์
                    count += 1
                except FileNotFoundError:
                    print(f"ไม่พบโฟลเดอร์ที่ทาง {link}")

            try:
                destination1 = os.path.join(Evidence_folder, f'data.csv')
                shutil.copy(data_file_path, destination1)
            except FileNotFoundError:
                print(f"ไม่พบไฟล์ที่ทาง {data_file_path}")

            filename = f'{major_from_session}_{round_from_session}_{year}.zip'
            filename_encoded = quote(filename)
            response = HttpResponse(content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{filename_encoded}'
            buffer = BytesIO()
            with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for foldername, subfolders, filenames in os.walk(Evidence_folder):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        zip_path = os.path.relpath(file_path, Evidence_folder)
                        zipf.write(file_path, zip_path)

            buffer.seek(0)
            response.write(buffer.read())
            try:
                shutil.rmtree(folder_path)
            except FileNotFoundError:
                    print(f"ไม่พบโฟลเดอร์ {folder_path}")
            try:
                os.remove(data_file_path)
            except FileNotFoundError:
                    print(f"ไม่พบไฟล์.csv {data_file_path}")
            return response
        else:
            return response_csv              


        context = {
            'student_ex':student_ex,
            "student":student,
            'index_student':student_index,
            'column_topic_name':column,
            'scores': topic_scores_all,
            "s_major" : major_from_session,
            "faculty_all" : faculty_all,
            "majors" : majors,
            "s_round" : round_from_session,
        }
        
    return redirect(request.META.get('HTTP_REFERER', 'fallback-url')) 

def mode(request):
    if request.method == 'POST':
        button = request.POST.get('button') 
        instances_mode = login_mode.objects.all()
        # mode = None
        for instance in instances_mode:
                instance.mode = button
                instance.save()


    return redirect(request.META.get('HTTP_REFERER', 'fallback-url')) 

def ajax_round(request):
    major_name = request.GET.get('major')  
    major_object = Major.objects.get(major=major_name)
    round = major_object.round_set.all()
    print(round)

    return render(request, 'admin/dropdown-round.html', {"rounds": round})

def report_User_to_html(request):
    data_list=report_User.objects.all()
    duplicate_emails = request.session.get('user_duplicate_emails', [])
    users_with_duplicates = []
    users_without_duplicates = []
    for user in data_list:
        if user.email in duplicate_emails:
            users_with_duplicates.append(user)
        else:
            users_without_duplicates.append(user)
    return render(request,'admin/report_user/report_User.html',{"data_list":users_without_duplicates,"data_duplicates":users_with_duplicates})

def confirm_adduser(request):
  if request.method == 'POST':
        data_list=report_User.objects.all()
        for item in data_list:
            if not User.objects.filter(email=item.email).exists():
        
                new_user = User(
                    username=item.citizen_id,
                    first_name=item.first_name,
                    last_name=item.last_name,
                    email=item.email,
                    prefix=item.prefix
                )
                new_user.save()
                Round_db = Round.objects.get(round_name=item.round_name)
                Round_db.users.add(new_user)  
                faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                faculty_instance.users.add(new_user)
                major_instance = Major.objects.get(major=Round_db.major.major)
                major_instance.users.add(new_user) 
                role = item.role_name
                list_role = eval(role)
                for role_name in list_role:
                        role_model, _ = Role.objects.get_or_create(name=role_name)
                        role_model.users.add(new_user)
            else:
                old_user = User.objects.get(email=item.email)
                Round_db = Round.objects.get(round_name=item.round_name)
                Round_db.users.add(old_user)  
                faculty_instance = Faculty.objects.get(faculty=Round_db.major.faculty.faculty)
                faculty_instance.users.add(old_user)
                major_instance = Major.objects.get(major=Round_db.major.major)
                major_instance.users.add(old_user) 
                role = item.role_name
                list_role = eval(role)
                for role_name in list_role:
                        role_model, _ = Role.objects.get_or_create(name=role_name)
                        role_model.users.add(old_user)
            

        return redirect('User')
  
