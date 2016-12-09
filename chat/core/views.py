from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import ChatMessage


# Create your views here.
def index(request):
    messages = ChatMessage.objects.filter(room="chat-dev2").order_by('-time')
    template = loader.get_template('core/index.html')
    context = {
        'messages': messages,
    }
    return HttpResponse(template.render(context, request))


def slides(request):
    template = loader.get_template('core/slides.html')
    return HttpResponse(template.render({}, request))