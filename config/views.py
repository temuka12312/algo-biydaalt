from django.shortcuts import render
import os
import json
import logging
from spellchecker import SpellChecker

from django.http import JsonResponse

from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class First(TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    

spell = SpellChecker(language=None)

mongolian_words = ["жишээ", "текст", "үнэ", "санал", "хүсэлт"]

spell.word_frequency.load_words(mongolian_words)  

@csrf_exempt
def spell_check(request):
    if request.method == "POST":
        text = request.POST.get("text", "")
        
        words = text.split()
        misspelled_words = {}

        for word in words:
            if not spell[word]: 
                suggestions = spell.candidates(word)
                misspelled_words[word] = list(suggestions)

        return JsonResponse({"misspelled_words": misspelled_words})

    return JsonResponse({"error": "Invalid request method"}, status=400)

