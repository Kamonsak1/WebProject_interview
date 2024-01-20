from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import Role, User ,Faculty,Major,Round
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
        users_stuedbt= [
            {'username': '6701920033','email': 'None','password': '6701920033','first_name':'นายธาราธร' ,'last_name':'บุญประดับ'},
            {'username': '6701920060','email': 'None','password': '6701920060','first_name':'นายพีรพัฒน์' ,'last_name':'หงษ์สินี'},
            {'username': '6701920106','email': 'None','password': '6701920106','first_name':'นายภาคิน' ,'last_name':'วิลามาศ'},
            {'username': '6701920208','email': 'None','password': '6701920208','first_name':'นายบัณฑิต' ,'last_name':'เพ็งเหล็ง'},
            {'username': '6701920235','email': 'None','password': '6701920235','first_name':'นายสุรเชษฐ์' ,'last_name':'สีสา'},
            {'username': '6701920279','email': 'None','password': '6701920279','first_name':'นายวงศธร' ,'last_name':'ธน.ยอด'},
            {'username': '6701920306','email': 'None','password': '6701920306','first_name':'นางสาวกันยาดา' ,'last_name':'ยุบล'},
            {'username': '6701920363','email': 'None','password': '6701920363','first_name':'นายประพุทธ์' ,'last_name':'คำคาวี'},
            {'username': '6701920441','email': 'None','password': '6701920441','first_name':'นายคาสึมะ' ,'last_name':'นันทรักษ์'},
            {'username': '6701920576','email': 'None','password': '6701920576','first_name':'นางสาวอาฐิรตา' ,'last_name':'รัตนกุล'},
            {'username': '6701920588','email': 'None','password': '6701920588','first_name':'นายคมชาญ' ,'last_name':'น้อยเนียม'},
            {'username': '6701920660','email': 'None','password': '6701920660','first_name':'นายเมธาวัช' ,'last_name':'กลิ่นเกษร'},
            {'username': '6701920854','email': 'None','password': '6701920854','first_name':'นายณัฏฐกิตติ์' ,'last_name':'คำเพาะ'},
            {'username': '6701920923','email': 'None','password': '6701920923','first_name':'นายธนากร' ,'last_name':'หนูมี'},
            {'username': '6701921137','email': 'None','password': '6701921137','first_name':'นายธนากร' ,'last_name':'ไชยรัตน์'},
            {'username': '6701921255','email': 'None','password': '6701921255','first_name':'นายธนพงษ์' ,'last_name':'สองสี'},
            {'username': '6701921305','email': 'None','password': '6701921305','first_name':'นางสาวกวิณชฎา' ,'last_name':'มีศรี'},
            {'username': '6701921355','email': 'None','password': '6701921355','first_name':'นายรัชชานนท์' ,'last_name':'รื่นจิตต์'},
            {'username': '6701921395','email': 'None','password': '6701921395','first_name':'นายวรินทร' ,'last_name':'เสริมศิริ'},
            {'username': '6701921506','email': 'None','password': '6701921506','first_name':'นายญาณพัทธ์' ,'last_name':'วงศ์ตา'},  
            {'username': '6701921556','email': 'None','password': '6701921556','first_name':'นายธนกฤต' ,'last_name':'ผวนชัยภูมิ'},
            {'username': '6701921558','email': 'None','password': '6701921558','first_name':'นายแอนโทนี่' ,'last_name':'ดูบัชนี'},
            {'username': '6701921680','email': 'None','password': '6701921680','first_name':'นายรพีวิชญ์' ,'last_name':'บุญเกื้อ'},
            {'username': '6701921798','email': 'None','password': '6701921798','first_name':'นางสาวพิยดา' ,'last_name':'รักษาเชื้อ'},
            {'username': '6701921924','email': 'None','password': '6701921506','first_name':'นายภัครพล' ,'last_name':'คำภู'},  
            {'username': '6701921960','email': 'None','password': '6701921960','first_name':'นายอัครชัย' ,'last_name':'พูลสวัสดิ์'},                         
        ]


        admin = ['64114540506','64114540025']
        r_ad,asd = Role.objects.get_or_create(name='Admin')
        r_ma,asd = Role.objects.get_or_create(name='Manager')
        r_in,asd = Role.objects.get_or_create(name='Interviewer')
        r_st,asd = Role.objects.get_or_create(name='Student')
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
                new_user_m.first_name = user['first_name']
                new_user_m.last_name = user['last_name']
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
