from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import FeedingSchedule, FeedingLog

class Command(BaseCommand):
    help = 'Check for scheduled feedings and trigger them'

    def handle(self, *args, **options):
        now = timezone.now()
        current_time = now.time().replace(second=0, microsecond=0)  # Ignore seconds for matching

        # Find schedules that match current time and are recurring or one-time
        schedules = FeedingSchedule.objects.filter(time=current_time)

        for schedule in schedules:
            # Check if already fed today (for recurring, to avoid multiple feeds per day)
            today_logs = FeedingLog.objects.filter(
                schedule=schedule,
                timestamp__date=now.date()
            )
            if not today_logs.exists():
                # Trigger feed
                log = FeedingLog.objects.create(
                    schedule=schedule,
                    status='success',
                    amount_dispensed=schedule.amount
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Fed {schedule.pet.name} via {schedule.device.name} at {schedule.time} - Log ID: {log.id}')
                )
            else:
                self.stdout.write(f'Schedule {schedule.id} already fed today')