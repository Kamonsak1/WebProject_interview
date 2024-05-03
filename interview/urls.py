from django.urls import path,include
from interview.views import * 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', index,name='index'),
    path('login',log_in, name='log_in'),
    path('first_login',first_login, name='first_login'),
    path('logout',log_out, name='log_out'),
    path('accounts/', include('allauth.urls')), 
    path('auth/', include('social_django.urls', namespace='social')),
    path('test',test, name='test'),
     path('google_LOGIN_URL',google_LOGIN_URL, name='google_LOGIN_URL'),
    path('ajax_load_major',ajax_load_major, name='ajax_load_major'),
    path('ajax_load_cities',ajax_load_cities, name='ajax_load_cities'),
    path('ajax_searchText',ajax_searchText, name='ajax_searchText'),
    path('ajax_round',ajax_round, name='ajax_round'),
    path('ajax_select_round',ajax_select_round, name='ajax_select_round'),
    path('backup_data',backup_data, name='backup_data'),
    path('mode',mode, name='mode'),

    #Siteuser
    path('profile_changname',profile_changname, name='profile_changname'),
    path('profile_changemail',profile_changemail, name='profile_changemail'),
    path('profile_changecitizen_id',profile_changecitizen_id, name='profile_changecitizen_id'),
    path('profile_changephone_number',profile_changephone_number, name='profile_changephone_number'),
    path('profile_changeaddress',profile_changeaddress, name='profile_changeaddress'),
    path('profile_send_otp',profile_send_otp, name='profile_send_otp'),
    path('profile_hbd',profile_hbd, name='profile_hbd'),


    #Admin
    path('Admin_page',admin_page, name='Admin_page'),
    path('Announcement_page',Announcement_page, name='Announcement_page'),
    path('FacultyMajor',FacultyMajor, name='FacultyMajor'),
    path('Interview',Interview, name='Interview'),
    path('Score',Admin_Score, name='Score'),
    path('TemporaryUser',TemporaryUser_path, name='TemporaryUser'),
    path('confirm_add_TUser',confirm_add_TUser, name='confirm_add_TUser'),
    path('report_TemporaryUser',report_TemporaryUser,name='report_TemporaryUser'),
    path('User',User_path, name='User'),
    #path('form_interview',form_interview, name='form_interview'),
    path('profile',admin_profile, name='admin_profile'),
    path('add_Faculty',add_Faculty, name='add_Faculty'),
    path('delete_Faculty/<int:id>',delete_Faculty ,name='delete_Faculty'),
    path('add_Major',add_Major, name='add_Major'),
    path('delete_Major/<int:id>',delete_Major ,name='delete_Major'),
    path('add_TemporaryUser',add_TemporaryUser, name='add_TemporaryUser'),
    path('report_User_to_html',report_User_to_html, name='report_User_to_html'),
    path('confirm_adduser',confirm_adduser, name='confirm_adduser'),
    path('delete_TemporaryUser/<int:id>',delete_TemporaryUser,name='delete_TemporaryUser'),
    path('delete_User/<int:id>',delete_User,name='delete_User'),
    path('add_InterviewRound',add_InterviewRound, name='add_InterviewRound'),
    path('delete_InterviewRound/<int:id>',delete_InterviewRound, name='delete_InterviewRound'),
    path('edit_InterviewRound',edit_InterviewRound, name='edit_InterviewRound'),
    path('add_ScorePattern',add_ScorePattern, name='add_ScorePattern'),
    path('add_ScoreTopic',add_ScoreTopic, name='add_ScoreTopic'),
    path('delete_ScoreTemplate/<int:id>',delete_ScoreTemplate, name='delete_ScoreTemplate'),
    path('delete_ScoreTopic/<int:id>',delete_ScoreTopic, name='delete_ScoreTopic'),
    path('edit_ScoreTopic',edit_ScoreTopic, name='edit_ScoreTopic'),
    path('View_ScoreTemplate/<int:id>',View_ScoreTopic, name='View_ScoreTopic'),
    path('edit_TemporaryUser',edit_TemporaryUser, name='edit_TemporaryUser'),
    path('add_TemporaryUser_by_file',add_TemporaryUser_by_file, name='add_TemporaryUser_by_file'),
    path('add_User',add_User, name='add_User'),
    path('add_User_by_file',add_User_by_file, name='add_User_by_file'),
    path('edit_User',edit_User, name='edit_User'),
    path('search_user',search_user, name='search_user'),
    path('search_TemporaryUser',search_TemporaryUser, name='search_TemporaryUser'),
    path('edit_password_in_profile',edit_password_in_profile, name='edit_password_in_profile'),
    path('add_Major_manager',add_Major_manager, name='add_Major_manager'),
    path('delete_manage_in_major',delete_manage_in_major, name='delete_manage_in_major'),
    path('delete_Announcement/<int:id>/',delete_Announcement, name='delete_Announcement'),
    path('delete_Schedule/<int:id>/',delete_Schedule, name='delete_Schedule'),
    path('addSchedule',addSchedule,name='addSchedule'),
    path('edit_Schedule',edit_Schedule,name='edit_Schedule'),

    


    #manage
    path('Manager_page/<int:id>/',manager_page, name='Manager_page'),
    path('manage_profile',manage_profile, name='manage_profile'),
    path('Manage_personnel',Manage_personnel, name='Manage_personnel'),
    path('Manager_Announcement',Manager_Announcement, name='Manager_Announcement'),
    path('Manager_interview',Manager_interview, name='Manager_interview'),
    path('Manager_Score',Manager_Score, name='Manager_Score'),
    path('Manager_Print_Interview',Manager_Print_Interview, name='Manager_Print_Interview'),
    path('Manager_Status',Manager_Status, name='Manager_Status'),
    path('toggle_round_active/<int:round_id>/', toggle_round_active, name='toggle_round_active'),
    path('toggle_status_active/<int:link_id>/', toggle_status_active, name='toggle_status_active'),
    path('chang_major', chang_major, name='chang_major'),
    path('Manage_User', Manage_User, name='Manage_User'),
    path('Manager_Score/<int:id>', Manager_ScoreTopic, name="Manager_ScoreTopic"),
    path('delete_User_in_manager',delete_User_in_manager,name='delete_User_in_manager'),
    path('add_announcement',add_announcement,name='add_announcement'),
    path('Manager_Status/<int:id>',Manager_StatusRound,name='Manager_StatusRound'),
    path('edit_Announcement',edit_Announcement,name='edit_Announcement'),
    path('decrease_manager',decrease_manager,name='decrease_manager'),
    path('increase_manager',increase_manager,name='increase_manager'),
    path('student_one_tocsv',student_one_tocsv,name='student_one_tocsv'),
    path('student_all_tocsv',student_all_tocsv,name='student_all_tocsv'),
    path('form_student_all',form_student_all,name='form_student_all'),
    path('form_student/<int:id>',form_student,name='form_student'),
    path('manager_edit_Schedule',manager_edit_Schedule,name='manager_edit_Schedule'),
    path('Manager_add_announcement',Manager_add_announcement,name='Manager_add_announcement'),
    path('Manager_add_Schedule',Manager_add_Schedule,name='Manager_add_Schedule'),
    path('Manager_edit_Announcement',Manager_edit_Announcement,name='Manager_edit_Announcement'),
    path('Manager_deledte_announcement/<int:id>',Manager_deledte_announcement,name='Manager_deledte_announcement'),
    path('manager_delete_Schedule/<int:id>',manager_delete_Schedule,name='manager_delete_Schedule'),
    path('Manager_data_investigator/<int:id>',Manager_data_investigator,name='Manager_data_investigator'),


    #Interviewer
    path('Interviewer_page',interviewer_page, name='Interviewer_page'),
    path('Interviewer_Profile',Interviewer_Profile, name='Interviewer_Profile'),
    path('Interviewer_room',Interviewer_room, name='Interviewer_room'),
    path('add_meetlink', add_meetlink, name="add_meetlink"),
    path('get-current-student/', get_current_student, name='get_current_student'),

    #Student
    path('Student_page',student_page, name='Student_page'),
    path('confirm_email',confirm_email, name='confirm_email'),
    path('Student_profile',Student_profile, name='Student_profile'),
    path('Student_register',Student_register, name='Student_register'),
    path('Student_room',Student_room, name='Student_room'),
    path('interview-status/', interview_status, name='interview_status'),
    path('Student_evidence',Student_evidence, name='Student_evidence'),
    path('register_interview/<int:round_id>/', register_interview, name='register_interview'),

    path('confirm_otp',confirm_otp, name='confirm_otp'),
    path('changepassword',changepassword, name='changepassword'),
    path('send_email_password',send_email_password, name='send_email_password'),



]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)