from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
import json

from .models import Chat


def index(request):
    return render(request, 'chat/index.html', {})


class RoomView(generic.TemplateView):
    model = Chat
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        try:
            chat_list = Chat.objects.filter(book_id=self.kwargs.get('room_name'))
            chat_msg_list = list()
            for chat in chat_list:
                chat_msg_list.append(chat.message)
        except ObjectDoesNotExist:
            chat_msg_list = list()
        return {
            'room_name': self.kwargs.get('room_name'),
            'user_name': mark_safe(json.dumps(self.request.user.username)),
            'room_name_json': mark_safe(json.dumps(self.kwargs.get('room_name'))),
            'chat_msg_list': mark_safe(json.dumps(chat_msg_list)),
        }


def send_msg(request, room_name):
    message = '[' + request.user.username + ']: '
    message += request.POST['msg']
    Chat.objects.create(book_id=room_name, message=message)

    return redirect('chat:room', room_name)
