from django.shortcuts import render
from django.urls import reverse
import speech_recognition as sr 
import moviepy.editor as mp
from .helpers import handle_uploaded_file
import os
from pathlib import Path
from django.http import HttpResponse, Http404, HttpResponseRedirect


# Create your views here.
def home(request):
    projrect_dir = os.getcwd()
    token = str(request.COOKIES.get('csrftoken')).lower()
    
    if request.method == 'POST':
        try:
            uploaded_video = request.FILES.get('video')
            if not uploaded_video:
                return render(request,'home.html',context={'download':False,'error':True,'message':'Please upload a video file.'})
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
    
        
        
        



from django.http import FileResponse, HttpResponseBadRequest
from django.conf import settings

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
import platform
import time
def clean_media(request):
    print(2)
    folder = os.listdir('media/')
    for file in folder:

        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime)=os.stat(file)
        print(time.ctime(mtime))
        if platform.system() == 'Windows':
            print (os.path.getmtime(f'media/{file}'))
            # os.remove(f"media/{file}")
        else:
            stat = os.stat(f'media/{file}')
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime
    return HttpResponse('ok')
        
    
    