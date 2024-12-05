from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from spellchecker import SpellChecker
import logging
import os

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

@csrf_exempt
def spell_check_view(request):
    suggestions = {}
    text = ""

    if request.method == 'POST':
        text = request.POST.get('text', '') 
        words = text.split()  # Текстийг үгсэд хуваах

        misspelled_words = spell.unknown(words)

        for word in misspelled_words:
            if word in spell:
                suggestions[word] = word  # Үг өөрөө зөв гэж тооцох
            else:
                suggestions[word] = spell.correction(word)

    # Front-end-д буцаах
    return render(request, 'index.html', {
        'text': text,
        'suggestions': suggestions
    })

def about(request):
    return render(request, 'about.html')
