from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize SpellChecker with a custom Mongolian word list
spell = SpellChecker(language=None)

try:
    spell.word_frequency.load_text_file('mongolian_words.txt')  # Adjust path to actual file location
except FileNotFoundError:
    logger.error("Mongolian word list file not found. Please check the file path.")
except Exception as e:
    logger.error(f"An error occurred while loading the word list: {e}")

@csrf_exempt
def spell_check_view(request):
    suggestions = {}
    text = ""
    
    if request.method == 'POST':
        text = request.POST.get('text', '')  # Retrieve the text input
        words = text.split()  # Split text into individual words
        misspelled_words = spell.unknown(words)  # Find misspelled words

        # Generate suggestions for each misspelled word
        suggestions = {word: spell.correction(word) for word in misspelled_words}

    return render(request, 'index.html', {'text': text, 'suggestions': suggestions})
