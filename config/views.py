from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging


logger = logging.getLogger(__name__)


spell = SpellChecker(language=None)

try:
    spell.word_frequency.load_text_file('mongolian_words.txt') 
except FileNotFoundError:
    logger.error("Mongolian word list file not found. Please check the file path.")
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
