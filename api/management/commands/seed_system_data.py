from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Device, Pet, FeedingSchedule, FeedingLog
from datetime import time


class Command(BaseCommand):
    help = 'Seed the database with initial users, devices, pets, schedules, and logs.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing seeded records before creating new ones.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Resetting seeded data...')
            FeedingLog.objects.all().delete()
            FeedingSchedule.objects.all().delete()
            Pet.objects.all().delete()
            Device.objects.all().delete()
            User.objects.filter(username__in=['demo_user', 'admin']).delete()

        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={
                'email': 'demo@example.com',
            }
        )
        if created:
            demo_user.set_password('DemoPass123')
            demo_user.save()
            self.stdout.write('Created demo user: demo_user / DemoPass123')
        else:
            self.stdout.write('Demo user already exists: demo_user')

        admin_user, admin_created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if admin_created:
            admin_user.set_password('AdminPass123')
            admin_user.save()
            self.stdout.write('Created admin user: admin / AdminPass123')
        else:
            self.stdout.write('Admin user already exists: admin')

        devices_data = [
            {'name': 'Kitchen Feeder', 'location': 'Kitchen', 'status': 'active', 'ip_address': '192.168.1.10', 'mac_address': 'AA:BB:CC:DD:EE:01'},
            {'name': 'Living Room Feeder', 'location': 'Living Room', 'status': 'active', 'ip_address': '192.168.1.11', 'mac_address': 'AA:BB:CC:DD:EE:02'},
        ]

        devices = []
        for device_data in devices_data:
            device, created = Device.objects.get_or_create(
                owner=demo_user,
                name=device_data['name'],
                defaults=device_data,
            )
            devices.append(device)
            self.stdout.write('Created device: %s' % device.name if created else 'Device already exists: %s' % device.name)

        pets_data = [
            {'name': 'Max', 'breed': 'Golden Retriever', 'age': 4, 'weight': 28.0},
            {'name': 'Bella', 'breed': 'Siamese Cat', 'age': 2, 'weight': 4.2},
        ]

        pets = []
        for pet_data in pets_data:
            pet, created = Pet.objects.get_or_create(
                owner=demo_user,
                name=pet_data['name'],
                defaults=pet_data,
            )
            pets.append(pet)
            self.stdout.write('Created pet: %s' % pet.name if created else 'Pet already exists: %s' % pet.name)

        schedules_data = [
            {'pet': pets[0], 'device': devices[0], 'time': time(hour=8, minute=0), 'amount': 50.0, 'recurring': True},
            {'pet': pets[1], 'device': devices[1], 'time': time(hour=18, minute=0), 'amount': 30.0, 'recurring': True},
        ]

        schedules = []
        for schedule_data in schedules_data:
            schedule, created = FeedingSchedule.objects.get_or_create(
                pet=schedule_data['pet'],
                device=schedule_data['device'],
                time=schedule_data['time'],
                defaults={
                    'amount': schedule_data['amount'],
                    'recurring': schedule_data['recurring'],
                },
            )
            schedules.append(schedule)
            self.stdout.write('Created schedule: %s' % schedule if created else 'Schedule already exists: %s' % schedule)

        logs_data = [
            {'schedule': schedules[0], 'status': 'success', 'amount_dispensed': 50.0},
            {'schedule': schedules[1], 'status': 'success', 'amount_dispensed': 30.0},
            {'schedule': None, 'status': 'success', 'amount_dispensed': 25.0},
        ]

        for log_data in logs_data:
            if log_data['schedule']:
                log, created = FeedingLog.objects.get_or_create(
                    schedule=log_data['schedule'],
                    amount_dispensed=log_data['amount_dispensed'],
                    defaults={'status': log_data['status']},
                )
                self.stdout.write('Created scheduled log for: %s' % log.schedule if created else 'Scheduled log already exists for: %s' % log.schedule)
            else:
                log, created = FeedingLog.objects.get_or_create(
                    schedule=None,
                    amount_dispensed=log_data['amount_dispensed'],
                    defaults={'status': log_data['status']},
                )
                self.stdout.write('Created manual feed log' if created else 'Manual feed log already exists')

        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))
