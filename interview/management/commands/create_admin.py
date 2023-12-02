from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from interview.models import Role,User as User_M

class Command(BaseCommand):
    help = 'Creates a new superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@ubu.ac.th', 'admin')
            new_user = User_M.objects.get(username='admin')
            R_Ad = Role.objects.get(name='Admin')
            R_Mn = Role.objects.get(name='Manager')
            R_Iv = Role.objects.get(name='Interviewer')
            R_Ad.users.add(new_user)
            R_Mn.users.add(new_user)
            R_Iv.users.add(new_user)
            R_Ad.save()
            R_Mn.save()
            R_Iv.save()
            self.stdout.write(self.style.SUCCESS('Successfully created "admin" super user'))