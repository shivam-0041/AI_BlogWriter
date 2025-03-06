from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth import authenticate,login,logout # type: ignore
from django.contrib.auth.decorators import login_required #type:ignore
from django.views.decorators.csrf import csrf_exempt #type:ignore
from django.http import JsonResponse #type:ignore
import json
import assemblyai as aai
from django.conf import settings
import os
from yt_dlp import YoutubeDL
from pytube.exceptions import PytubeError
import re
from .models import BlogPost
import google.generativeai as genai


@login_required
def home(request):
    return render(request, 'home.html',{})

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password) 
        if user is not None:
            login(request,user)
            user_name=username
            return redirect('home')
            
        else:
            error_message="Invalid username or password"
            return render(request,'login.html',{'error_message':error_message})
        
    return render(request,'login.html',{})

def user_signup(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['Confirmpassword']
        if password==cpassword:
            try:
                user=User.objects.create_user(username,email,password)
                user.save()
                login(request,user)
                return redirect(home)
            except:
                error_message='Error creating account'
                return render(request,'signup.html',{'error_message':error_message}) 
        else:
            error_message="Passwords do not match"
            return render(request,'signup.html',{'error_message':error_message})
    return render(request,'signup.html',{})


def download_audio(link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                #'ffmpeg_path':'\WebApp_AI\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
            info = ydl.extract_info(link, download=False)
            file_name = f"{info['title']}.mp3"
            file_name = re.sub(r'[<>:"/\\|*]', '_', file_name)
            return os.path.join(settings.MEDIA_ROOT, file_name)
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None



def generate_transcript(link):
    
    #audio = f"./media/{yt_title(link)}.mp3"
    audio=download_audio(link)
    try:
        aai.settings.api_key = "YOUR_API_KEY_HERE"
        transcriber = aai.Transcriber()
        config=aai.TranscriptionConfig(speaker_labels=True)
        transcript = transcriber.transcribe(audio,config)
        return transcript.text
    except Exception as e:
        print(f"Error generating transcript: {e}")
        return None

def generate_note_from_transcript(transcription):
    try:
        
        genai.configure(api_key="YOUR_API_KEY_HERE")
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"Based on the following transcript from a youtube video, write comprehensive notes, write it on base of transcript, but do not make it look like a youtube video, make it look like a proper notes so i can study for my exam, dont use bold characters or any type of highlighters keep it simple, 1 small para about each topic : \n\n {transcription}\n\nArticle:"
        response=model.generate_content(prompt)
        #generated_content = response.choices[0].text.strip()
        generated_content=response.text
        return generated_content
    except Exception as e:
        print(f"Error generating note: {e}")
        return None

def yt_title(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(settings.MEDIA_ROOT, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            #'ffmpeg_path':'\WebApp_AI\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        file_name = f"{info['title']}.mp3"
        file_name = re.sub(r'[<>:"/\\|*]', '_', file_name)
        return file_name
    #return video title for blog title and file address to remove from dir
    #under work

    
    

@csrf_exempt
def generate_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid Request'}, status=400)
        

        transcription = generate_transcript(yt_link)
        if not transcription:
            return JsonResponse({'error': "Failed to get transcript"}, status=500)

        text_content = generate_note_from_transcript(transcription)
        if not text_content:
            return JsonResponse({'error': "Failed to generate text"}, status=500)

        new_blog = BlogPost.objects.create(
            user=request.user,
            title=yt_title(yt_link),
            link=yt_link,
            content=text_content,
        )
        new_blog.save()
        os.remove(yt_title(yt_link))
        return JsonResponse({'content': text_content})
        

    else:
        return JsonResponse({'error': 'Invalid Request'}, status=405)
    

def all_texts(request):
    blog_articles = BlogPost.objects.filter(user=request.user)
    return render(request, 'all_texts.html', {'blog_articles': blog_articles})

def text_details(request, pk):
    blog_post = BlogPost.objects.get(id=pk)
    if request.user == blog_post.user:
        return render(request, 'text_details.html', {'blog_post': blog_post})
    else:
        return redirect('')

def user_logout(request):
    logout(request)
    return redirect('home')
