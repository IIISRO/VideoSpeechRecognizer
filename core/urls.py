from django.urls import path
from django.conf.urls.static import static
from .views import home#, clean_media
from django.conf import settings

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    #path('clean/'   ,clean_media)
    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)