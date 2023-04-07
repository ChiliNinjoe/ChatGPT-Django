from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai

import os

from markdown2 import Markdown

def chat(request):
    if 'chat_messages' in request.session:
        chats = request.session["chat_messages"]
    else:
        chats = [
            {"role": "system", "content": "The following is a friendly conversation between a human and an AI. The AI is talkative and provides lots of specific details from its context. If the AI does not know the answer to a question, it truthfully says it does not know."},
        ]
        request.session["chat_messages"] = chats

    return render(request, 'chat.html', {
        'chats': chats,
    })


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
