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
            {'username': '6701920033','email': 'user10@gmail.com','password': 'mavnhb','prefix':'นาย','first_name':'ธาราธร' ,'last_name':'บุญประดับ'},
            {'username': '6701920060','email': 'user11@gmail.com','password': 'qwdgyy','prefix':'นาย','first_name':'พีรพัฒน์' ,'last_name':'หงษ์สินี'},
            {'username': '6701920106','email': 'user12@gmail.com','password': 'owwfhm','prefix':'นาย','first_name':'ภาคิน' ,'last_name':'วิลามาศ'},
            {'username': '6701920208','email': 'user13@gmail.com','password': 'sqlkug','prefix':'นาย','first_name':'บัณฑิต' ,'last_name':'เพ็งเหล็ง'},
            {'username': '6701920235','email': 'user14@gmail.com','password': 'ejoimn','prefix':'นาย','first_name':'สุรเชษฐ์' ,'last_name':'สีสา'},
            {'username': '6701920279','email': 'user15@gmail.com','password': 'cnlyjm','prefix':'นาย','first_name':'วงศธร' ,'last_name':'ธน.ยอด'},
            {'username': '6701920306','email': 'user16@gmail.com ','password': 'wpkjar','prefix':'นางสาว','first_name':'กันยาดา' ,'last_name':'ยุบล'},
            {'username': '6701920363','email': 'user17@gmail.com','password': 'xbydcw','prefix':'นาย','first_name':'ประพุทธ์' ,'last_name':'คำคาวี'},
            {'username': '6701920441','email': 'user18@gmail.com','password': 'nnvali','prefix':'นาย','first_name':'คาสึมะ' ,'last_name':'นันทรักษ์'},
            {'username': '6701920576','email': 'user19@gmail.com','password': 'vainix','prefix':'นางสาว','first_name':'อาฐิรตา' ,'last_name':'รัตนกุล'},
            {'username': '6701920588','email': 'user20@gmail.com','password': 'jczlnz','prefix':'นาย','first_name':'คมชาญ' ,'last_name':'น้อยเนียม'},
            {'username': '6701920660','email': 'user21@gmail.com','password': 'uodqit','prefix':'นาย','first_name':'เมธาวัช' ,'last_name':'กลิ่นเกษร'},
            {'username': '6701920854','email': 'user22@gmail.com','password': 'ijheif','prefix':'นาย','first_name':'ณัฏฐกิตติ์' ,'last_name':'คำเพาะ'},
            {'username': '6701920923','email': 'user23@gmail.com','password': 'cxesvu','prefix':'นาย','first_name':'ธนากร' ,'last_name':'หนูมี'},
            {'username': '6701921137','email': 'user24@gmail.com','password': 'vkshms','prefix':'นาย','first_name':'ธนากร' ,'last_name':'ไชยรัตน์'},
            {'username': '6701921255','email': 'user25@gmail.com','password': 'crbscl','prefix':'นาย','first_name':'ธนพงษ์' ,'last_name':'สองสี'},
            {'username': '6701921305','email': 'user26@gmail.com','password': 'ygwkov','prefix':'นางสาว','first_name':'กวิณชฎา' ,'last_name':'มีศรี'},
            {'username': '6701921355','email': 'user27@gmail.com','password': 'zoecxs','prefix':'นาย','first_name':'รัชชานนท์' ,'last_name':'รื่นจิตต์'},
            {'username': '6701921395','email': 'user28@gmail.com','password': 'hppndq','prefix':'นาย','first_name':'วรินทร' ,'last_name':'เสริมศิริ'},
            {'username': '6701921506','email': 'user29@gmail.com','password': 'xepina','prefix':'นาย','first_name':'ญาณพัทธ์' ,'last_name':'วงศ์ตา'},  
            {'username': '6701921556','email': 'user30@gmail.com','password': 'cmikrw','prefix':'นาย','first_name':'ธนกฤต' ,'last_name':'ผวนชัยภูมิ'},
            {'username': '6701921558','email': 'user31@gmail.com','password': 'rriism','prefix':'นาย','first_name':'แอนโทนี่' ,'last_name':'ดูบัชนี'},
            {'username': '6701921680','email': 'user32@gmail.com','password': 'rtvbkw','prefix':'นาย','first_name':'รพีวิชญ์' ,'last_name':'บุญเกื้อ'},
            {'username': '6701921798','email': 'user33@gmail.com','password': 'dfcbyi','prefix':'นางสาว','first_name':'พิยดา' ,'last_name':'รักษาเชื้อ'},
            {'username': '6701921924','email': 'user34@gmail.com','password': 'pcmobb','prefix':'นาย','first_name':'ภัครพล' ,'last_name':'คำภู'},  
            {'username': '6701921960','email': 'user35@gmail.com','password': 'ktqopb','prefix':'นาย','first_name':'อัครชัย' ,'last_name':'พูลสวัสดิ์'}, 
            {'username': 'student1','email': 'None','password': 'student1','prefix':'นาย','first_name':'student' ,'last_name':'1'},      
            {'username': 'student2','email': 'None','password': 'student2','prefix':'นาย','first_name':'student' ,'last_name':'2'},   
            {'username': 'student3','email': 'None','password': 'student3','prefix':'นาย','first_name':'student' ,'last_name':'3'},   
            {'username': 'student4','email': 'None','password': 'student4','prefix':'นาย','first_name':'student' ,'last_name':'4'},   
            {'username': 'student5','email': 'None','password': 'student5','prefix':'นาย','first_name':'student' ,'last_name':'5'},   
            {'username': 'student6','email': 'None','password': 'student6','prefix':'นาย','first_name':'student' ,'last_name':'6'},   
            {'username': 'student7','email': 'None','password': 'student7','prefix':'นาย','first_name':'student' ,'last_name':'7'},   
            {'username': 'student8','email': 'None','password': 'student8','prefix':'นาย','first_name':'student' ,'last_name':'8'},   
            {'username': 'student9','email': 'None','password': 'student9','prefix':'นาย','first_name':'student' ,'last_name':'9'},   
            {'username': 'student10','email': 'None','password': 'student10','prefix':'นาย','first_name':'student' ,'last_name':'10'},   
            {'username': 'student11','email': 'None','password': 'student11','prefix':'นาย','first_name':'student' ,'last_name':'11'},   
            {'username': 'student12','email': 'None','password': 'student12','prefix':'นาย','first_name':'student' ,'last_name':'12'},   
            {'username': 'student13','email': 'None','password': 'student13','prefix':'นาย','first_name':'student' ,'last_name':'13'},   
            {'username': 'student14','email': 'None','password': 'student14','prefix':'นาย','first_name':'student' ,'last_name':'14'},   
            {'username': 'student15','email': 'None','password': 'student15','prefix':'นาย','first_name':'student' ,'last_name':'15'},   
            {'username': 'student16','email': 'None','password': 'student16','prefix':'นาย','first_name':'student' ,'last_name':'16'},                                  
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
