from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from .models import People, Chats
from django.db.models import Q
from django.http import HttpResponse
from . import util
import os

from datetime import datetime

@login_required
def home(request):
    people = People.objects.get(username=request.user.username)
    all_friends = people.friend.all()
    
    return render(request, 'home.html', {
        'username': request.user.username,
        'all_friends': all_friends
    })
    
def getLastNChats(request, n, friend_username):
    chats = {}
    if People.objects.filter(username=friend_username).exists():
        all_chats = Chats.objects.filter(Q(sender=request.user.username) | Q(sender=friend_username), 
                            Q(receiver=request.user.username) | Q(receiver=friend_username)).values()
        

        count = 0
        for item in all_chats:
            item['send_time'] = item['send_time'].strftime("%Y-%m-%d %H:%M")
            if item['receive_time']:
                item['receive_time'] = item['receive_time'].strftime("%Y-%m-%d %H:%M")

            if item['image']:
                item['image'] = os.path.join('media', item['image'])
            
            count += 1
            chats[count] = item

    
    return HttpResponse(json.dumps(chats))


def uploadImages(request):
    if request.method == 'POST':
        data = request.POST

        image_chats = {}
        count = 0

        receiver = data[util.receiver]
        msg = data[util.msg]
        for _img in request.FILES.getlist('CHAT_IMAGES'):
            chat = Chats(sender=request.user.username, receiver=receiver, message=msg, image=_img)
            chat.save()
            
            count += 1
            image_chats[count] = {
                'chat_id': chat.id,
                'image': chat.image.url
            }

        return HttpResponse(json.dumps(image_chats))

        
            
            