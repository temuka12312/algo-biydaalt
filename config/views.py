from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging
import os
from functools import lru_cache
import re

logger = logging.getLogger(__name__)

# SpellChecker тохируулах
spell = SpellChecker(language=None)

# Монгол хэлний толь бичгийн файлуудыг зааж өгөх
mn_dic_path = os.path.join('mn.dic')
mn_aff_path = os.path.join('mn.aff')

try:
    # mn.dic файлыг SpellChecker-д нэмэх
    spell.word_frequency.load_text_file(mn_dic_path)
    logger.info("mn.dic амжилттай ачааллаа.")

    # mn.aff файлыг SpellChecker-д дүрмийн дагуу нэмэх
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
    # Том үсгийг жижиг болгох
    text = text.lower()

    # Тусгай тэмдэгтүүд болон тоог устгах
    text = re.sub(r'[^\w\s]', '', text)  # Тусгай тэмдэгтүүдийг арилгах
    text = re.sub(r'\d+', '', text)      # Тоог арилгах

    # Үгсэд хуваах
    words = text.split()

    return words

# Кэштэй зөв бичгийн функц үүсгэх
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
