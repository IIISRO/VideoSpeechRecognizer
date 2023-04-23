
from celery import shared_task
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from core.models import Media
import os
@shared_task
def clean_media():
    for media in Media.objects.all():
        now = datetime.now(timezone.utc)
        delta = relativedelta(now,media.created_at)
        if delta.hours >= 1:
            print('Cleaning media files...')
            media.delete()
    