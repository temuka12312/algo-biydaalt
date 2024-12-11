import os
import re
import logging
from functools import lru_cache
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from spellchecker import SpellChecker
import traceback

logger = logging.getLogger(__name__)

spell = SpellChecker(language=None)

# Use absolute path to the dictionaries
mn_dic_path = os.path.join(os.path.dirname(__file__), 'mn.dic')
mn_aff_path = os.path.join(os.path.dirname(__file__), 'mn.aff')

try:
    spell.word_frequency.load_text_file(mn_dic_path)
    logger.info("mn.dic амжилттай ачааллаа.")

    spell.word_frequency.load_text_file(mn_aff_path)
    logger.info("mn.aff амжилттай ачааллаа.")
except FileNotFoundError as e:
    logger.error(f"Монгол хэлний толь бичгийн файл олдсонгүй: {e}")
except Exception as e:
    logger.error(f"Толь бичгийг ачаалахад алдаа гарлаа: {str(e)}")
    logger.error(f"Трасс: {traceback.format_exc()}")

def preprocess_text(text):
    """
    Текстийг урьдчилан боловсруулж үгсэд хуваах.
    1. Том үсгийг жижиг болгох.
    2. Тусгай тэмдэгтүүд болон тоог устгах.
    3. Үгсийг массив болгон буцаах.
    """
    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\d+', '', text)      
    words = text.split()
    return words

@lru_cache(maxsize=1000)
def cached_correction(word):
    # Тус үгийг "suggested" гэж тэмдэглэх эсвэл засаж болох өөрчлөлт хийж болно.
    return spell.correction(word)

@csrf_exempt
def spell_check_view(request):
    suggestions = {}
    text = ""

    if request.method == 'POST':
        text = request.POST.get('text', '') 
        words = preprocess_text(text)
        misspelled_words = spell.unknown(words)

        for word in misspelled_words:
            suggested_word = cached_correction(word)
            # Засваруудыг сайтар шалгах, илүү тохиромжтой үгс санал болгох
            suggestions[word] = suggested_word

    return render(request, 'index.html', {
        'text': text,
        'suggestions': suggestions
    })

def about(request):
    return render(request, 'about.html')
