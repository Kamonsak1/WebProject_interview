from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import Role, User ,Faculty,Major,Round
class Command(BaseCommand):
    help = 'Creates new superusers with Admin role'

    def handle(self, *args, **options):
        # Define the users to be created
        users_to_create = [
            {'username': 'wayo', 'email': 'user1@example.com', 'password': 'dcaamx','first_name':'อ.วาโย' ,'last_name':'ปุยะติ'},
            {'username': 'wichit', 'email': 'user2@example.com', 'password': 'egkzch','first_name':'ดร.วิชิต' ,'last_name':'สมบัติ'},
            {'username': 'wasana', 'email': 'user3@example.com', 'password': 'wvhscz','first_name':'อ.วาสนา' ,'last_name':'เหง้าเกษ'},
            {'username': 'kriengsak', 'email': 'user4@example.com', 'password': 'qsvoll','first_name':'ดร.เกรียงศักดิ์' ,'last_name':'ตรีประพิน'},
            {'username': 'chayaporn', 'email': 'user5@example.com', 'password': 'alfvcn','first_name':'ผศ.ชยาพร' ,'last_name':'แก่นสาร์'},
            {'username': 'wanarase', 'email': 'user6@example.com', 'password': 'zbpiwo','first_name':'อ.วันนเรศวร์' ,'last_name':'สิงหัษฐิต'},
            {'username': 'phaichayon', 'email': 'user7@example.com', 'password': 'kwgbdj','first_name':'ดร.ไพชยนต์' ,'last_name':'คงไชย'},
            {'username': 'supawadee', 'email': 'user8@example.com', 'password': 'xskhbf','first_name':'ผศ.ดร.สุภาวดี' ,'last_name':'หิรัญพงศ์สิน'},
            {'username': 'tossaporn', 'email': 'user9@example.com', 'password': 'qgwryt','first_name':'ดร.ทศพร' ,'last_name':'อเลิร์ป'},
            {'username': '64114540025', 'email': 'kamonsak.ba.64@ubu.ac.th', 'password': 'qgwryt','first_name':'นายกมลศักดิ์' ,'last_name':'บรรพตะธิ'},
            {'username': '64114540506', 'email': 'ronnapong.pi.64@ubu.ac.th', 'password': 'hsumxh','first_name':'นายรณพงษ์' ,'last_name':'ไพชยนต์'},
        ]
        users_stuedbt= [
            {'username': '6701920033','email': 'taraton02548@gmail.com','password': 'mavnhb','first_name':'นายธาราธร' ,'last_name':'บุญประดับ'},
            {'username': '6701920060','email': 'Peerapathongsinee73@gmail.com','password': 'qwdgyy','first_name':'นายพีรพัฒน์' ,'last_name':'หงษ์สินี'},
            {'username': '6701920106','email': 'pakinwilamas@gmail.com','password': 'owwfhm','first_name':'นายภาคิน' ,'last_name':'วิลามาศ'},
            {'username': '6701920208','email': 'playeroneneon@gmail.com','password': 'sqlkug','first_name':'นายบัณฑิต' ,'last_name':'เพ็งเหล็ง'},
            {'username': '6701920235','email': 'surachet2421@gmail.com','password': 'ejoimn','first_name':'นายสุรเชษฐ์' ,'last_name':'สีสา'},
            {'username': '6701920279','email': 'duckyduckzy@gmail.com','password': 'cnlyjm','first_name':'นายวงศธร' ,'last_name':'ธน.ยอด'},
            {'username': '6701920306','email': 'kanyadayudon@gmail.com ','password': 'wpkjar','first_name':'นางสาวกันยาดา' ,'last_name':'ยุบล'},
            {'username': '6701920363','email': 'praput2057@gmail.com','password': 'xbydcw','first_name':'นายประพุทธ์' ,'last_name':'คำคาวี'},
            {'username': '6701920441','email': 'iamshadowfu@gmail.com','password': 'nnvali','first_name':'นายคาสึมะ' ,'last_name':'นันทรักษ์'},
            {'username': '6701920576','email': '548athirata@gmail.com','password': 'vainix','first_name':'นางสาวอาฐิรตา' ,'last_name':'รัตนกุล'},
            {'username': '6701920588','email': 'komcha0829396277@gmail.com','password': 'jczlnz','first_name':'นายคมชาญ' ,'last_name':'น้อยเนียม'},
            {'username': '6701920660','email': 'wami3423@gmail.com','password': 'uodqit','first_name':'นายเมธาวัช' ,'last_name':'กลิ่นเกษร'},
            {'username': '6701920854','email': 'utkam447@gmail.com','password': 'ijheif','first_name':'นายณัฏฐกิตติ์' ,'last_name':'คำเพาะ'},
            {'username': '6701920923','email': 'gun9443@gmail.com','password': 'cxesvu','first_name':'นายธนากร' ,'last_name':'หนูมี'},
            {'username': '6701921137','email': 'boomafk33@gmail.com','password': 'vkshms','first_name':'นายธนากร' ,'last_name':'ไชยรัตน์'},
            {'username': '6701921255','email': 'filmgghannae@gmail.com','password': 'crbscl','first_name':'นายธนพงษ์' ,'last_name':'สองสี'},
            {'username': '6701921305','email': 'kawinchada.ploy@gmail.com','password': 'ygwkov','first_name':'นางสาวกวิณชฎา' ,'last_name':'มีศรี'},
            {'username': '6701921355','email': 'beembeew.3115@gmail.com','password': 'zoecxs','first_name':'นายรัชชานนท์' ,'last_name':'รื่นจิตต์'},
            {'username': '6701921395','email': 'yodsapoul.2548@gmail.com','password': 'hppndq','first_name':'นายวรินทร' ,'last_name':'เสริมศิริ'},
            {'username': '6701921506','email': 'yanaphatwongta2@gmail.com','password': 'xepina','first_name':'นายญาณพัทธ์' ,'last_name':'วงศ์ตา'},  
            {'username': '6701921556','email': 'darkfourz@gmail.com','password': 'cmikrw','first_name':'นายธนกฤต' ,'last_name':'ผวนชัยภูมิ'},
            {'username': '6701921558','email': 'antony9876502@gmail.com','password': 'rriism','first_name':'นายแอนโทนี่' ,'last_name':'ดูบัชนี'},
            {'username': '6701921680','email': 'rapeewit2548@gmail.com','password': 'rtvbkw','first_name':'นายรพีวิชญ์' ,'last_name':'บุญเกื้อ'},
            {'username': '6701921798','email': 'phiyada122005@gmail.com','password': 'dfcbyi','first_name':'นางสาวพิยดา' ,'last_name':'รักษาเชื้อ'},
            {'username': '6701921924','email': 'tonnamsocial2549@gmail.com','password': 'pcmobb','first_name':'นายภัครพล' ,'last_name':'คำภู'},  
            {'username': '6701921960','email': 'Akkharac123@gmail.com','password': 'ktqopb','first_name':'นายอัครชัย' ,'last_name':'พูลสวัสดิ์'}, 
            {'username': 'student1','email': 'None','password': 'student1','first_name':'student' ,'last_name':'1'},      
            {'username': 'student2','email': 'None','password': 'student2','first_name':'student' ,'last_name':'2'},   
            {'username': 'student3','email': 'None','password': 'student3','first_name':'student' ,'last_name':'3'},   
            {'username': 'student4','email': 'None','password': 'student4','first_name':'student' ,'last_name':'4'},   
            {'username': 'student5','email': 'None','password': 'student5','first_name':'student' ,'last_name':'5'},   
            {'username': 'student6','email': 'None','password': 'student6','first_name':'student' ,'last_name':'6'},   
            {'username': 'student7','email': 'None','password': 'student7','first_name':'student' ,'last_name':'7'},   
            {'username': 'student8','email': 'None','password': 'student8','first_name':'student' ,'last_name':'8'},   
            {'username': 'student9','email': 'None','password': 'student9','first_name':'student' ,'last_name':'9'},   
            {'username': 'student10','email': 'None','password': 'student10','first_name':'student' ,'last_name':'10'},   
            {'username': 'student11','email': 'None','password': 'student11','first_name':'student' ,'last_name':'11'},   
            {'username': 'student12','email': 'None','password': 'student12','first_name':'student' ,'last_name':'12'},   
            {'username': 'student13','email': 'None','password': 'student13','first_name':'student' ,'last_name':'13'},   
            {'username': 'student14','email': 'None','password': 'student14','first_name':'student' ,'last_name':'14'},   
            {'username': 'student15','email': 'None','password': 'student15','first_name':'student' ,'last_name':'15'},   
            {'username': 'student16','email': 'None','password': 'student16','first_name':'student' ,'last_name':'16'},                                  
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
