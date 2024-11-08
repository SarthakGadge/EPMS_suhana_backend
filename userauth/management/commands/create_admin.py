from django.core.management.base import BaseCommand
from django.utils import timezone
from userauth.models import CustomUser, Admin


class Command(BaseCommand):
    help = 'Create a single admin user and profile if it does not exist'

    def add_arguments(self, parser):
        # Add arguments for username, email, and password
        parser.add_argument('--username', type=str,
                            required=True, help='Username for the admin')
        parser.add_argument('--email', type=str,
                            required=True, help='Email for the admin')
        parser.add_argument('--password', type=str,
                            required=True, help='Password for the admin')

    def handle(self, *args, **options):
        # Extract the arguments
        username = options['username']
        email = options['email']
        password = options['password']

        # Check if an admin user already exists
        if CustomUser.objects.filter(role='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
        else:
            # Create the admin user
            admin_user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role='admin'
            )

            # Create the Admin profile
            Admin.objects.create(
                user=admin_user,
                full_name='System Admin',
                contact_number='1234567890',  # You can replace or add more fields if necessary
                joining_date=timezone.now().date(),
                gender='NA',
                emergency_contact='0987654321',
                dob='1990-01-01'
            )

            self.stdout.write(self.style.SUCCESS(
                'Admin user created successfully.'))
