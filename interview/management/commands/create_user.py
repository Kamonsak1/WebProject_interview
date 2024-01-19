from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import Role, User ,Faculty,Major
class Command(BaseCommand):
    help = 'Creates new superusers with Admin role'

    def handle(self, *args, **options):
        # Define the users to be created
        users_to_create = [
            {'username': 'wayo', 'email': 'user1@example.com', 'password': 'wayo','first_name':'อ.วาโย' ,'last_name':'ปุยะติ'},
            {'username': 'wichit', 'email': 'user2@example.com', 'password': 'wichit','first_name':'ดร.วิชิต' ,'last_name':'สมบัติ'},
            {'username': 'wasana', 'email': 'user3@example.com', 'password': 'wasana','first_name':'อ.วาสนา' ,'last_name':'เหง้าเกษ'},
            {'username': 'kriengsak', 'email': 'user4@example.com', 'password': 'kriengsak','first_name':'ดร.เกรียงศักดิ์' ,'last_name':'ตรีประพิน'},
            {'username': 'chayaporn', 'email': 'user5@example.com', 'password': 'chayaporn','first_name':'ผศ.ชยาพร' ,'last_name':'แก่นสาร์'},
            {'username': 'wanarase', 'email': 'user6@example.com', 'password': 'wanarase','first_name':'อ.วันนเรศวร์' ,'last_name':'สิงหัษฐิต'},
            {'username': 'phaichayon', 'email': 'user7@example.com', 'password': 'phaichayon','first_name':'ดร.ไพชยนต์' ,'last_name':'คงไชย'},
            {'username': 'supawadee', 'email': 'user8@example.com', 'password': 'supawadee','first_name':'ผศ.ดร.สุภาวดี' ,'last_name':'หิรัญพงศ์สิน'},
            {'username': 'tossaporn', 'email': 'user9@example.com', 'password': 'tossaporn','first_name':'ดร.ทศพร' ,'last_name':'อเลิร์ป'},
            {'username': '64114540025', 'email': 'kamonsak.ba.64@ubu.ac.th', 'password': '64114540025','first_name':'นายกมลศักดิ์' ,'last_name':'บรรพตะธิ'},
            {'username': '64114540506', 'email': 'ronnapong.pi.64@ubu.ac.th', 'password': '64114540506','first_name':'นายรณพงษ์' ,'last_name':'ไพชยนต์'},
        ]

        admin = ['64114540506','64114540025']
        r_ad = Role.objects.get_or_create(name='Admin')
        r_ma = Role.objects.get_or_create(name='Manager')
        r_in = Role.objects.get_or_create(name='Interviewer')
        r_st = Role.objects.get_or_create(name='Student')
        f,asd = Faculty.objects.get_or_create(faculty='วิทยาศาสตร์')
        m,ewqe = Major.objects.get_or_create(faculty=f,major='วิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์')
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
                new_user_m.first_name = user['first_name']
                new_user_m.last_name = user['last_name']
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


        self.stdout.write(self.style.SUCCESS('Successfully created specified super users with Admin role'))
