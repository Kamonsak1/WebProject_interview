from django.contrib import admin
from interview.models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(User)
admin.site.register(TemporaryUser)
admin.site.register(Role)
# """admin.site.register(Faculty)
# admin.site.register(Major)
# admin.site.register(InterviewRound)
# admin.site.register(Schedule)
# admin.site.register(Announcement)
# admin.site.register(Document)
# admin.site.register(InterviewScoreTopic)
# admin.site.register(Score)
# admin.site.register(InterviewStatus)"""