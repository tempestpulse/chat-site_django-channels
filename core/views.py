from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from core.models import Message


@login_required
def index(request):
    users = User.objects.exclude(username=request.user.username)
    return render(request, "core/index.html", context={'users': users})


@login_required
def chat_page(request, username):
    user_obj = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > user_obj.id:
        title = f'{request.user.id}-{user_obj.id}'
    else:
        title = f'{user_obj.id}-{request.user.id}'
    message_objs = Message.objects.filter(title=title)
    return render(request, 'core/chat_page.html', context={'user': user_obj, 'users': users, 'messages': message_objs})
