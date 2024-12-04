from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging
import os

logger = logging.getLogger(__name__)

spell = SpellChecker(language=None)

# Load the Mongolian dictionary files (mn.dic and mn.aff)
dic_path = os.path.join('mn.dic')
aff_path = os.path.join('mn.aff')

try:
    spell.word_frequency.load_text_file(dic_path)
    spell.word_frequency.load_text_file(aff_path)
except FileNotFoundError as e:
    logger.error(f"Mongolian dictionary file not found: {e}")
except Exception as e:
    logger.error(f"An error occurred while loading the word list: {e}")

@csrf_exempt
def spell_check_view(request):
    suggestions = {}
    text = ""
    
    if request.method == 'POST':
        text = request.POST.get('text', '') 
        words = text.split()  
        misspelled_words = spell.unknown(words)  

        suggestions = {word: spell.correction(word) for word in misspelled_words}

    return render(request, 'index.html', {'text': text, 'suggestions': suggestions})
