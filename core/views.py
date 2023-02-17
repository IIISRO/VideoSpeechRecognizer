from django.shortcuts import render
from django.urls import reverse
import speech_recognition as sr 
import moviepy.editor as mp
from .helpers import handle_uploaded_file
import os
from pathlib import Path
from django.http import HttpResponseRedirect

# Create your views here.
def home(request):
    projrect_dir = os.getcwd()
    token = request.COOKIES.get('csrftoken')
    # if os.path.exists(f'{projrect_dir}/media/2.mp4'):
    #     os.remove(f"{projrect_dir}/media/2.mp4")
    if request.method == 'POST':

        try:
            uploaded_video = request.FILES.get('video')
            if not uploaded_video:
                return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload video file.'})
            if  Path(uploaded_video.name).suffix == '.mp4' or  Path(uploaded_video.name).suffix == '.mov' or  Path(uploaded_video.name).suffix == '.m4a':
                handle_uploaded_file(uploaded_video,token)
                video = mp.VideoFileClip(f'{token}.mp4')
                video.audio.write_audiofile(f'{token}.wav')
                r = sr.Recognizer()
                audio = sr.AudioFile(f'{token}.wav')
                with audio as source:
                    r.adjust_for_ambient_noise(source)  
                    audio_file = r.record(source)
                text = r.recognize_google(audio_file,language=request.POST.get('lang'))
                
                with open(f'{token}.txt',mode ='w',encoding="utf-8") as file: 
                    file.write(text) 
                    
                os.chdir(projrect_dir)
                return render(request,'home.html', context={'download':True,'token':token, 'error':False})

            else:
                return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload only mp4, mov, m4a.'})
                    
        except:
            print('execept')
            os.chdir(projrect_dir)
            return render(request,'home.html',context={'download':False,'error':True,'message':'Somthing goes wrong. Try again.'})
        
    return render(request,'home.html',context={'download':False,'error':False})
    
        
        
        
        



