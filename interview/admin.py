from django.contrib import admin
from interview.models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(TemporaryUser)
admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(Role)
admin.site.register(Round)
admin.site.register(Schedule)
admin.site.register(Announcement)
admin.site.register(Document)
admin.site.register(Evidence)
admin.site.register(ScorePattern)
admin.site.register(ScoreTopic)
admin.site.register(Score)
admin.site.register(InterviewStatus) 
admin.site.register(InterviewLink)
admin.site.register(RoundScore)
admin.site.register(InterviewNow)
admin.site.register(report_temporaryUser)
admin.site.register(login_mode)