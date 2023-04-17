from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Chat
from .forms import ChatForm
from django.contrib.auth.models import User
from actions.utils import create_action

@login_required
def chatroom(request, username):
    recipient = User.objects.get(username=username)
    
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = recipient
            chat.save()
           
            create_action(chat.sender, 'has sent you a message.')

            return redirect ('chatroom:chatbox', username=username)
    else:
        form = ChatForm()
    chats = Chat.objects.filter(sender=request.user, receiver=recipient) | Chat.objects.filter(sender=recipient, receiver=request.user)
    chats = chats.order_by('timestamp')
    context = {
        'form': form,
        'chats': chats,
        'recipient': recipient,
    }
    return render(request, 'chatbox/chat.html', context)
