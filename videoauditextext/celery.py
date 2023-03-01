
from __future__ import absolute_import
import os
import platform
from django.conf import settings
from celery import shared_task
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'videoauditextext.settings')

celery_app = Celery('videoauditextext')
celery_app.config_from_object(settings, namespace='CELERY')
celery_app.autodiscover_tasks()

@celery_app.task(bind=True)
def hello():
    print ("This task is registering successfully")
    
    
@shared_task
def clean_media():
    folder = os.listdir('media/')
    print(2)
    # for file in folder:


    #     if platform.system() == 'Windows':
    #         print (os.path.getctime(f'media/{file}'))
    #         os.remove(f"media/{file}")
    #     else:
    #         stat = os.stat(f'media/{file}')
    #         try:
    #             return stat.st_birthtime
    #         except AttributeError:
    #             return stat.st_mtime
        
    
    