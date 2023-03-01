from django.urls import path
from .views import home, clean_media

app_name = 'core'

urlpatterns = [
    path('', home, name='home'),
    path('clean/',clean_media)
    
]