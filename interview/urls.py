from django.urls import path,include
from interview.views import * 
urlpatterns = [
    path('', index,name='index'),
    path('login',log_in, name='log_in'),
    path('first_login',first_login, name='first_login'),
    path('logout',log_out, name='log_out'),
    path('accounts/', include('allauth.urls')), 
    path('auth/', include('social_django.urls', namespace='social')),
    path('test',test, name='test'),


    #Siteuser
    


    #Admin
    path('Admin_page',admin_page, name='Admin_page'),
    path('Announcement',Announcement, name='Announcement'),
    path('FacultyMajor',FacultyMajor, name='FacultyMajor'),
    path('Interview',Interview, name='Interview'),
    path('Score',Score, name='Score'),
    path('TemporaryUser',TemporaryUser_path, name='TemporaryUser'),
    path('User',User_path, name='User'),
    path('form_interview',form_interview, name='form_interview'),
    path('profile',admin_profile, name='profile'),
    path('add_Faculty',add_Faculty, name='add_Faculty'),
    path('delete_Faculty/<int:id>',delete_Faculty ,name='delete_Faculty'),
    path('add_Major',add_Major, name='add_Major'),
    path('delete_Major/<int:id>',delete_Major ,name='delete_Major'),
    


    #manage
    path('Manager_page',manager_page, name='Manager_page'),
    path('manage_profile',manage_profile, name='manage_profile'),
    path('Manage_personnel',Manage_personnel, name='Manage_personnel'),
    path('Manager_Announcement',Manager_Announcement, name='Manager_Announcement'),
    path('Manager_interview',Manager_interview, name='Manager_interview'),
    path('Manager_Score',Manager_Score, name='Manager_Score'),
    path('Manager_Print_Interview',Manager_Print_Interview, name='Manager_Print_Interview'),
    path('Manager_Status',Manager_Status, name='Manager_Status'),

    #Interviewer
    path('Interviewer_page',interviewer_page, name='Interviewer_page'),
    path('Interviewer_Profile',Interviewer_Profile, name='Interviewer_Profile'),
    path('Interviewer_room',Interviewer_room, name='Interviewer_room'),

    #Student
    path('Student_page',student_page, name='Student_page'),
    path('confirm_email',confirm_email, name='confirm_email'),
    path('Student_profile',Student_profile, name='Student_profile'),
    path('Student_register',Student_register, name='Student_register'),
    path('Student_room',Student_room, name='Student_room'),
    path('Student_evidence',Student_evidence, name='Student_evidence'),

    path('confirm_otp',confirm_otp, name='confirm_otp'),
    path('changepassword',changepassword, name='changepassword'),
    path('send_email_password',send_email_password, name='send_email_password'),

]