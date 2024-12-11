from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging
import os
from functools import lru_cache
from django.http import JsonResponse
import re

def ping(request):
    data = {}
    data['build_mode'] = os.environ.get("BUILD_MODE")
    data['build_date'] = os.environ.get("BUILD_DATE")
    data['version'] = os.environ.get("IMAGE_VERSION")
    data['app'] = "core"
    return JsonResponse(data)

logger = logging.getLogger(__name__)

spell = SpellChecker(language=None)

mn_dic_path = os.path.join('mn.dic')
mn_aff_path = os.path.join('mn.aff')

try:
    spell.word_frequency.load_text_file(mn_dic_path)
    logger.info("mn.dic амжилттай ачааллаа.")

    spell.word_frequency.load_text_file(mn_aff_path)
    logger.info("mn.aff амжилттай ачааллаа.")
except FileNotFoundError as e:
    logger.error(f"Монгол хэлний толь бичгийн файл олдсонгүй: {e}")
except Exception as e:
    logger.error(f"Толь бичгийг ачаалахад алдаа гарлаа: {e}")

def preprocess_text(text):
    """
    Текстийг урьдчилан боловсруулж үгсэд хуваах.
    1. Том үсгийг жижиг болгох.
    2. Тусгай тэмдэгтүүд болон тоог устгах.
    3. Үгсийг массив болгон буцаах.
    """
    text = text.lower()

    text = re.sub(r'[^\w\s]', '', text)  
    text = re.sub(r'\d+', '', text)      

    words = text.split()

    return words

@lru_cache(maxsize=1000)
def cached_correction(word):
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
            suggestions[word] = cached_correction(word)

    return render(request, 'index.html', {
        'text': text,
        'suggestions': suggestions
    })


def about(request):
    return render(request, 'about.html')
