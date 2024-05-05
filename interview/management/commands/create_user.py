from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import *
class Command(BaseCommand):
    help = 'Creates new superusers with Admin role'

    def handle(self, *args, **options):
        # Define the users to be created
        users_to_create = [
            {'username': 'wayo', 'email': 'user1@example.com', 'password': 'dcaamx','prefix':'อ.','first_name':'วาโย' ,'last_name':'ปุยะติ'},
            {'username': 'wichit', 'email': 'user2@example.com', 'password': 'egkzch','prefix':'ดร.','first_name':'วิชิต' ,'last_name':'สมบัติ'},
            {'username': 'wasana', 'email': 'user3@example.com', 'password': 'wvhscz','prefix':'อ.','first_name':'วาสนา' ,'last_name':'เหง้าเกษ'},
            {'username': 'kriengsak', 'email': 'user4@example.com', 'password': 'qsvoll','prefix':'ดร.','first_name':'เกรียงศักดิ์' ,'last_name':'ตรีประพิน'},
            {'username': 'chayaporn', 'email': 'user5@example.com', 'password': 'alfvcn','prefix':'ผศ.','first_name':'ชยาพร' ,'last_name':'แก่นสาร์'},
            {'username': 'wanarase', 'email': 'user6@example.com', 'password': 'zbpiwo','prefix':'อ.','first_name':'วันนเรศวร์' ,'last_name':'สิงหัษฐิต'},
            {'username': 'phaichayon', 'email': 'user7@example.com', 'password': 'kwgbdj','prefix':'ดร.','first_name':'ไพชยนต์' ,'last_name':'คงไชย'},
            {'username': 'supawadee', 'email': 'user8@example.com', 'password': 'xskhbf','prefix':'ผศ.ดร.','first_name':'สุภาวดี' ,'last_name':'หิรัญพงศ์สิน'},
            {'username': 'tossaporn', 'email': 'user9@example.com', 'password': 'qgwryt','prefix':'ดร.','first_name':'ทศพร' ,'last_name':'อเลิร์ป'},
            {'username': '64114540025', 'email': 'kamonsak.ba.64@ubu.ac.th', 'password': '1','prefix':'นาย','first_name':'กมลศักดิ์' ,'last_name':'บรรพตะธิ'},
            {'username': '64114540506', 'email': 'ronnapong.pi.64@ubu.ac.th', 'password': '1','prefix':'นาย','first_name':'รณพงษ์' ,'last_name':'ไพชยนต์'},
        ]
        users_stuedbt= [
            {'username': 'student1','email': 'None','password': 'student1','prefix':'นาย','first_name':'student' ,'last_name':'1'},      
            {'username': 'student2','email': 'None','password': 'student2','prefix':'นาย','first_name':'student' ,'last_name':'2'},                                   
        ]


        admin = ['64114540506','64114540025']
        r_ad,asd = Role.objects.get_or_create(name='Admin')
        r_ma,asd = Role.objects.get_or_create(name='Manager')
        r_in,asd = Role.objects.get_or_create(name='Interviewer')
        r_st,asd = Role.objects.get_or_create(name='Student')
        f,asd = Faculty.objects.get_or_create(faculty='วิทยาศาสตร์')
        m,ewqe = Major.objects.get_or_create(faculty=f,major='วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์')
        a = login_mode.objects.get_or_create(mode='0')
        for user in users_to_create:
            if not User.objects.filter(username=user['username']).exists():
                new_superuser = User.objects.create_superuser(
                    user['email'], 
                    user['username'],                    
                    user['password']
                )

                new_user_m, created = User.objects.get_or_create(username=user['username'])
                if new_user_m.username in admin:
                    new_user_m.is_staff = True
                else:
                    new_user_m.is_staff = False
                new_user_m.prefix = user['prefix']    
                new_user_m.first_name = user['first_name']
                new_user_m.last_name = user['last_name']
                new_user_m.first_name2 = user['first_name']
                new_user_m.last_name2 = user['last_name']
                new_user_m.save()
                f.users.add(new_user_m)
                m.users.add(new_user_m)
                r_ad.users.add(new_user_m)
                r_ma.users.add(new_user_m)
                r_in.users.add(new_user_m)
                r_st.users.add(new_user_m)

        # Save the roles
        f.save()
        m.save()
        r_ad.save()
        r_ma.save()
        r_in.save()
        r_st.save()


        manager_username = '64114540506'
        manager_instance = User.objects.get(username=manager_username)
        round_instance = Round.objects.create(
            major=m,
            academic_year='2567',
            round_name='DSSI Port2/67',
            manager=manager_instance,
            active=True 
        )
        #round,asd=Round.objects.get_or_create(round_name='DSSI Port2/67',academic_year='2567',manager__user__username='64114540506')
        for user in users_stuedbt:
            if not User.objects.filter(username=user['username']).exists():
                new_superuser = User.objects.create_superuser(
                    user['email'], 
                    user['username'],                    
                    user['password']
                )

                new_user_m, created = User.objects.get_or_create(username=user['username'])
                new_user_m.is_staff = False
                new_user_m.set_password(user['password'])
                new_user_m.prefix = user['prefix']  
                new_user_m.first_name = user['first_name']
                new_user_m.last_name = user['last_name']
                new_user_m.first_name2 = user['first_name']
                new_user_m.last_name2 = user['last_name']
                new_user_m.citizen_id = user['username']
                new_user_m.save()
                f.users.add(new_user_m)
                m.users.add(new_user_m)
                r_st.users.add(new_user_m)
                round_instance.users.add(new_user_m)
                #round.users.add(new_user_m)

        # Save the roles
        #round.save()
        round_instance.save()
        f.save()
        m.save()
        r_st.save()

        self.stdout.write(self.style.SUCCESS('Successfully created specified super users with Admin role'))
