from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.models import AbstractUser,UserManager,PermissionsMixin,AbstractBaseUser,BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model

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
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    address = models.CharField(max_length=400)
    postcode = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=10)
    citizen_id = models.CharField(max_length=13)
    birth_date = models.DateField(blank=True,null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    objects = CustomUserManager()

    USERNAME_FIELD = 'username'  # แก้ให้ USERNAME_FIELD เป็น 'email' แทน
    EMAIL_FIELD = 'email'  # แก้ให้ EMAIL_FIELD เป็น 'email' แทน
    REQUIRED_FIELDS = ['email']  # ไม่ต้องระบุใน REQUIRED_FIELDS แล้ว

    def __str__(self):
        return f"ชื่อผู้ใช้: {self.username}"


    def can_login_with_email(self):
            return bool(self.email)

    @staticmethod
    def authenticate_with_google(email, ):
        User = get_user_model()
        return User.objects.authenticate_with_google(email=email,)






class TemporaryUser(models.Model):
    citizen_id = models.CharField(max_length=13, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    password = models.CharField(max_length=10, blank=True)

    def save(self, *args, **kwargs):
        thai_birth_date_str = self.birth_date.strftime('%d/%m/%Y')  
        self.password = thai_birth_date_str
        super().save(*args, **kwargs)



class Faculty(models.Model):
    faculty = models.CharField(max_length=100)

class Major(models.Model):
    major = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    default_manager = models.ForeignKey(User, on_delete=models.CASCADE)

class Role(models.Model):
    DEFAULT_ROLES = ['Admin', 'Manager','Interviewer', 'Student']
    
    name = models.CharField(max_length=50, default=DEFAULT_ROLES[0], choices=[(role, role) for role in DEFAULT_ROLES])
    users = models.ManyToManyField(User, related_name='roles')

    def __str__(self):
        return self.name


class Round(models.Model):
    major = models.ForeignKey(Major, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=20) 
    round_name = models.CharField(max_length=20)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='rounds_participated')

class Schedule(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    schedule_name = models.CharField(max_length=200)
    schedule_content = models.TextField()

class Announcement(models.Model):
    post_date = models.DateField(default=datetime.now) 
    expire_date = models.DateField()
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    announcement_content = models.TextField()

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    document = models.CharField(max_length=200)

class ScoreTopic(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    pattern_id = models.CharField(max_length=100)
    topic_name = models.CharField(max_length=100)
    max_score = models.PositiveIntegerField()

class Score(models.Model):
    topic = models.ForeignKey(ScoreTopic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()

class InterviewStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    round = models.ForeignKey(Round, on_delete=models.CASCADE)

class InterviewLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=300)
