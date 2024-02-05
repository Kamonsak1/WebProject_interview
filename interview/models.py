from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractUser,UserManager,PermissionsMixin,AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from interview.models import User as User_M

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, google_login_id=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not username:
            raise ValueError('Username is required')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)

        try:
            user_google = User.objects.get(email=email)
            if user_google.is_active:
                return user_google
            else:
                return None
        except User.DoesNotExist:
            if username and password:
                user.save(using=self._db)
                return user
            else:
                return None

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password=password, **extra_fields)
    
    def authenticate_with_google(self, email):
        try:
            user = self.get(email=email)
            return user
        except self.model.DoesNotExist:
            return None


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True )#primary_key=True
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=400)
    postcode = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    citizen_id = models.CharField(max_length=13,unique=True,blank=True,null=True)
    birth_date = models.DateField(blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    prefix = models.CharField(max_length=20)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  
    EMAIL_FIELD = 'email' 
    REQUIRED_FIELDS = ['email']  

    def __str__(self):
        return f"ชื่อผู้ใช้: {self.username}"


    def can_login_with_email(self):
            return bool(self.email)

    @staticmethod
    def authenticate_with_google(email, ):
        User = get_user_model()
        return User.objects.authenticate_with_google(email=email,)

class report_temporaryUser(models.Model):
    citizen_id = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=128, blank=True)
    prefix = models.CharField(max_length=20,null=True, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True )
    round_name = models.CharField(max_length=20)

class TemporaryUser(models.Model):
    citizen_id = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    birth_date = models.DateField(default=timezone.now)
    password = models.CharField(max_length=128, blank=True)
    prefix = models.CharField(max_length=20,null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     birth_year = self.birth_date.year
    #     password = f"{self.birth_date.day:02d}{self.birth_date.month:02d}{birth_year}"
    #     self.password = password
    #     super(TemporaryUser, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



class Faculty(models.Model):
    faculty = models.CharField(max_length=100)
    users = models.ManyToManyField(User,blank=True)
    TemporaryUser = models.ManyToManyField(TemporaryUser , blank=True)

    def __str__(self) -> str:
        return f"{self.faculty}"

class Major(models.Model):
    major = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    default_manager = models.ManyToManyField(User, blank=True,related_name='manager')
    users = models.ManyToManyField(User,blank=True)
    TemporaryUser = models.ManyToManyField(TemporaryUser , blank=True)

    def __str__(self) -> str:
        return f"{self.major}"

class Role(models.Model):
    DEFAULT_ROLES = ['Admin', 'Manager','Interviewer', 'Student']
    
    name = models.CharField(max_length=50, default=DEFAULT_ROLES[0], choices=[(role, role) for role in DEFAULT_ROLES])
    users = models.ManyToManyField(User, related_name='roles', blank=True)
    TemporaryUser = models.ManyToManyField(TemporaryUser, related_name='roles', blank=True)

    def __str__(self):
        return self.name


class Round(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20) 
    round_name = models.CharField(max_length=20)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='round_user', blank=True)
    TemporaryUser = models.ManyToManyField(TemporaryUser,related_name='round_temp_user', blank=True)
    documents = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    interview_time = models.CharField(max_length=50)
    line_Token = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.round_name

class Schedule(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField()
    major = models.ManyToManyField(Major)
    round = models.ManyToManyField(Round)
    role = models.ManyToManyField(Role)
    schedule_name = models.CharField(max_length=200)
    schedule_content = models.TextField()

class Announcement(models.Model):
    post_date = models.DateField(default=datetime.now) 
    expire_date = models.DateField(null=True,blank=True)
    major = models.ManyToManyField(Major)
    round = models.ManyToManyField(Round)
    role = models.ManyToManyField(Role )
    title = models.CharField(max_length=200)
    announcement_content = models.TextField()

def user_directory_path(instance, filename):
    return 'Document/{0}/{1}'.format(instance.user.id, filename)
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=100)
    document = models.FileField(upload_to=user_directory_path)

class ScorePattern(models.Model):
    pattern_name = models.CharField(max_length=100)
    main_pattern = models.BooleanField(default=False)

class ScoreTopic(models.Model):
    pattern_id = models.ForeignKey(ScorePattern, on_delete=models.CASCADE, related_name="Score_pattern")
    topic_name = models.CharField(max_length=100)
    max_score = models.PositiveIntegerField()
    score_detail = models.CharField(max_length=500)

class Score(models.Model):
    topic = models.ForeignKey(ScoreTopic, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_score')
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_score')
    score = models.PositiveIntegerField()

class InterviewStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_status')
    status = models.CharField(max_length=100)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    reg_at = models.DateTimeField(auto_now_add=True)

class InterviewLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_link')
    link = models.CharField(max_length=300)
    active = models.BooleanField(default=False)
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name='interview_round')


class RoundScore(models.Model):
    pattern = models.ForeignKey(ScorePattern, on_delete=models.CASCADE)
    Round = models.ForeignKey(Round, on_delete=models.CASCADE)

class InterviewNow(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interview_student',blank=True,null=True)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviewer')