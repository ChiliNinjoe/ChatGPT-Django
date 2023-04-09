from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import openai

import os

from markdown2 import Markdown

def chat(request):
    if request.method == 'POST':
        if request.POST.get('action')== 'clear':
            del request.session['chat_messages']
    
    if 'chat_messages' in request.session:
        chats = request.session["chat_messages"]
    else:
        chats = [
            {"role": "system", "content": settings.CHAT_SYSTEM_MESSAGES[int(os.getenv('SYSTEM_MESSAGE_INDEX',0))]},
        ]
        request.session["chat_messages"] = chats

    context = {
        'chats': chats,
        'pagetitle': settings.APP_TITLE
    }
    return render(request, 'chat.html', context)


@csrf_exempt
def Ajax(request):
    # Check if request is Ajax
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        text = request.POST.get('text')
        # print(text)
        request.session["chat_messages"].append(
            {"role": "user", "content": text})

        openai.api_key = os.environ["OPENAI_API_KEY"]
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=request.session["chat_messages"]
        )

        response = res.choices[0].message
        ai_message = response["content"]
        # print(ai_message)
        request.session["chat_messages"].append(response)
        request.session.modified = True

        markdowner = Markdown(extras=["fenced-code-blocks"])
        return JsonResponse({'data': markdowner.convert(ai_message), })
    return JsonResponse({})
