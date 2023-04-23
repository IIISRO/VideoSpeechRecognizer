import os
from django.shortcuts import render
import speech_recognition as sr 
import moviepy.editor as mp
from django.core.files import File
from .models import Media
from pathlib import Path
import pytube
import textwrap

# from django.urls import reverse
# from .helpers import handle_uploaded_file
# from django.http import HttpResponse, Http404, HttpResponseRedirect
# from django.conf import settings
# from moviepy.editor import AudioFileClip
# from django.http import HttpResponse, FileResponse, HttpResponseBadRequest
# import platform
# import time

# Create your views here.
def home(request):
    if request.method == 'POST':
        token = str(request.COOKIES.get('csrftoken')).lower()
        
        
        try:
            uploadfrom = request.POST.get('uploadfrom')
            if uploadfrom == 'device':
                uploaded_video = request.FILES.get('video')
                if not uploaded_video:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload a video file.'})
                if  Path(uploaded_video.name).suffix == '.mp4' or  Path(uploaded_video.name).suffix == '.mov' or  Path(uploaded_video.name).suffix == '.m4a':
                    if uploaded_video.size // 1024 // 1024 > 100:
                        return render(request,'home.html',context={'download':False,'error':True,'message':'Please select less than 100MB'})    
                
                    media = Media.objects.create( video = uploaded_video )

                    video = mp.VideoFileClip(f'media/{media.video.name}')
                    video.audio.write_audiofile(f'media/audio/{token}.wav')
                    
            
                        
                    audio = sr.AudioFile(f'media/audio/{token}.wav')
                    
                    r = sr.Recognizer()
                    with audio as source:
                        r.adjust_for_ambient_noise(source)  
                        audio_file = r.record(source)
                    text = r.recognize_google(audio_file,language=request.POST.get('lang'))
                    print(text)
                    with open(f'media/text/{token}.txt',mode ='w',encoding="utf-8") as file: 
                        wrapped = textwrap.fill(text, 100)
                        file.write(wrapped)
                        
                    audio_file = open(f'media/audio/{token}.wav', 'rb')
                    media.audio = File(audio_file)
                    media.audio.name = f'{uploaded_video.name.split(".")[0]}.wav'
                    media.save()
                    audio_file.close()
                    os.remove(f'media/audio/{token}.wav')
                    
                    text_file = open(f'media/text/{token}.txt', 'rb')
                    media.text = File(text_file)
                    media.text.name = f'{uploaded_video.name.split(".")[0]}.txt'
                    media.save()
                    text_file.close()
                    os.remove(f'media/text/{token}.txt')
                    
                    
                    return render(request,'home.html', context={'download':True,'file':Media.objects.get(video = media.video), 'error':False})
            
                else:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload only mp4, mov, m4a.'})
            elif uploadfrom == 'youtube':
                ytlink = request.POST.get('video')
                if not ytlink:
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please paste the video url.'})
                else:
                    video = pytube.YouTube(ytlink)
                    print(video)
                    
                if int(video.length) > int(300) :
                    return render(request,'home.html',context={'download':False,'error':True,'message':'Please select less than 5 minute'})
                else:    
                    video.streams.filter(progressive=True, file_extension='mp4').get_lowest_resolution().download('media/video',filename=f'{token}.mp4')
                    with open(f'media/video/{token}.mp4', mode='rb') as video_file:
                        
                        media = Media(video = File(video_file))
                        media.video.name = f'{video.title}.mp4'
                        media.save()
                    os.remove(f'media/video/{token}.mp4')
                    
                    
                    mpvideo = mp.VideoFileClip(f'media/{media.video.name}')
                    mpvideo.audio.write_audiofile(f'media/audio/{token}.wav')
                    
            
                        
                    audio = sr.AudioFile(f'media/audio/{token}.wav')
                    
                    r = sr.Recognizer()
                    with audio as source:
                        r.adjust_for_ambient_noise(source)  
                        audio_file = r.record(source)
                    text = r.recognize_google(audio_file,language=request.POST.get('lang'))
                    
                    with open(f'media/text/{token}.txt',mode ='w',encoding="utf-8") as file: 
                        wrapped = textwrap.fill(text, 100)
                        file.write(wrapped)
                        
    
                        
                    audio_file = open(f'media/audio/{token}.wav', 'rb')
                    media.audio = File(audio_file)
                    media.audio.name = f'{video.title}.wav'
                    media.save()
                    audio_file.close()
                    os.remove(f'media/audio/{token}.wav')
                    
                    text_file = open(f'media/text/{token}.txt', 'rb')
                    media.text = File(text_file)
                    media.text.name = f'{video.title}.txt'
                    media.save()
                    text_file.close()
                    os.remove(f'media/text/{token}.txt')
                    return render(request,'home.html', context={'download':True,'file':Media.objects.get(video = media.video), 'error':False})
        except:
            print('execept')
            return render(request,'home.html',context={'download':False,'error':True,'message':'Somthing goes wrong. Try again.'})
        
    return render(request,'home.html',context={'download':False,'error':False})
    
        
        
        




# def download_media(request, token):
#     if os.getcwd() != 'C:\\Users\\Ilgar Shukuroff\\Desktop\\VideoSpeechRecognizer\\media':
#         projrect_dir = os.getcwd()
#         os.chdir(f"{projrect_dir}/media")
#     media_file = open(f'{token}.wav', 'rb')
#     response = FileResponse(media_file)
#     response['Content-Disposition'] = f'attachment; filename="{token}.wav"'

#     if 'HTTP_RANGE' in request.META:
#         # The request includes a Range header
#         range_header = request.META['HTTP_RANGE']
#         bytes_range = range_header.replace('bytes=', '').split('-')
#         start_byte = int(bytes_range[0])
#         end_byte = int(bytes_range[1]) if bytes_range[1] else None

     
        
#         if end_byte is not None and end_byte < media_file - 1:
#             # The client requested a partial download
#             response['Content-Length'] = end_byte - start_byte + 1
#             response['Content-Range'] = 'bytes {}-{}/{}'.format(start_byte, end_byte, media_file.size)
#             response.status_code = 206  # Partial Content
#         elif end_byte is None or end_byte == media_file.size - 1:
#             # The client requested the entire file
#             response['Content-Length'] = media_file.size
#             if settings.DEBUG:
#                 print("File downloaded completely. Deleting file...")
#             media_file.delete()  # Delete the file from the server
#         else:
#             # The client requested an invalid range
#             return HttpResponseBadRequest('Invalid Range header')
#     else:
#         media_file_stat = os.stat(f'{os.getcwd()}/{token}.wav')
#         # The client requested the entire file
#         response['Content-Length'] = media_file_stat.st_size
        
#         print("File downloaded completely. Deleting file...")
#         # media_file.close()
#         # if os.path.exists(f'{projrect_dir}/media/{token}.wav'):
#         #     os.remove(f"{projrect_dir}/media/{token}.wav")
#         #dict deyis refersh duzeld silinmeyin ele
#     return response


# def clean_media(request):
#     print(2)
#     folder = os.listdir('media/')
#     for file in folder:

#         (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)=os.stat(file)
#         print(time.ctime(mtime))
#         if platform.system() == 'Windows':
#             print (os.path.getmtime(f'media/{file}'))
#             # os.remove(f"media/{file}")
#         else:
#             stat = os.stat(f'media/{file}')
#             try:
#                 return stat.st_birthtime
#             except AttributeError:
#                 return stat.st_mtime
#     return HttpResponse('ok')
        
    
    